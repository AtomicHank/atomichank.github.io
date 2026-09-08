"""Build the 1-200 infantry numbering series from reviewed sources using the 26th's layout.

Run from any directory: python scripts/build_infantry_timelines.py
Requires beautifulsoup4. The hand-edited 26th prototype is never regenerated.
The browser reads static HTML; Python and the source data are build tools only.
"""
from pathlib import Path
from datetime import date
from html import escape
from urllib.parse import quote
import json
import re
from bs4 import BeautifulSoup
from infantry_timeline_data import ROWS, NOTES
from infantry_timeline_events import SERVICE, TOURS, CAMPAIGNS
from infantry_timeline_supplements import SOURCES as SUPPLEMENT_SOURCES, UPDATES, EXTRA_ROWS, EVIDENCE
import infantry_timeline_data_31_60 as EXT
import infantry_timeline_data_61_100 as EXT2
import infantry_timeline_data_101_200 as EXT3
import argparse

ROWS = ROWS + EXT.ROWS
NOTES = {**NOTES, **EXT.NOTES}
SERVICE = SERVICE + EXT.SERVICE
TOURS = TOURS + EXT.TOURS
CAMPAIGNS = {**CAMPAIGNS, **EXT.CAMPAIGNS}
EVIDENCE = EVIDENCE + EXT.EVIDENCE
SUPPLEMENT_SOURCES = {**SUPPLEMENT_SOURCES, **EXT.SOURCES}
UPDATES = {**UPDATES, **EXT.UPDATES}

ROWS += EXT2.ROWS
NOTES.update(EXT2.NOTES)
SERVICE += EXT2.SERVICE
TOURS += EXT2.TOURS
CAMPAIGNS.update(EXT2.CAMPAIGNS)
EVIDENCE += EXT2.EVIDENCE
SUPPLEMENT_SOURCES.update(EXT2.SOURCES)
UPDATES.update(EXT2.UPDATES)
STEP_SOURCES = {**EXT.STEP_SOURCES, **EXT2.STEP_SOURCES}
OPERATIONS = EXT.OPERATIONS + EXT2.OPERATIONS

ROWS += EXT3.ROWS
NOTES.update(EXT3.NOTES)
EVIDENCE += EXT3.EVIDENCE
SUPPLEMENT_SOURCES.update(EXT3.SOURCES)
OPERATIONS += EXT3.OPERATIONS
UNIT_LABELS = {**EXT2.UNIT_LABELS, **EXT3.UNIT_LABELS}
PERIOD_NOTES = {**EXT2.PERIOD_NOTES, **EXT3.PERIOD_NOTES}
def is_numbering(n): return 92<=n<=100 or n in EXT3.NUMBERING

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / 'milhist/modern/US Infantry Regiments'
SCRIPTS = Path(__file__).resolve().parent
CUTOFF = '2026-09-08'
END = '2026-09-09'
PATCHES = json.loads((SCRIPTS/'infantry_timeline_patches.json').read_text(encoding='utf-8'))
SOURCES = json.loads((SCRIPTS/'infantry_timeline_sources.json').read_text(encoding='utf-8'))
for sid,(url,title) in SUPPLEMENT_SOURCES.items():
    SOURCES[str(sid)] = dict(url=url,title=title)

def ordinal(n):
    return str(n) + ('th' if 10 <= n % 100 <= 20 else {1:'st',2:'d',3:'d'}.get(n%10,'th'))

def wiki(n):
    number = str(n)+('th' if 10 <= n%100 <= 20 else {1:'st',2:'nd',3:'rd'}.get(n%10,'th'))
    return f'https://en.wikipedia.org/wiki/{number}_Infantry_Regiment_(United_States)'

for n in range(1,201):
    SOURCES[str(1000+n)] = dict(url=wiki(n),title=f'{ordinal(n)} Infantry Regiment history (Wikipedia; secondary)')

LABELS = {f'd{n}':f'{ordinal(n)} Infantry Division' for n in range(1,104)}
LABELS.update({f'd{n}':f'{ordinal(n)} Division (World War I)' for n in range(11,20)})
LABELS.update(d10='10th Division',d23='23d Infantry Division (Americal)',
    a1='1st Armored Division',a2='2d Armored Division',m10='10th Mountain Division',
    ab11='11th Airborne Division',hawaii='Hawaiian Division',phil='Philippine Division',
    const1='1st Constabulary Regiment',berlin='Berlin Brigade',usma='United States Military Academy',
    training='TRADOC · Training',ind='No assigned division',inactive='Inactive',unk='Assignment not established')
for n in (1,2,11,170,171,172,193,194,196,197,198,199):
    LABELS[f'b{n}'] = f'{ordinal(n)} Infantry Brigade · Separate'

LABELS.update({f'a{n}': f'{ordinal(n)} Armored Division' for n in range(3,14)})
LABELS.update(d20='20th Division (World War I)', panama='Panama Canal Division',
    cav1='1st Cavalry Division', const14='14th Constabulary Regiment',
    b177='177th Armored Brigade', attached83='Attached to 83d Division · Depot service',
    training101='Attached to 101st Airborne Division · Training',
    notformed='Not yet constituted / organized', disbanded='Disbanded',
    captured='Surrendered · Captivity and surviving detachments')
LABELS.update(a14='14th Armored Division', ab13='13th Airborne Division',
    b92='92d Infantry Brigade \u00b7 Separate', b93='93d Infantry Brigade \u00b7 Separate',
    ar96='96th Army Reserve Command', medical='Warrior Transition Battalion \u00b7 Medical support',
    reserve='Army Reserve \u00b7 Division assignment not established',
    training_ww2='Training \u00b7 No assigned division', abbrig1='1st Airborne Brigade \u00b7 Separate',
    never='Regiment not constituted')
LABELS.update({f'a{n}':f'{ordinal(n)} Armored Division' for n in (27,40,48,49,50)})
LABELS.update({f'b{n}':f'{ordinal(n)} Infantry Brigade \u00b7 Brigade assignment' for n in (26,27,30,32,33,37,39,40,41,45,48,49,50,53,58,67,69,73,76,81,86,155,256)})
LABELS.update(ab82='82d Airborne Division',aa11='11th Air Assault Division',ab17='17th Airborne Division',ab101='101st Airborne Division',
    attached106='Attached to 106th Infantry Division',armbrig40='40th Armored Brigade',armbrig53='53d Armored Brigade',
    converted='Converted to another branch',priorbranch='Other branch / predecessor service',
    merged='Consolidated into another organization',renamed103='Redesignated as 103d Infantry',
    renamed1='Redesignated as 1st Virginia Infantry',renamed176='Redesignated as 176th Infantry',
    renamed206='Redesignated as 206th Infantry Battalion')
for code, label in list(LABELS.items()):
    LABELS['i_'+code] = 'Inactive · '+label

def kind(code):
    if code in ('converted','priorbranch','merged') or code.startswith('renamed'):return 'inactive'
    if code.startswith('i_') or code in ('notformed','disbanded','captured','never'): return 'inactive'
    if code in ('training101','training_ww2','medical'): return 'training'
    if code in ('ar96','reserve','abbrig1'): return 'separate'
    return {'d1':'first','d2':'second','d8':'eighth','training':'training','usma':'training',
        'inactive':'inactive','unk':'unknown','ind':'separate'}.get(code,
        'airborne' if code=='ab11' else ('separate' if code.startswith('b') or code=='const1' else 'division'))

def short(code):
    if code.startswith('i_'):return 'Inactive: '+short(code[2:])
    if code.startswith('a') and code[1:].isdigit():return ordinal(int(code[1:]))+' AD'
    if code.startswith('d') and code[1:].isdigit(): return ordinal(int(code[1:]))+' ID'
    return {'ab11':'11th ABN','a1':'1st AD','a2':'2d AD','m10':'10th MTN','hawaii':'Hawaiian',
        'phil':'Philippine','training':'Training','usma':'USMA','inactive':'Inactive',
        'unk':'Unverified','ind':'No division','berlin':'Berlin','const1':'Constabulary'}.get(code,LABELS[code])

def fmt(iso):
    d=date.fromisoformat(iso)
    return f'{d.day} {d:%b %Y}'

def fragment(html):
    return BeautifulSoup(html,'html.parser')

def set_html(element,html):
    element.clear()
    element.extend(list(fragment(html).contents))

def link_source(sid):
    return f'<a href="#source-{sid}">Source</a>'

def patch(code,css='division-patch',width=56,height=76):
    code=code.removeprefix('i_')
    if code not in PATCHES:return ''
    return f'<img class="{css}" src="images/division-patches/{PATCHES[code][0]}" alt="" width="{width}" height="{height}">'

def unit_key(b): return 'reg' if b==0 else 'bn'+str(b)
def unit_label(n,b):
    if (n,b) in UNIT_LABELS:return UNIT_LABELS[n,b]
    if is_numbering(n) and b==0:return f'{ordinal(n)} Infantry \u00b7 Regimental numbering record'
    if b==0:return f'{ordinal(n)} Infantry Regiment'
    if isinstance(b,str):
        if b.startswith('aib'):return f'{ordinal(int(b[3:]))} Armored Infantry Battalion · Predecessor'
        if b.startswith('ps') and b[2:].isdigit():return f'{ordinal(int(b[2:]))} Infantry Battalion (Philippine Scouts) · Successor'
        if b=='wwi':return 'World War I organization'
        if b=='ps':return '44th Infantry (Philippine Scouts) · Separate organization'
        return f'Company {b} · Headquarters lineage'
    return f'{ordinal(b)} Battle Group / Battalion lineage'

def make_records(n):
    records=[]
    for rn,b,sid,transitions in sorted(ROWS+EXTRA_ROWS,key=lambda x:(x[0],isinstance(x[1],str),x[1])):
        if rn!=n:continue
        steps=[(t.split()[0],t.split()[1],sid) for t in transitions.split(';')]
        if (n,b) in UPDATES:
            usid,extra=UPDATES[n,b]
            steps.extend((t.split()[0],t.split()[1],usid) for t in extra.split(';'))
        # The Hawaiian Division was redesignated on 26 August, not the
        # 1 October activation date of the separate 25th Infantry Division.
        if n in (19,21) and b==0:
            steps=[('1941-08-26',c,210) if d=='1941-10-01' and c=='d24' else (d,c,s) for d,c,s in steps]
        # CMH's parent certificate omits WWII's separate-regiment service.
        if n==24 and b==0:steps.insert(1,('1943-08-28','ind',1024))
        # Month-only inactivation of the 13th in 1940 is independently dated.
        if n==13 and b==0:
            steps=[x for x in steps if x[0]!='1940-06-22']
            steps.extend([('1940-06-14','inactive',1013),('1940-07-14','d8',1013)])
            steps.sort()
        for i,(start,code,source) in enumerate(steps):
            if code=='end':break
            end=steps[i+1][0] if i+1<len(steps) else END
            assert start<end,(n,b,start,end)
            last=end==END
            note='Division names are normalized across historical redesignations. This entry follows the cited unit lineage.'
            if code=='inactive':note='The unit or its headquarters lineage was inactive. This status does not imply that every inherited honor or divisional affiliation was erased.'
            elif code=='ind':note='The cited record establishes service outside an assigned division. Higher headquarters and temporary operational attachments could still direct the unit.'
            elif code=='unk':note='The available record does not establish a precise assignment throughout this interval. No division is inferred.'
            elif code in ('training','usma'):note='Institutional or training service. This is a command relationship, not a maneuver-division assignment.'
            elif code.startswith('b') or code=='const1':note='This headquarters is not a division. Temporary attachments in the service entries below are distinct from the formal assignment.'
            elif code.startswith('i_'):note='The unit was inactive but retained the division assignment shown. Paper assignments and Reserve-officer training are not active combat service.'
            elif code=='notformed':note='This timeline begins in 1916. The cited organization had not yet been constituted or organized during this interval; its formation follows.'
            elif code=='disbanded':note='The organization was removed from the rolls. A later reconstitution, if documented, is shown separately.'
            elif code=='captured':note='Organized resistance ended in surrender. Captivity and surviving detachments are not treated as normal divisional service or a formal inactivation order.'
            elif code in ('attached83','training101'):note='An attachment for depot or training service, not a formal maneuver-division assignment.'
            if (n,b,start) in STEP_SOURCES:source=STEP_SOURCES[n,b,start]
            if (n,b) in UPDATES and code=='unk' and start[:4] in ('2012','2013'):
                note='The parent brigade inactivated during this month. A precise effective date for this battalion is not established here.'
            if n==28 and b==1 and start=='2023-03-24':source=202
            if n==9 and b==4 and start=='2014-03-17':source=201
            note=PERIOD_NOTES.get((n,b,start),note)
            title=LABELS[code]
            approximate=(n,b,start) in EXT3.APPROXIMATE
            if approximate:title+=' \u00b7 Approximate period'
            if last:
                title='Last documented: '+title
                note+=' The source establishes this last recorded status, not uninterrupted service through 2026. The striped bar extends to the page cutoff to keep the later research gap visible.'
            records.append(dict(b=b,unit=unit_key(b),start=start,end=end,code=code,kind='reported' if last else ('unknown' if approximate else kind(code)),
                title=title,note=note,source=source,last=last,events=[]))
    return records

def make_events(n,records):
    events=[]
    for rn,b,years,title,sid in SERVICE:
        if rn==n:
            if sid==218:
                events.append((b,years,title,'Combat operations','The Army\'s Combat Studies Institute documents the battalion\'s operations in these districts during autumn 2009. This marker does not define the entire tour.',sid))
            else:
                events.append((b,years,title,'Credited overseas service','The Army lineage lists a unit decoration for service in these years. These are credited service years, not exact deployment and return dates.',sid))
    for rn,b,years,title,note in TOURS:
        if rn==n:events.append((b,years,title,'Deployment / overseas operation',note,1000+n))
    for rn,b,years,title,note,sid in OPERATIONS:
        if rn==n:events.append((b,years,title,'Deployment / campaign service',note,sid))
    regsource=next((r['source'] for r in records if r['b']==0 and r['code'] not in ('unk','inactive','notformed','disbanded')),records[0]['source'])
    for years,title in CAMPAIGNS.get(n,[]):
        events.append((0,years,title,'Campaign service','Campaign participation is recorded in the cited history. The year label summarizes campaign service, not an exact overseas tour.',regsource))
    for i,(b,years,title,category,note,source) in enumerate(events,1):
        year=years[:4]
        matching=[r for r in records if r['b']==b and r['start'][:4]<=year and r['end'][:4]>=year and r['code'] not in ('inactive','unk','notformed','disbanded','captured') and not r['code'].startswith('i_')]
        if not matching:
            matching=[r for r in records if r['b']==b and r['start'][:4]<=year and r['end'][:4]>=year and r['code']=='unk']
        assert matching,(n,b,years,title)
        # Place a year-only record in that year's final documented active
        # assignment. Explain any ambiguity instead of inventing a tour day.
        parent=matching[-1]
        if len(matching)>1:
            note+=' More than one assignment falls in the opening year; this year-level service marker does not establish the assignment on a particular deployment day.'
        endyear=years[-4:]
        if parent['end'][:4]<=endyear and not parent['last']:
            note+=' The labeled service overlaps an assignment change and is listed only once; consult the following assignment cards as well.'
        parent['events'].append(dict(id='deployment-'+str(i),year=year,years=years,title=title,category=category,note=note,source=source))

def build(n,template):
    soup=BeautifulSoup(template,'html.parser')
    name=ordinal(n)+' Infantry'
    soup.title.string=name+' · Division Timeline'
    soup.select_one('meta[name="description"]')['content']=f'Division assignments and selected deployments of the {name} Regiment and its battalions, 1916-2026, with patches and sources.'
    soup.h1.string=name+(' \u00b7 Numbering record' if is_numbering(n) else ' Regiment')
    for a in soup.select('a[href]'):
        if a['href']=='26RGT.html':a['href']=f'{n}RGT.html';a.string=name
        elif a['href']=='26RGT_battalions.html':a['href']=f'{n}RGT_battalions.html'
    soup.select_one('.timeline-hero .eyebrow').string='Infantry timelines · Infantry numbers 1–200'
    soup.select_one('.hero-text').string='1916–2026 · Regimental service, battle groups, battalions and deployments.'
    image=soup.select_one('.regiment-mark img')
    asset=HERE/f'images/BLU USA {n} IN RGT.png'
    if asset.exists() and not is_numbering(n):image['src']='images/'+quote(asset.name);image['alt']=name+' Regiment unit graphic'
    else:soup.select_one('.regiment-mark').decompose()
    if soup.select_one('.regiment-mark figcaption'):soup.select_one('.regiment-mark figcaption').string=name+' Regiment'
    for e in soup.select('.battalion-evidence'):e.decompose()
    for e in soup.select('nav[aria-label="Timeline series"]'):e.decompose()
    records=make_records(n)
    make_events(n,records)
    notes=[e for e in EVIDENCE if e[0]==n]
    units=sorted({r['b'] for r in records if r['b']}|{e[1] for e in notes},key=lambda b:(isinstance(b,str),b))
    first=min((r for r in records if re.fullmatch(r'(?:d|a|ab|aa|m|cav)\d+',r['code']) or r['code'] in ('hawaii','phil','panama')),key=lambda r:r['start'],default=None)
    set_html(soup.select_one('.summary-grid'),f'''<div class="summary-card"><span class="summary-label">First division shown</span><strong>{escape(LABELS[first['code']]) if first else 'Not established'}</strong><span>{fmt(first['start']) if first else 'See source notes'}</span></div>
<div class="summary-card"><span class="summary-label">Separate unit histories</span><strong>{len(units)} documented elements</strong><span>Dated lineages and service notes below</span></div>
<div class="summary-card"><span class="summary-label">Page cutoff</span><strong>8 September 2026</strong><span>Last-documented status is explicitly marked</span></div>''')
    regend=next((r['end'] for r in records[::-1] if r['b']==0),END)
    text='The common row follows the regiment. After its reorganization, battle groups and battalions could hold different assignments at the same time. A deployment or temporary attachment does not by itself change the assigned division.'
    if regend!=END:text+=f' The common row closes on {fmt(regend)}; later service belongs to the separate element rows.'
    text+=' Battalion rows follow headquarters lineages, often descended from lettered companies, rather than assuming that the old regimental battalions continued unchanged.'
    if is_numbering(n):text='No U.S. Regular Army infantry regiment was constituted under this number. The numbering row and any separately numbered battalion histories have different identities.'
    if n in EXT3.NUMBERING:text='The site includes this numbered placeholder, but a matching infantry-regiment lineage has not been established. Related training institutes and similarly numbered brigades are identified separately.'
    set_html(soup.select_one('.reading-note'),('<h2>Numbering and separate battalions</h2><p>' if is_numbering(n) else '<h2>One regiment, separate assignments</h2><p>')+escape(text)+'</p>'+('<p>'+escape(NOTES[n])+'</p>' if n in NOTES else ''))
    gallery={}
    used_sources=set()
    html=[]
    for i,r in enumerate(records,1):
        r['id']='period-'+str(i)
        code=r['code'];used_sources.add(r['source'])
        patchcode=code.removeprefix('i_')
        if patchcode in PATCHES and patchcode not in gallery:gallery[patchcode]=r['id']
        dates=fmt(r['start'])+' – '+('page cutoff*' if r['last'] else fmt(r['end']))
        title=f'<div class="division-heading">{patch(code)}<h3>{escape(r["title"])}</h3></div>'
        deployments=''
        if r['events']:
            items=[]
            for e in r['events']:
                used_sources.add(e['source'])
                items.append(f'<li class="deployment" id="{e["id"]}" data-year="{e["year"]}"><p class="deployment-date">{e["years"]}</p><h5>{escape(e["title"])}</h5><p class="deployment-unit">{escape(unit_label(n,r["b"]))} · {escape(e["category"])}</p><p>{escape(e["note"])}</p>{link_source(e["source"])}</li>')
            deployments='<section class="deployments" aria-label="Deployments and campaign service"><h4>Deployments &amp; overseas operations</h4><ol class="deployment-list">'+''.join(items)+'</ol></section>'
        html.append(f'''<li class="period {r['kind']}" id="{r['id']}" data-unit="{r['unit']}" data-start="{r['start']}" data-end="{r['end']}" data-kind="{r['kind']}" data-short="{escape(('Approx.: ' if (n,r['b'],r['start']) in EXT3.APPROXIMATE else ('Last: ' if r['last'] else ''))+short(code))}">
<div class="period-date">{dates}</div><article class="period-card"><p class="unit-label">{escape(unit_label(n,r['b']))}</p>{title}<p class="period-note">{escape(r['note'])}</p><p class="period-sources">{link_source(r['source'])}</p>{deployments}</article></li>''')
    set_html(soup.select_one('#period-list'),'\n'.join(html))
    set_html(soup.select_one('.patch-grid'),''.join(f'<a class="patch-key" href="#{pid}">{patch(c,width=64,height=88)}<strong>{escape(LABELS[c])}</strong></a>' for c,pid in gallery.items()))
    if not gallery:set_html(soup.select_one('.patch-grid'),'<p>Division names appear in the timeline. No verified patch artwork is included for these assignments.</p>')
    soup.select_one('#patch-title').parent.select_one('.chart-help').string='Representative division patches. Patterns could change over time; an image does not imply that the exact version was worn throughout every period. Divisions without a verified asset remain identified by name.'
    set_html(soup.select_one('.legend'),''.join(f'<li><span class="swatch {c}"></span>{t}</li>' for c,t in [('division','Division assignment'),('first','1st Infantry'),('second','2d Infantry'),('eighth','8th Infantry'),('separate','Separate headquarters'),('training','Training / academy'),('inactive','Inactive'),('unknown','Unverified / last documented')]))
    soup.select_one('#date-explorer > div p:not(.eyebrow)').string='Look up the dated rows below. Service notes with incomplete dates are excluded; last-documented results do not certify a current assignment.'
    soup.select_one('#latest-date').string='Page cutoff'
    set_html(soup.select_one('#unit-filter'),''.join(f'<option value="{unit_key(b)}" data-label="{escape(unit_label(n,b))}">Regiment → {escape(unit_label(n,b))}</option>' for b in units)+( '<option value="reg">Regimental history</option>' if not units else '')+'<option value="all">All documented elements</option>')
    soup.select_one('.deployment-intro').string='Deployments, operations and credited campaign service appear inside assignment cards. Award years establish credited service, not exact tour dates. Some service notes identify only company-sized elements. This is a sourced selection, not a complete movement log.'
    if not any(r['events'] for r in records):soup.select_one('.deployment-intro').string='No deployment with sufficiently established dates is plotted for this regiment. Read the assignment cards and service notes for its garrison, training and successor-unit history.'
    soup.select_one('.date-convention').string='Assignment ends are exclusive: the next period starts on that date. *Striped final bars mean last documented, with later status unverified through the page cutoff. Unknown intervals are not treated as inactive.'
    chronology=soup.select_one('.chronology')
    for _,b,title,text,source in notes:
        used_sources.add(source)
        chronology.append(fragment(f'<section class="battalion-evidence panel" id="battalion-{b}" data-unit="bn{b}"><p class="eyebrow">Service note · dates incomplete</p><h2>{escape(unit_label(n,b))} · {escape(title)}</h2><p>{escape(text)}</p><p>{link_source(source)}</p></section>'))
    research=soup.select_one('.research')
    if research:research.attrs.pop('aria-labelledby',None)
    if research is None:
        research=soup.new_tag('section',attrs={'class':'research panel'});soup.main.append(research)
    set_html(research,'''<h2>Sources and scope</h2><p>Army Center of Military History lineage certificates, regimental associations and secondary histories document assignments, operations and battalions. Exact lineage dates and approximate historical coverage are distinguished. Where the evidence stops, the page says so. A page cutoff is not a claim that every unit directory was current on that date.</p><p>Earlier battalions are covered by common regimental service; separately dated lineages and substantiated later battalions receive their own rows or notes. A unit graphic alone is not evidence of a battalion assignment. Reserve, training and inactive organizations are distinguished from active combat units.</p><ol class="sources">'''+''.join(f'<li id="source-{sid}"><a href="{escape(SOURCES[str(sid)]["url"],quote=True)}">{escape(SOURCES[str(sid)]["title"])}</a></li>' for sid in sorted(used_sources))+'''</ol><h3>Patch artwork</h3><p>Unmodified artwork from Wikimedia Commons; individual file pages identify the artist and license. Insignia represent the divisions, not regimental affiliation badges.</p><ul class="sources">'''+''.join(f'<li><a href="https://commons.wikimedia.org/wiki/File:{quote(PATCHES[c][1].replace(" ","_"))}">{escape(LABELS[c])} · file and credit</a>'+(' · <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a> (Noclador; unmodified)' if c=='a1' else ' · <a href="https://creativecommons.org/licenses/by/2.5/">CC BY 2.5</a> (Stannered; unmodified)' if c=='d45' else ' · public domain')+'</li>' for c in gallery)+'</ul>')
    # Prototype research subsections may sit outside .research.
    for element in soup.select('[id^="source-"]'):
        if element.find_parent(class_='research') is None:element.decompose()
    footer=soup.select_one('.footer-panel')
    nav=f'<a href="{n}RGT.html">{name} overview</a> · <a href="{n}RGT_battalions.html">Battalions</a> · <a href="infantry_timelines.html">All 200 timeline pages</a> · <a href="rgt_index.html">Regiment index</a>'
    if n>1:nav+=f' · <a href="{n-1}RGT_timeline.html">← {ordinal(n-1)} Infantry</a>'
    if n<200:nav+=f' · <a href="{n+1}RGT_timeline.html">{ordinal(n+1)} Infantry →</a>'
    set_html(footer,'<nav aria-label="Timeline series">'+nav+'</nav>')
    (HERE/f'{n}RGT_timeline.html').write_text(str(soup)+'\n',encoding='utf-8')
    return len(records),sum(len(r['events']) for r in records),len(notes)

def link_series():
    # Small string insertions preserve formatting in the established pages.
    for n in range(1,201):
        timeline=HERE/f'{n}RGT_timeline.html'
        content=timeline.read_text(encoding='utf-8')
        content=content.replace('All 100 timeline pages','All 200 timeline pages').replace('Infantry numbers 1\u2013100','Infantry numbers 1\u2013200')
        content=content.replace('All 60 timelines','All 200 timeline pages').replace('Regiments 1\u201360','Infantry numbers 1\u2013100').replace('All 30 timelines','All 200 timeline pages').replace('Regiments 1–30','Infantry numbers 1–200')
        if n==100 and 'href="101RGT_timeline.html"' not in content:
            content=content.replace('<a href="99RGT_timeline.html">\u2190 99th Infantry</a>', '<a href="99RGT_timeline.html">\u2190 99th Infantry</a> \u00b7 <a href="101RGT_timeline.html">101st Infantry \u2192</a>')
        if n==60 and 'href="61RGT_timeline.html"' not in content:
            content=content.replace('<a href="59RGT_timeline.html">\u2190 59th Infantry</a>', '<a href="59RGT_timeline.html">\u2190 59th Infantry</a> \u00b7 <a href="61RGT_timeline.html">61st Infantry \u2192</a>')
        if n==30 and 'href="31RGT_timeline.html"' not in content:
            content=content.replace('<a href="29RGT_timeline.html">← 29th Infantry</a>', '<a href="29RGT_timeline.html">← 29th Infantry</a> · <a href="31RGT_timeline.html">31st Infantry →</a>')
        if content!=timeline.read_text(encoding='utf-8'):timeline.write_text(content,encoding='utf-8')
        for suffix in ('','_battalions'):
            p=HERE/f'{n}RGT{suffix}.html';text=p.read_text(encoding='utf-8')
            if f'href="{n}RGT_timeline.html"' not in text:
                addition=f'<p class="text_column"><a href="{n}RGT_timeline.html">Division timeline, 1916–2026 · assignments, patches and deployments →</a></p>\n'
                if '<h3>See Also</h3>' in text:text=text.replace('<h3>See Also</h3>',addition+'<h3>See Also</h3>',1)
                else:text=re.sub(r'(<h2[^>]*>.*?</h2>)',r'\1\n'+addition,text,count=1,flags=re.S)
                p.write_text(text,encoding='utf-8')
    # The prototype remains hand-edited; add only the series navigation.
    p=HERE/'26RGT_timeline.html';text=p.read_text(encoding='utf-8')
    if 'href="infantry_timelines.html"' not in text:
        text=text.replace('</footer>','<nav aria-label="Timeline series"><a href="25RGT_timeline.html">← 25th Infantry</a> · <a href="infantry_timelines.html">All 200 timeline pages</a> · <a href="27RGT_timeline.html">27th Infantry →</a></nav></footer>')
        p.write_text(text,encoding='utf-8')
    p=HERE/'rgt_index.html';text=p.read_text(encoding='utf-8')
    text=text.replace('Infantry numbers 1\u2013100','Infantry numbers 1\u2013200')
    text=text.replace('Regiments 1–30','Infantry numbers 1–200').replace('Regiments 1\u201360','Infantry numbers 1\u2013100')
    if 'href="infantry_timelines.html"' not in text:
        text=re.sub(r'(<h[12][^>]*>.*?</h[12]>)',r'\1\n<p><a href="infantry_timelines.html">Infantry division timelines · Infantry numbers 1–200</a></p>',text,count=1,flags=re.S)
    if text!=p.read_text(encoding='utf-8'):p.write_text(text,encoding='utf-8')

def index():
    cards=''.join(f'<a class="timeline-index-card" href="{n}RGT_timeline.html"><span class="eyebrow">1916–2026</span><h2>{ordinal(n)} Infantry{' numbering record' if is_numbering(n) else ' Regiment'}</h2><p>Assignments · Division patches · Service history</p><span>Explore timeline →</span></a>' for n in range(1,201))
    (HERE/'infantry_timelines.html').write_text(f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Infantry Division Timelines · Infantry numbers 1–200</title><meta name="description" content="Explore division assignments, battalions and deployments of the U.S. infantry numbers 1 through 200 from 1916 through 2026."><link rel="stylesheet" href="regiment-timeline.css"></head><body><a class="skip-link" href="#main">Skip to timelines</a><div class="site-shell"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../../../index.html">Home</a> / <a href="../modern.html">Modern Era</a> / <a href="rgt_index.html">Infantry Regiments</a> / Timelines</nav><header class="timeline-hero"><div><p class="eyebrow">U.S. Army · Infantry</p><h1>Infantry numbers 1–200.<br>A century of assignments.</h1><p class="hero-subtitle">Division timelines, 1916–2026</p><p class="hero-text">Follow each regiment into its separate battle groups and battalions, with division patches, selected deployments and linked sources.</p></div></header><main id="main"><section class="reading-note"><h2>Choose a regiment</h2><p>Each page uses the 26th Infantry timeline format. Numbers 92–100 are numbering records: no Regular Army infantry regiments were constituted under those numbers; separately numbered battalions are distinguished. Dated assignments, inactive intervals and incomplete service records remain distinct. Last-documented bars identify gaps in later verification. The 177th and 189th–192d pages flag unresolved regimental identities; similarly numbered brigades are separate organizations.</p></section><div class="timeline-index-grid">{cards}</div></main><footer class="footer-panel"><a href="rgt_index.html">Infantry Regiment Index</a> · <a href="../modern.html">Modern Era</a></footer></div></body></html>\n''',encoding='utf-8')

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--start',type=int,default=1)
    parser.add_argument('--end',type=int,default=200)
    args=parser.parse_args()
    assert 1<=args.start<=args.end<=200
    template=(HERE/'26RGT_timeline.html').read_text(encoding='utf-8')
    totals=[0,0,0]
    for n in range(args.start,args.end+1):
        if n==26:continue
        counts=build(n,template)
        totals=[a+b for a,b in zip(totals,counts)]
        print(n,counts)
    index();link_series()
    print('Generated requested range; preserved 26th. Periods, service markers, notes:',totals)
