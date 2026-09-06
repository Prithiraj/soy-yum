#!/usr/bin/env python3
"""End-to-end browser checks against the actual generated site. Requires Playwright."""
from pathlib import Path
import json, os
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'test-results';OUT.mkdir(exist_ok=True)
BASE=os.getenv('TEST_URL','http://127.0.0.1:8765/soy-yum/')
AXE=os.getenv('AXE_PATH','/tmp/soy-qa/node_modules/axe-core/axe.min.js')
report={'base':BASE,'checks':[],'axe':{}}
def save_report():
    (OUT/'browser-report.json').write_text(json.dumps(report,indent=2))
def log(name):
    report['checks'].append(name);print('PASS',name);save_report()
def ready(page):
    page.evaluate("async () => {for (const image of document.querySelectorAll('img[src]')) {image.loading='eager';} await Promise.all([...document.images].filter(i=>i.src).map(i=>i.decode().catch(()=>{})));}")
    page.evaluate('document.fonts.ready')
with sync_playwright() as p:
    browser=p.chromium.launch(channel='chrome',headless=True,args=['--no-sandbox'])
    for width in (320,390,768,1024,1440):
        for route in ('','menu/'):
            page=browser.new_page(viewport={'width':width,'height':900},device_scale_factor=1)
            errors=[];page.on('pageerror',lambda e: errors.append(str(e)))
            response=page.goto(BASE+route,wait_until='networkidle');assert response.status==200
            ready(page)
            label=('home' if not route else 'menu')+f'-{width}'
            if width in (320,390,1440):page.screenshot(path=str(OUT/(label+'.png')),full_page=True)
            assert not errors,errors
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),(width,route,'overflow')
            assert page.locator('h1').count()==1
            assert page.locator('img[src]').evaluate_all('(images)=>images.every(i=>i.complete && i.naturalWidth>0)'),(width,route,'broken photo')
            # The first call link is correctly hidden inside collapsed mobile navigation.
            # The hero/mobile action bar must still expose a genuine phone destination.
            assert page.locator('a[href="tel:+918100581884"]:visible').count()>0,(width,route,'visible call action')
            if width==1440 and Path(AXE).exists():
                page.add_script_tag(path=AXE)
                result=page.evaluate("async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']}})")
                report['axe'][label]={'violations':result['violations'],'passes':len(result['passes']),'incomplete':len(result['incomplete'])}
                save_report()
                assert not result['violations'],[(v['id'],v['impact'],[n['target'] for n in v['nodes']]) for v in result['violations']]
            if width==390 and not route:
                toggle=page.locator('.nav-toggle');toggle.click();assert toggle.get_attribute('aria-expanded')=='true'
                assert page.locator('.navigation a').first.is_visible()
                page.keyboard.press('Escape');assert toggle.get_attribute('aria-expanded')=='false'
                assert toggle.evaluate('(e)=>e===document.activeElement')
                page.locator('.visit-faq summary').first.click();assert page.locator('.visit-faq details').first.get_attribute('open') is not None
                page.locator('[data-lightbox]').first.click();assert page.locator('#photo-dialog').evaluate('(e)=>e.open')
                page.keyboard.press('Escape');assert not page.locator('#photo-dialog').evaluate('(e)=>e.open')
                assert page.locator('[data-lightbox]').first.evaluate('(e)=>e===document.activeElement')
                log('mobile navigation, Escape/focus return, FAQ and photo dialog')
            if width==390 and route:
                page.locator('[data-filter="bakery"]').click();assert page.locator('.menu-item:visible').count()==1
                page.locator('[data-filter="all"]').click();page.locator('#menu-search').fill('ramen');assert page.locator('.menu-item:visible').count()==1
                page.locator('#menu-search').fill('no-such-dish');assert page.locator('.menu-empty').is_visible()
                page.locator('#reset-menu').click();assert page.locator('.menu-item:visible').count()==5
                log('menu category filtering, search, empty state and reset')
            log(f'{route or "home"}: {width}px, photos, actions, overflow, JS errors')
            page.close()
    for route in ('','menu/'):
        context=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844})
        page=context.new_page();page.goto(BASE+route,wait_until='networkidle')
        assert page.locator('.navigation a').first.is_visible()
        assert page.locator('main').is_visible()
        if route:assert page.locator('.menu-item:visible').count()==5
        assert page.locator('a[href="tel:+918100581884"]:visible').count()>0
        log(f'{route or "home"}: no-JavaScript fallback')
        context.close()
    context=browser.new_context(reduced_motion='reduce',viewport={'width':390,'height':844})
    page=context.new_page();page.goto(BASE,wait_until='networkidle')
    assert page.evaluate('getComputedStyle(document.documentElement).scrollBehavior')=='auto'
    assert page.locator('.experience-card').first.evaluate('(e)=>getComputedStyle(e).transitionDuration')=='0s'
    log('reduced-motion behavior')
    page.keyboard.press('Tab');assert page.locator('.skip-link').evaluate('(e)=>e===document.activeElement')
    page.keyboard.press('Enter');assert page.locator('#main').evaluate('(e)=>e===document.activeElement')
    log('keyboard skip link')
    context.close()
    for route in ('credits/','404.html'):
        page=browser.new_page(viewport={'width':390,'height':844});page.goto(BASE+route,wait_until='networkidle');ready(page)
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),route
        if Path(AXE).exists():
            page.add_script_tag(path=AXE);result=page.evaluate("async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']}})")
            report['axe'][route]={'violations':result['violations'],'passes':len(result['passes']),'incomplete':len(result['incomplete'])}
            save_report()
            assert not result['violations'],[(v['id'],v['impact']) for v in result['violations']]
        log(route+' mobile and accessibility checks');page.close()
    browser.close()
save_report()
print(f'PASS: {len(report["checks"])} browser check groups. Axe results written to test-results/.')
