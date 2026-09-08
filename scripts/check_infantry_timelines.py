"""Validate static links, records and interactive timeline behavior.

python scripts/check_infantry_timelines.py [--browser]
Browser checks require selenium and Chrome, using a temporary local server.
"""
from pathlib import Path
from collections import defaultdict
from urllib.parse import urlsplit,unquote,quote
from datetime import date
from bs4 import BeautifulSoup
import argparse
import functools
import http.server
import threading

ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/'milhist/modern/US Infantry Regiments'

def static_checks():
    cache={}
    def parse(path):
        if path not in cache:cache[path]=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
        return cache[path]
    total=0
    for n in range(1,201):
        p=HERE/f'{n}RGT_timeline.html';s=parse(p)
        ids=[x['id'] for x in s.select('[id]')]
        assert len(ids)==len(set(ids)),f'Duplicate IDs: {p}'
        assert s.h1 and s.h1.text.startswith(str(n)),p
        for x in s.select('[aria-labelledby], [aria-describedby]'):
            for attr in ('aria-labelledby','aria-describedby'):
                for target in x.get(attr,'').split():assert target in ids,(p,attr,target)
        for tag,attr in [(x,'href') for x in s.select('[href]')]+[(x,'src') for x in s.select('[src]')]:
            url=urlsplit(tag[attr])
            if url.scheme or url.netloc:continue
            path=(p.parent/unquote(url.path)).resolve() if url.path else p
            assert path.exists(),(p,tag[attr])
            if url.fragment and path.suffix=='.html':assert parse(path).find(id=unquote(url.fragment)),(p,tag[attr])
        options={x['value'] for x in s.select('#unit-filter option')}
        rows=defaultdict(list)
        for r in s.select('.period'):
            assert r['data-unit']=='reg' or r['data-unit'] in options,(p,r['data-unit'])
            start=date.fromisoformat(r['data-start']);end=date.fromisoformat(r['data-end'])
            assert start<end,(p,r['id'])
            rows[r['data-unit']].append((start,end))
            for e in r.select('.deployment'):
                assert e.select_one('a[href]') and e.select_one('h5'),(p,e['id'])
                assert 1916<=int(e['data-year'])<=2026,(p,e['id'])
            total+=1
        for unit,spans in rows.items():
            spans.sort()
            for a,b in zip(spans,spans[1:]):assert a[1]<=b[0],(p,unit,a,b)
        for suffix in ('','_battalions'):
            assert parse(HERE/f'{n}RGT{suffix}.html').find('a',href=f'{n}RGT_timeline.html'),(n,suffix)
        assert s.find('a',href='infantry_timelines.html'),p
        if n>1:assert s.find('a',href=f'{n-1}RGT_timeline.html'),('previous',n)
        if n<200:assert s.find('a',href=f'{n+1}RGT_timeline.html'),('next',n)
    index=parse(HERE/'infantry_timelines.html')
    assert len(index.select('.timeline-index-card'))==200
    print(f'Static checks passed: 200 timeline pages, {total} periods, all local links/assets and source anchors.')

def browser_checks():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select,WebDriverWait
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self,*args):pass
        def handle(self):
            try:super().handle()
            except (ConnectionResetError,BrokenPipeError):pass
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(ROOT)))
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    options=webdriver.ChromeOptions();options.add_argument('--headless=new');options.add_argument('--window-size=1440,1000')
    options.set_capability('goog:loggingPrefs',{'browser':'ALL'})
    driver=webdriver.Chrome(options=options)
    base=f'http://127.0.0.1:{server.server_port}/'+quote('milhist/modern/US Infantry Regiments/')
    try:
        for n in range(1,201):
            driver.get(base+f'{n}RGT_timeline.html')
            WebDriverWait(driver,10).until(lambda d:d.find_element(By.ID,'overview').is_displayed())
            assert not driver.execute_script('return [...document.images].some(i=>!i.complete || !i.naturalWidth)'),n
            select=Select(driver.find_element(By.ID,'unit-filter'))
            for option in select.options:
                value=option.get_attribute('value');select.select_by_value(value)
                assert driver.execute_script('return [...document.querySelectorAll(".period,.battalion-evidence")].every(e=>e.hidden === !(arguments[0]==="all" || e.dataset.unit===arguments[0] || (e.classList.contains("period") && e.dataset.unit==="reg")))',value), (n,value)
            # Boundary lookup: exact dates must move to the next interval.
            for value in ('1916-01-01','1957-07-01','1969-02-15','2008-03-16','2026-09-08'):
                driver.execute_script('const e=document.getElementById("assignment-date");e.value=arguments[0];e.dispatchEvent(new Event("change"));',value)
                expected=driver.execute_script('return [...document.querySelectorAll(".period")].filter(e=>e.dataset.start<=arguments[0]&&arguments[0]<e.dataset.end).length',value)
                assert len(driver.find_elements(By.CSS_SELECTOR,'.date-result'))==expected,(n,value)
            markers=driver.find_elements(By.CSS_SELECTOR,'.deployment-marker')
            if markers:
                driver.execute_script('arguments[0].click()',markers[-1])
                assert driver.execute_script('return document.activeElement.classList.contains("deployment") && !document.activeElement.closest(".period").hidden'),n
            errors=[x for x in driver.get_log('browser') if x['level']=='SEVERE' and 'favicon.ico' not in x['message']]
            assert not errors,(n,errors)
            driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride',{'width':390,'height':844,'deviceScaleFactor':1,'mobile':True})
            assert driver.execute_script('return innerWidth===390 && document.documentElement.scrollWidth<=391'),('mobile overflow',n)
            driver.execute_cdp_cmd('Emulation.clearDeviceMetricsOverride',{})
        # Bookmark navigation must reveal an initially hidden battalion.
        company_page=BeautifulSoup((HERE/'52RGT_timeline.html').read_text(encoding='utf-8'),'html.parser')
        company_anchor=company_page.select_one('.period[data-unit="bnD"]')['id']
        for n,anchor in ((1,'battalion-3'),(9,'battalion-4'),(26,'battalion-four'),(44,'battalion-wwi'),(52,company_anchor)):
            driver.get(base+f'{n}RGT_timeline.html#{anchor}')
            WebDriverWait(driver,10).until(lambda d:d.find_element(By.ID,anchor).is_displayed())
        driver.execute_cdp_cmd('Emulation.setScriptExecutionDisabled',{'value':True})
        driver.get(base+'1RGT_timeline.html')
        assert all(e.is_displayed() for e in driver.find_elements(By.CSS_SELECTOR,'.period'))
        assert not driver.find_element(By.ID,'overview').is_displayed()
        print('Chrome checks passed: all 200 pages, every filter, five date boundaries, markers, mobile widths, bookmarks and no-JavaScript content.')
    finally:
        driver.quit();server.shutdown();server.server_close()

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--browser',action='store_true');args=parser.parse_args()
    static_checks()
    if args.browser:browser_checks()
