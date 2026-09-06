#!/usr/bin/env python3
"""Build a static, no-JavaScript-required site. Python + Pillow, no runtime framework.

Default: a clearly labelled, noindex preview. Production refuses uncleared assets
or unapproved business/menu information. Downloaded images are an ephemeral cache.
"""
from __future__ import annotations
import argparse
import html
import io
import json
import re
import shutil
import time
import urllib.parse
import urllib.request
from pathlib import Path
from PIL import Image, ImageChops, ImageFont, ImageDraw, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_HOSTS = {'b.zmtcdn.com', 'ugc.production.linktr.ee'}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', default='/soy-yum/')
    parser.add_argument('--origin', default='https://prithiraj.github.io')
    parser.add_argument('--offline', action='store_true', help='Require all originals in .cache/images')
    parser.add_argument('--production', action='store_true', help='Require documented owner and rights approval')
    args = parser.parse_args()
    base = '/' + args.base.strip('/') + '/' if args.base.strip('/') else '/'
    origin = args.origin.rstrip('/')
    if urllib.parse.urlparse(origin).scheme not in {'http', 'https'}:
        raise SystemExit('Origin must be an HTTP(S) URL.')
    site = json.loads((ROOT / 'content/site.json').read_text())
    photos = json.loads((ROOT / 'content/photos.json').read_text())
    menu = json.loads((ROOT / 'content/menu.json').read_text())
    if args.production:
        missing = [key for key, value in photos.items() if not value.get('production_approved')]
        if missing or not site.get('owner_approved') or not site.get('hours') or not site.get('current_menu_approved'):
            raise SystemExit('PRODUCTION BLOCKED: obtain and record image rights, owner approval, weekly hours and an approved current menu. No deployment generated.')
        # The current copy deliberately identifies an independent preview. Merely changing a flag must not remove that safeguard.
        raise SystemExit('PRODUCTION BLOCKED: replace preview-specific copy and metadata with approved business copy, then update the release tests.')
    out = ROOT / '_site'
    if out.exists(): shutil.rmtree(out)
    (out / 'assets/img').mkdir(parents=True)
    cache = ROOT / '.cache/images'
    cache.mkdir(parents=True, exist_ok=True)
    dimensions = {}
    report = {}
    for key, photo in photos.items():
        url = photo['url']
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme != 'https' or parsed.hostname not in ALLOWED_HOSTS:
            raise SystemExit(f'Unapproved image host: {key}')
        original = cache / (key + '.jpg')
        if not original.exists():
            if args.offline: raise SystemExit(f'Missing cached photograph: {key}')
            for attempt in range(3):
                try:
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=30) as response:
                        data = response.read(15_000_001)
                    if len(data) > 15_000_000: raise ValueError('Image exceeds 15 MB safety limit')
                    im = ImageOps.exif_transpose(Image.open(io.BytesIO(data))).convert('RGB')
                    im.save(original, quality=95)
                    break
                except Exception:
                    if attempt == 2: raise
                    time.sleep(2 ** attempt)
        im = ImageOps.exif_transpose(Image.open(original)).convert('RGB')
        if key == 'logo':
            # Remove only empty white margins; retain the complete original brand mark.
            diff = ImageChops.difference(im, Image.new('RGB', im.size, 'white'))
            box = diff.point(lambda p: 255 if p > 50 else 0).getbbox()
            if box: im = im.crop((max(0, box[0]-12), max(0,box[1]-12), min(im.width,box[2]+12), min(im.height,box[3]+12)))
            im.thumbnail((200,270)); im.save(out/'assets/img/logo.png', optimize=True)
            dimensions[key] = im.size
            continue
        dimensions[key] = im.size
        sizes = {}
        for width in (480,800,1200):
            # Do not enlarge low-resolution sources. Width suffix denotes the requested tier.
            actual = min(width, im.width)
            resized = im.resize((actual, round(im.height * actual / im.width)), Image.Resampling.LANCZOS)
            for extension, quality in [('webp',82),('jpg',86)]:
                dest=out/f'assets/img/{key}-{width}.{extension}'
                resized.save(dest, quality=quality, optimize=True, **({'method':6} if extension=='webp' else {'progressive':True}))
                sizes[dest.name] = dest.stat().st_size
        report[key] = sizes
    for name in ('style.css','app.js','favicon.svg'):
        shutil.copy(ROOT/'assets'/name, out/'assets'/name)

    def picture(match: re.Match) -> str:
        key, role = match.group(1), match.group(2)
        photo = photos[key]
        width,height = dimensions[key]
        eager = role in {'hero','menuhero'}
        sizes = '(max-width: 767px) 88vw, (max-width: 1100px) 43vw, 570px' if role in {'hero','menuhero','feature'} else '(max-width: 767px) 88vw, 400px'
        if role == 'gallery': sizes = '(max-width: 767px) 85vw, 520px'
        srcset=', '.join(f'{base}assets/img/{key}-{w}.webp {min(w,width)}w' for w in (480,800,1200))
        loading='loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
        return f'<picture><source type="image/webp" srcset="{srcset}" sizes="{sizes}"><img src="{base}assets/img/{key}-800.jpg" width="{width}" height="{height}" alt="{html.escape(photo["alt"],quote=True)}" {loading} decoding="async"></picture>'

    item_html=[]
    seen=set()
    for i,item in enumerate(menu,1):
        category=item['category']
        anchor=f' id="{category}"' if category not in seen else ''
        seen.add(category)
        search=html.escape((item['name']+' '+item['description']+' '+item['label']).lower(),quote=True)
        item_html.append(f'''<article class="menu-item"{anchor} data-category="{html.escape(category)}" data-search="{search}"><div class="item-category"><span class="item-number">0{i}</span>{html.escape(item['label'].upper())}</div><div><h3>{html.escape(item['name'])}</h3><p>{html.escape(item['description'])}</p><p class="item-source">Published reference: {html.escape(item['source_date'])} · <a href="{html.escape(site[item['source']],quote=True)}" target="_blank" rel="noopener noreferrer">Source ↗<span class="sr-only"> (opens in a new tab)</span></a></p></div><a class="item-action" href="tel:{site['phone']}">Ask the team ↗<span class="sr-only"> about {html.escape(item['name'])}</span></a></article>''')

    credits=[]
    for key,photo in photos.items():
        src=f'{base}assets/img/logo.png' if key=='logo' else f'{base}assets/img/{key}-480.webp'
        credits.append(f'''<article class="credit-item" id="{key}"><img src="{src}" alt="{html.escape(photo['alt'],quote=True)}" width="480" height="320" loading="lazy"><div><h3>{html.escape(photo['caption'])}</h3><p><strong>Preview only · reuse rights unconfirmed.</strong></p><p>{html.escape(photo['rightsholder'])}</p><a href="{html.escape(photo['source'],quote=True)}" target="_blank" rel="noopener noreferrer">Published source ↗<span class="sr-only"> (opens in a new tab)</span></a></div></article>''')
    common={**{k:html.escape(v,quote=True) for k,v in site.items() if isinstance(v,str)},'base':base,'origin':origin,'robots':'noindex, nofollow','menu_items':'\n'.join(item_html),'photo_credits':'\n'.join(credits)}
    pages=[('index.html','index.html','Soy Yum Hindustan Park | Sushi, Korean BBQ & Asian Bakery','Discover Japanese dining, Korean BBQ and the Asian bakery at Soy Yum, Hindustan Park, Kolkata. Explore menu highlights and plan a visit. Website design preview.'),('menu.html','menu/index.html','Menu Highlights | Soy Yum Hindustan Park','Explore published Soy Yum highlights: sushi, ramen, Korean BBQ and Japanese cheesecake. Call the Hindustan Park restaurant for current availability and prices.'),('credits.html','credits/index.html','Photo Credits & Site Notes | Soy Yum Website Preview','Photography sources, preview-use restrictions, business evidence and privacy notes for this independent Soy Yum website design.'),('404.html','404.html','Page Not Found | Soy Yum','That page is not here. Return to Soy Yum and explore the restaurant website preview.')]
    for template,destination,title,description in pages:
        canonical=origin+base+(destination.replace('index.html','') if destination!='404.html' else '404.html')
        data={**common,'title':html.escape(title),'description':html.escape(description,quote=True),'canonical':canonical,'menu_current':'aria-current="page"' if template=='menu.html' else ''}
        if template=='index.html':
            schema={'@context':'https://schema.org','@type':'Restaurant','@id':origin+base+'#restaurant','name':'Soy Yum — Hindustan Park','description':'Japanese dining, sushi, Korean BBQ and an in-house Asian bakery. Referenced in an independent website design preview; restaurant approval pending.','telephone':site['phone'],'address':{'@type':'PostalAddress','streetAddress':'P353B, Keyatala Road, Hindustan Park','addressLocality':'Kolkata','addressRegion':'West Bengal','postalCode':'700029','addressCountry':'IN'},'geo':{'@type':'GeoCoordinates','latitude':22.5147434,'longitude':88.362267},'servesCuisine':['Japanese','Korean'],'hasMap':site['maps'],'subjectOf':{'@type':'WebPage','url':origin+base,'name':'Independent Soy Yum website design preview'}}
            data['jsonld']='<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False).replace('</','<\\/')+'</script>'
        else: data['jsonld']=''
        for part in ('head','header','footer'):
            data[part]=(ROOT/'src/partials'/f'{part}.html').read_text()
        rendered=(ROOT/'src'/template).read_text()
        for _ in range(3):
            for key,value in data.items(): rendered=rendered.replace('{{'+key+'}}',value)
        rendered=re.sub(r'\{\{photo:([a-z-]+):([a-z]+)\}\}',picture,rendered)
        if '{{' in rendered: raise SystemExit(f'Unresolved template token in {template}')
        path=out/destination;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(rendered)
    (out/'.nojekyll').touch()
    (out/'robots.txt').write_text('User-agent: *\nAllow: /\n# Independent preview: all HTML pages carry noindex, nofollow.\n')
    (out/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>\n')
    # Original typographic sharing card. No unlicensed photograph in link previews.
    card=Image.new('RGB',(1200,630),'#fff8ee');draw=ImageDraw.Draw(card)
    def font(size:int):
        for name in ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','DejaVuSans.ttf']:
            try:return ImageFont.truetype(name,size)
            except OSError:pass
        return ImageFont.load_default(size=size)
    draw.rectangle((0,0,1200,22),fill='#b93227');draw.ellipse((850,170,1230,550),fill='#e4ee9b')
    draw.text((70,65),'SOY YUM / HINDUSTAN PARK',font=font(24),fill='#b93227')
    draw.text((65,140),'Sushi. Sizzle.',font=font(86),fill='#29201d')
    draw.text((65,250),'Something sweet.',font=font(84),fill='#b93227')
    draw.text((70,418),'Japanese dining · Korean BBQ · Asian bakery',font=font(28),fill='#29201d')
    draw.text((70,545),'KOLKATA / INDEPENDENT WEBSITE DESIGN PREVIEW',font=font(18),fill='#655b54')
    card.save(out/'assets/og-card.png',optimize=True)
    (out/'build-info.json').write_text(json.dumps({'mode':'preview','research_checked':site['checked'],'image_sizes':report},indent=2))
    total=sum(p.stat().st_size for p in out.rglob('*') if p.is_file())
    print(f'Built {len(pages)} static pages, {len(photos)-1} real photographs. Mode: PREVIEW / noindex. Total variants: {total:,} bytes.')

if __name__ == '__main__':
    main()
