#!/usr/bin/env python3
"""Validate generated HTML, local destinations, metadata and launch safeguards."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import gzip, json, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'_site'
BASE='/soy-yum/'
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.h1=0;self.ids=set();self.links=[];self.images=[];self.metas={};self.html=False;self.main=0;self.jsonld=False;self.feed(text)
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=='html': self.html=d.get('lang')=='en-IN'
        if tag=='h1':self.h1+=1
        if tag=='main':self.main+=1
        if 'id' in d:
            assert d['id'] not in self.ids,f'Duplicate ID: {d["id"]}'
            self.ids.add(d['id'])
        if tag=='a':self.links.append(d.get('href',''))
        if tag=='img':self.images.append(d)
        if tag=='meta':self.metas[d.get('name',d.get('property',''))]=d.get('content','')
        if tag=='script' and d.get('type')=='application/ld+json':self.jsonld=True
pages={p.relative_to(SITE).as_posix():Page(p.read_text()) for p in SITE.rglob('*.html')}
assert len(pages)==4
for path,page in pages.items():
    assert page.html and page.h1==1 and page.main==1,(path,'landmarks')
    assert 'noindex' in page.metas.get('robots',''),(path,'preview indexing')
    for field in ('description','og:title','og:description','og:url','og:image','og:image:alt'):
        assert page.metas.get(field),(path,field)
    for im in page.images:
        assert 'alt' in im and 'width' in im and 'height' in im,(path,'image accessibility')
        if im.get('src','').startswith(BASE):assert (SITE/im['src'][len(BASE):]).exists()
    for href in page.links:
        assert href and href!='#',(path,'placeholder link')
        url=urlsplit(href)
        if url.scheme:continue
        target=url.path
        if target.startswith(BASE):
            target=unquote(target[len(BASE):])
            if target.endswith('/') or not target:target+='index.html'
        elif target=='':target=path
        else:raise AssertionError((path,'Unexpected non-base-relative link',href))
        assert (SITE/target).exists(),(path,'broken local link',href)
        if url.fragment and target in pages:assert url.fragment in pages[target].ids,(path,'missing anchor',href)
assert pages['index.html'].jsonld
for name,budget in [('app.js',20_000),('style.css',35_000)]:
    size=len(gzip.compress((SITE/'assets'/name).read_bytes()))
    assert size<budget,(name,size,budget)
    print(f'{name}: {size:,} bytes gzip (budget {budget:,})')
for p in SITE.rglob('*.html'):assert '{{' not in p.read_text()
result=subprocess.run([sys.executable,str(ROOT/'scripts/build.py'),'--production','--offline'],capture_output=True,text=True)
assert result.returncode!=0 and 'PRODUCTION BLOCKED' in result.stderr
print('PASS: four pages; local links, anchors, metadata, alt text, unique IDs, size budgets and production gate.')
