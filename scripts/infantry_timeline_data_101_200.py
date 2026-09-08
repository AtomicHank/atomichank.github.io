"""Remaining site regiments. Approximate windows are evidence coverage, not orders.

Regimental histories are individually linked. Exact transitions supplement broad
wartime coverage; no battalion or current assignment is inferred from artwork.
"""
ROWS=[]
import json
from pathlib import Path
NOTES={}
EVIDENCE=[]
OPERATIONS=[]
UNIT_LABELS={}
PERIOD_NOTES={}
APPROXIMATE=set()
NUMBERING={177,189,190,191,192}
SOURCES={
5100:('https://history.army.mil/Unit-History/Lineage-and-Honors-Information/Infantry-Including-Rangers/','U.S. Army Center of Military History: infantry lineage directory'),
5101:('https://en.wikipedia.org/wiki/172nd_Cavalry_Regiment','Earlier 172d Infantry and its cavalry successor (Wikipedia; secondary)'),
5102:('https://en.wikipedia.org/wiki/172nd_Infantry_Regiment_(United_States,_1982%E2%80%93present)','172d Mountain Infantry, constituted in 1982 (Wikipedia; secondary)'),
5103:('https://www.southeastsun.com/news/article_1d16fd30-7a96-11e6-877a-4b0dd5d3da88.html','Southeast Sun: 131st Cavalry becomes 173d Infantry, September 2016'),
5104:('https://en.wikipedia.org/wiki/256th_Infantry_Brigade_Combat_Team','256th Infantry Brigade and its battalions (Wikipedia; secondary)'),
5105:('https://en.wikipedia.org/wiki/193rd_Glider_Infantry_Regiment_(United_States)','193d Glider Infantry history (Wikipedia; secondary)'),
5106:('https://en.wikipedia.org/wiki/194th_Glider_Infantry_Regiment_(United_States)','194th Glider Infantry history (Wikipedia; secondary)'),
5107:('https://history.nebraska.gov/wp-content/uploads/2017/12/doc_publications_NH1992Lost_Battalion.pdf','Nebraska History: Nebraska’s Lost Battalion, 1992'),
5108:('https://www.hlswilliwaw.com/aleutians/58th_infantry_regiment.htm','Aleutian veterans history: 198th Infantry and 206th Infantry Battalion'),
5109:('https://legislature.mi.gov/Home/GetObject?objectName=1999-mm-p0512-p0520','Michigan Manual, 1999: 177th Regiment, Regional Training Institute'),
5110:('https://www.army.mil/article/106404/192nd_infantry_brigade_discontinued','U.S. Army: 192d Infantry Brigade history and distinction from regiments'),
5111:('https://www.generalstaff.org/NAF/Pt_I_1941-1942/941uxib.pdf','George Nafziger: American Infantry Regiments, 1941–1945 (secondary compilation)'),
5112:('https://history.army.mil/Portals/143/LineageAndHonorsDocuments/InfantryIncludingRangers/108th%20Infantry%20Regiment.pdf?ver=N8MfcALj8-gwPdgvgvu8yw%3D%3D','U.S. Army: 108th Infantry lineage, 2014'),
}

def row(n,b,steps,sid=None):
    ROWS.append((n,b,sid or 1000+n,steps))

def replace(n,steps,sid=None):
    ROWS[:]=[r for r in ROWS if not(r[0]==n and r[1]==0)]
    row(n,0,steps,sid)

def event(n,b,years,title,note='',sid=None):
    OPERATIONS.append((n,b,years,title,note or 'Selected campaign service; year labels do not specify exact departure and return dates.',sid or 1000+n))

def evidence(n,b,text,sid=None):
    EVIDENCE.append((n,b,'Service and organization',text,sid or 1000+n))

# Year-level wartime affiliation. These windows are explicitly approximate in
# cards, chart labels and date-lookup results; they are not effective-date orders.
WW2={101:26,102:0,103:43,104:26,105:27,106:27,108:40,109:28,110:28,111:0,112:28,
113:0,114:44,115:29,116:29,117:30,118:0,119:30,120:30,121:8,123:33,124:31,
125:0,126:32,127:32,128:32,129:37,130:33,131:0,132:23,133:34,134:35,135:34,
136:33,137:35,138:0,139:0,140:0,141:36,142:36,143:36,144:0,145:37,147:0,
148:37,149:38,150:0,151:38,152:38,153:0,155:31,156:0,157:45,158:0,160:40,
161:25,162:41,163:41,164:23,165:27,167:31,168:34,169:43,174:0,175:29,
179:45,180:45,181:0,182:23,184:7,185:40,186:41}
EUROPE={101,104,109,110,112,114,115,116,117,119,120,121,133,134,135,137,141,142,143,157,168,175,179,180}
PACIFIC={103,105,106,108,123,124,126,127,128,129,130,132,136,145,148,149,151,152,155,158,160,161,162,163,164,165,167,169,182,184,185,186}
for n in range(101,201):
    steps=['1916-01-01 unk']
    if n<=168:
        div=26+(n-101)//4
        steps += [f'1918-01-01 d{div}','1919-01-01 unk']
        APPROXIMATE.add((n,0,'1918-01-01'))
        event(n,0,'1918','France · World War I','Includes combat or depot/replacement service as described in the regimental history; not every regiment fought as an intact formation.')
    if n in WW2:
        code='d'+str(WW2[n]) if WW2[n] else 'ind'
        end='1945-05-09' if n in EUROPE else '1945-08-15'
        steps += ['1944-01-01 '+code,end+' unk']
        APPROXIMATE.add((n,0,'1944-01-01'))
        if n in EUROPE:event(n,0,'1944-1945','European theater · World War II')
        elif n in PACIFIC:event(n,0,'1944-1945','Pacific theater · World War II')
    row(n,0,';'.join(steps),5100 if n in NUMBERING else None)
    NOTES[n]='Approximate wartime windows identify documented affiliations within the labeled years. Their boundaries are coverage limits, not assignment or inactivation orders. Unverified intervals remain visible; common regimental service does not establish the later assignments of each battalion.'

# Reviewed effective dates and branch changes replace approximate coverage.
replace(102,'1916-01-01 unk;1917-08-22 d26;1919-04-29 inactive;1921-11-25 i_d43;1922-10-20 d43;1942-02-19 ind;1945-04-10 inactive;1946-01-01 unk;1959-05-01 end')
row(102,2,'1945-04-10 ind;1946-06-30 inactive')
evidence(102,1,'Joined the 86th Infantry Brigade during its 2006 reorganization. Afghanistan deployments included 2006 and 2010; the brigade relationship is distinct from temporary operational command.')
replace(104,'1916-01-01 unk;1918-01-01 d26;1919-04-29 inactive;1921-09-30 d26;1945-12-29 inactive;1946-11-29 unk;1948-01-01 d26;1963-03-01 end')
row(104,1,'1963-03-01 d26;1992-09-30 unk;1995-10-01 d29;2005-12-01 converted')
row(104,2,'1963-03-01 d26;1992-09-30 merged')
replace(105,'1916-01-01 unk;1918-01-01 d27;1919-04-01 inactive;1920-12-30 i_d27;1921-06-01 d27;1945-12-12 inactive;1947-03-04 unk')
evidence(105,1,'The history identifies 1st Battalion in the 27th Infantry Brigade in 2001; an exact preceding assignment sequence is not established here.')
replace(107,'1916-01-01 unk;1918-01-01 d27;1919-04-02 inactive;1921-01-01 unk;1923-01-01 d27;1940-01-01 unk;1941-01-01 converted;1946-01-01 unk;1948-01-01 ind;1957-01-01 unk;1958-01-01 d42;1959-01-01 unk')
NOTES[107]+=' World War II service was as coast/antiaircraft artillery. The infantry battalion was deactivated in 1993; later support-group service is not an infantry division assignment.'
replace(108,'1916-01-01 unk;1917-10-01 d27;1919-03-31 inactive;1920-04-24 unk;1921-11-17 d27;1942-09-01 d40;1946-04-07 i_d40;1947-05-17 i_d27;1947-07-23 d27;1955-02-01 end',5112)
for b in ('aib108','aib175'):row(108,b,'1955-02-01 a27;1959-03-16 end',5112)
row(108,1,'1959-03-16 a27;1968-02-01 a50;1975-04-01 d42;1986-04-01 b27;2005-09-01 inactive',5112)
row(108,2,'1959-03-16 a27;1968-02-01 inactive;1971-12-01 d42;1986-04-01 b27;2005-09-01 b27',5112)
row(108,3,'1986-04-01 b27;1996-09-01 inactive',5112)
replace(109,'1916-01-01 unk;1917-10-11 d28;1919-01-01 unk;1921-04-01 d28;1945-10-22 inactive;1946-12-16 d28;1959-06-01 end')
row(109,1,'1959-06-01 d28;2007-09-01 d28')
row(109,2,'1963-04-01 d28;1992-03-01 converted')
row(109,3,'1964-03-24 ind;1968-02-17 inactive;1975-04-01 d28;1995-10-01 converted')
row(110,1,'1959-06-01 d28')
row(113,2,'1991-09-01 a50;1993-09-01 d42')
for b in (1,2):row(114,b,'1959-03-01 a50;1968-02-01 '+('a50' if b==1 else 'inactive')+';1975-07-01 a50;1991-09-01 '+('a50;1993-09-01 d42' if b==1 else 'inactive'))
replace(119,'1916-01-01 unk;1917-09-12 d30;1919-04-17 inactive;1921-11-08 merged;1942-08-24 i_d30;1942-09-07 d30;1945-11-24 inactive;1947-07-08 d30;1959-04-01 end')
for b in (1,2):row(119,b,'1959-04-01 d30;1963-03-10 end')
for b in (4,5,6):row(119,b,'1963-03-10 d30;1968-01-01 inactive')
row(119,1,'1968-01-01 d30;1974-01-01 unk;1975-01-01 b30;2004-01-01 unk;2005-01-01 inactive')
evidence(120,1,'The combined-arms battalion deployed with the 30th Brigade to Iraq in 2004–2005 and 2009–2010. Operational control by a deployed division does not itself establish a permanent assignment.')
for b in (1,2):row(121,b,'1959-01-01 unk;1960-01-01 a48;1968-01-01 unk;1969-01-01 d30;1973-11-30 b48')
evidence(121,3,'The regimental history documents a 3d Battalion in the modern Georgia National Guard, including domestic service in 2020.')
replace(122,'1916-01-01 unk;1918-01-01 d31;1919-01-01 unk;1939-07-01 converted;1947-01-01 unk;1948-01-01 d48;1955-01-01 unk;1956-01-01 training_ww2')
NOTES[122]+=' The 1939 conversion produced field and coast artillery organizations. The postwar infantry served in the 48th Division before later training-institute service.'
for b in (1,2,3):row(127,b,'1959-02-15 d32;1963-04-01 d32;1968-01-01 unk')
row(128,2,'2001-09-01 unk;2001-10-01 b32;2007-09-01 converted')
for b in (1,2):row(136,b,'1959-02-22 d47;1963-04-01 d47')
for b in (1,2):row(137,b,'1959-05-01 d35;1963-04-01 d35;1967-12-15 unk;1976-02-01 b69;1984-08-25 d35;1992-09-01 '+('inactive' if b==1 else 'd35;2020-10-17 converted'))
evidence(137,3,'The history records a 3d Battalion in the postwar reorganization; it inactivated on 1 February 1976.')
replace(150,'1916-01-01 unk;1917-09-19 d38;1919-01-01 unk;1941-01-01 d38;1942-03-01 ind;1946-02-01 inactive;1947-01-01 unk')
NOTES[150]+=' Later cavalry service is a branch conversion, not a continuous infantry-regiment division assignment.'
replace(154,'1916-01-01 unk;1918-01-01 d39;1919-01-01 unk;1942-09-20 d31;1944-04-05 merged')
NOTES[154]+=' The World War II 154th was disbanded in April 1944; its personnel and equipment filled the reactivated 124th Infantry.'
replace(157,'1916-01-01 unk;1918-01-01 d40;1919-01-01 unk;1944-01-01 d45;1945-12-03 inactive;1946-05-10 ind;1947-01-08 ind;1955-08-01 converted')
NOTES[157]+=' The 1955 conversion produced artillery organizations. Later infantry service requires its own battalion history.'
replace(159,'1916-01-01 unk;1918-01-01 d40;1919-01-01 unk;1941-09-29 d7;1943-08-23 ind;1945-03-01 unk;1945-04-01 attached106;1945-05-09 unk')
event(159,0,'1943','Aleutians')
event(159,0,'1945','Europe · attached to 106th Division','The 106th relationship was an attachment, not a documented permanent assignment.')
for b in (1,2):row(159,b,'1974-01-01 unk;1974-02-01 d40;'+('1976-01-01 unk;1976-02-01 end' if b==1 else '2000-10-01 unk;2000-11-01 end'))
for b in (1,2,3):row(160,b,'1968-01-29 b40;1974-01-13 d40;1985-08-01 '+('inactive' if b==1 else 'd40'))
row(160,4,'1968-01-29 armbrig40;1974-01-13 d40;1985-08-01 d40')
evidence(161,1,'Served with the 81st Infantry Brigade. The history records Iraq service in 2004–2005 and 2008–2009.')
evidence(161,3,'The 3d Battalion was deactivated in the 1 October 1998 regimental reorganization.')
replace(164,'1916-01-01 unk;1918-01-01 d41;1919-01-01 unk;1941-02-10 d34;1941-12-08 ind;1942-05-27 d23;1945-11-24 inactive;1946-06-10 i_d47;1947-05-01 unk')
replace(166,'1916-01-01 unk;1918-01-01 d42;1919-01-01 unk;1943-08-20 training_ww2;1944-01-22 inactive;1946-11-11 d37;1959-09-01 end')
row(166,1,'1959-09-01 d37;1968-02-15 unk;1977-03-01 b73;1992-09-01 merged')
row(166,2,'1943-09-01 training_ww2;1944-02-22 inactive')
row(166,3,'1944-01-22 training_ww2;1945-02-12 inactive')
row(168,1,'1959-05-01 d34;1963-03-01 ind;1968-01-01 d47;1991-02-10 d34')
replace(170,'1916-01-01 unk;1922-10-20 d43;1924-01-01 unk',1102)
NOTES[170]='The 170th was the interwar designation of Connecticut’s later 102d Infantry. See the 102d timeline for its continuing lineage; this number is not the separate 170th Infantry Brigade.'
replace(171,'1916-01-01 unk;1921-11-22 d43;1921-12-31 renamed103',1103)
NOTES[171]='Maine’s 171st Infantry was redesignated the 103d Infantry on 31 December 1921. Its subsequent wars and division assignments belong on the 103d page.'
replace(172,'1916-01-01 unk;1944-01-01 d43;1945-08-15 unk;1964-01-01 unk;1965-01-01 converted',5101)
row(172,'mountain','1982-09-01 ind;1983-04-01 ind;1983-12-01 end',5102)
row(172,3,'1983-12-01 ind;2006-10-01 unk;2006-11-01 b86',5102)
UNIT_LABELS[172,'mountain']='72d / 172d Mountain Infantry · Separate 1982 lineage'
NOTES[172]='The older 172d Infantry, later armor/cavalry, and the mountain unit constituted in 1982 are separate lineages. The modern mountain regiment was first called the 72d Infantry. Its 3d Battalion receives a separate row.'
event(172,0,'1944-1945','Pacific theater','Earlier regiment’s wartime service with the 43d Division.',5101)
replace(173,'1916-01-01 priorbranch;2016-09-11 end',5103)
row(173,1,'2016-09-11 b256',5103)
NOTES[173]='The 1st Battalion was converted from 1st Squadron, 131st Cavalry, in September 2016. The 173d Infantry Regiment and the 173d Airborne Brigade are different organizations.'
evidence(173,1,'The battalion serves in the 256th Infantry Brigade Combat Team. This brigade relationship does not imply assignment to the similarly numbered airborne brigade.',5104)
replace(174,'1916-01-01 unk;1940-09-16 d44;1943-01-27 ind;1944-04-01 training_ww2;1945-09-27 inactive;1947-04-15 d27;1955-02-01 converted')
replace(176,'1916-01-01 unk;1941-01-01 d29;1942-01-01 unk;1943-01-01 ind;1944-07-10 inactive;1946-11-20 end')
row(176,3,'1946-11-20 unk;1959-06-01 end')
row(176,1,'1959-06-01 unk;1963-03-22 converted')
NOTES[176]+=' The 1st Battle Group became the 276th Engineer Battalion in March 1963.'
for b in (1,2):row(179,b,'1959-05-01 d45;1963-04-01 d45;1968-02-01 '+('ind' if b==1 else 'inactive'))
row(180,1,'1977-04-01 b45;2007-09-01 b45;2008-12-01 converted')
row(180,2,'1977-04-01 ind;2007-09-01 inactive')
replace(181,'1916-01-01 unk;1921-11-30 d26;1942-01-27 ind;1945-01-01 unk;1947-01-01 unk')
replace(183,'1916-01-01 unk;1922-03-09 d29;1929-02-22 renamed1;1941-01-01 renamed176')
NOTES[183]='Virginia’s 183d Infantry was renamed the 1st Infantry in 1929 and the 176th Infantry in 1941. Later RSTA cavalry service is identified as cavalry, not a second infantry regiment with invented battalions.'
row(183,'cavalry','2006-02-11 priorbranch',1183)
UNIT_LABELS[183,'cavalry']='2d Squadron, 183d Cavalry · Cavalry organization'
replace(184,'1916-01-01 unk;1943-01-01 unk;1943-08-23 d7;1946-01-20 inactive;1946-08-05 i_d49;1947-01-01 unk')
replace(187,'1916-01-01 notformed;1942-11-12 inactive;1943-02-25 ab11;1950-08-01 unk;1950-09-01 ind;1957-03-01 end')
NOTES[187]='The regiment’s airborne combat team served separately in Korea. Later battalions had different assignments; the Panama battalions and the 101st Airborne battalions must not be treated as a single uninterrupted regimental assignment.'
for b in (1,2):row(187,b,'1983-10-01 unk;1983-11-01 b193;1987-01-01 unk;1988-01-01 ab101')
row(187,3,'1968-01-01 ab101')
row(187,4,'1983-10-01 unk;1983-11-01 ab101;1987-01-01 unk;1988-01-01 merged')
row(187,5,'1984-11-21 ab101;1987-01-01 unk;1988-01-01 merged')
event(187,0,'1944-1945','Leyte and Luzon')
event(187,0,'1950-1953','Korean War · Airborne regimental combat team')
event(187,3,'1968-1969','Vietnam')
for b in (1,2,3):event(187,b,'1990-1991','Saudi Arabia and Iraq')
event(187,4,'1984-1985','Sinai · Multinational Force and Observers')
replace(188,'1916-01-01 notformed;1942-11-12 inactive;1943-02-25 ab11;1945-08-15 unk')
event(188,0,'1944-1945','Leyte and Luzon')
for n,sid in ((193,5105),(194,5106)):
    replace(n,'1916-01-01 notformed;1942-12-16 inactive;1943-04-15 ab17;1945-01-01 ab17;1945-03-01 '+('merged' if n==193 else 'ab17;1945-05-09 unk'),sid)
    event(n,0,'1944-1945','European theater · Glider infantry','Service with the 17th Airborne Division.',sid)
    NOTES[n]='This page follows the glider infantry regiment, not the similarly numbered brigade. The 193d was absorbed into the 194th in March 1945.'
event(194,0,'1945','Operation Varsity · Rhine crossing','Glider assault in March 1945.',5106)
replace(195,'1916-01-01 priorbranch;1947-01-01 unk;1949-01-01 unk;1954-12-01 converted;1997-06-20 training_ww2')
NOTES[195]='New Hampshire’s infantry regiment was organized in 1947–1948, converted into artillery organizations in December 1954, and later perpetuated by a Regional Training Institute. The sources do not establish a maneuver-division assignment for its infantry years.'
replace(196,'1916-01-01 unk;1917-10-03 priorbranch;1946-06-24 inactive;1947-09-01 ind;1956-09-14 inactive;1986-01-01 unk;1987-01-01 training_ww2')
NOTES[196]='The 196th Infantry was a separate regimental combat team after World War II. Its earlier lineage includes artillery and engineers. The 196th Regiment later became a Regional Training Institute.'
replace(197,'1916-01-01 unk;1943-01-29 ind;1944-01-01 unk',5111)
row(197,2,'1943-01-29 ind;1944-01-01 unk',5107)
event(197,2,'1943','Aleutian Islands','Former 2d Battalion, 134th Infantry; the later reorganization is documented in Nebraska History.',5107)
NOTES[197]='A short-lived separate regiment in Alaska; it is not the 197th Infantry Brigade. The later battalion chronology is incomplete here.'
replace(198,'1916-01-01 unk;1943-02-09 end',5108)
row(198,1,'1943-02-09 ind;1944-01-26 renamed206',5108)
event(198,1,'1943','Aleutian Islands','The 1st Battalion, formed from the 71st Infantry, garrisoned the Aleutians before becoming the 206th Infantry Battalion.',5108)
NOTES[198]='The Alaska infantry organization is distinct from the 198th Infantry Brigade and Delaware’s coast-artillery/signal lineages. The 1st Battalion became the 206th Infantry Battalion in January 1944.'
replace(199,'1916-01-01 notformed;1952-05-01 unk;1960-08-04 inactive;1997-07-03 training_ww2')
NOTES[199]='Louisiana’s regiment served as infantry during the 1950s and returned in 1997 as a training regiment. It is not the separate 199th Infantry Brigade that fought in Vietnam.'
replace(200,'1916-01-01 priorbranch;2005-09-01 end',5100)
row(200,1,'2005-09-01 b26;2008-09-01 ind',5100)
row(200,2,'2005-09-01 b58;2008-09-01 inactive',5100)
NOTES[200]='The modern infantry designation dates from the 2005 conversion of New Mexico air-defense artillery. Earlier branch service and inherited campaign honors are not represented as deployments by a 200th Infantry Regiment. The Army’s 2024 certificate is the governing lineage source.'

for n in NUMBERING:
    NOTES[n]='The site contains this numbered placeholder, but a matching U.S. infantry-regiment lineage for 1916–2026 has not been established from the reviewed records. A similarly numbered brigade, a Civil War state regiment or a training institute is not assumed to be the same unit.'
evidence(177,'rti','The Michigan Manual identifies the 177th Regiment, Regional Training Institute, in 1999. This is a training organization, not evidence of a continuously assigned 177th Infantry Regiment.',5109)
UNIT_LABELS[177,'rti']='177th Regiment · Regional Training Institute'
for n in (189,190,191,192):evidence(n,'scope','A brigade with this number must not be used to populate the division history of an infantry regiment. No regimental battalions or deployments are inferred from the site’s existing graphics.',5110 if n in (191,192) else 5100)
for n in (189,190,191,192):UNIT_LABELS[n,'scope']='Numbering and organizational scope'

# Additional precisely identified service. Evidence notes are used when dates
# establish deployments but do not establish a full divisional sequence.
for n,b,text in [
(101,1,'The last active battalion was consolidated with 1st Battalion, 182d Infantry, on 1 September 1992.'),
(112,1,'The Pennsylvania history identifies this battalion with the 56th Stryker Brigade, 28th Division, including domestic service in 2020.'),
(112,2,'The regiment maintains a separate 2d Battalion; its later service must be distinguished from the 1st Battalion’s Stryker organization.'),
(115,1,'Company B deployed to Iraq in 2005–2006 with Georgia’s 48th Brigade. The temporary attachment did not turn the entire regiment into a Georgia unit.'),
(116,1,'The regimental history documents this battalion in the 116th Brigade and overseas service after 2001.'),
(116,2,'A separately organized battalion of the regiment; later cavalry conversions should not be treated as continuous infantry service.'),
(116,3,'The regimental history distinguishes a 3d Battalion and its overseas service from the other battalions.'),
(118,1,'The modern regiment includes 1st Battalion; deployments included security missions outside the United States.'),
(118,4,'Deployed to Kuwait during April–December 2012. Later company detachments served in Iraq and Syria in 2019–2020.'),
(124,1,'A documented battalion of Florida’s regiment; the regimental history covers postwar reorganizations and overseas service.'),
(124,2,'A separately documented battalion of Florida’s regiment; an exact independent division chronology is not inferred here.'),
(126,1,'The lineage passed through armor and cavalry roles before returning to infantry in 2016. Those branch changes are not infantry division transfers.'),
(148,1,'Deployed to Kosovo in 2004–2005 and Afghanistan in 2011–2012; brigade attachments must be distinguished from division assignment.'),
(155,1,'The combined-arms battalion serves with the 155th Armored Brigade. Iraq deployments included 2005–2006 and 2009–2010.'),
(162,2,'Company C provided security in Saudi Arabia in 1999–2000. This company mission is not a deployment of the entire regiment.'),
(167,1,'Company-sized elements deployed to Iraq in 2005 and 2007; the battalion deployed to Afghanistan in 2012.'),
(175,1,'Postwar service passed through the 58th Brigade and the 28th and 29th Divisions. By 1995 it was the regiment’s single battalion.'),
(182,1,'The 1st Battalion was assigned to the 27th Infantry Brigade Combat Team on 1 October 2016, following earlier training alignment.'),
(185,1,'The battalion redesignated from 185th Armor in February 2016 inherits that armor lineage; it is distinct from the earlier 185th Infantry battalion.')]:evidence(n,b,text)

for n,b,years,title in [(108,2,'2012','Afghanistan'),(109,1,'2012-2013','Kuwait'),(119,1,'2004','Iraq'),(121,2,'2005-2006','Iraq'),(137,2,'2010-2011','Djibouti'),(168,1,'2004-2005','Afghanistan'),(168,1,'2010-2011','Afghanistan'),(180,1,'2007-2008','Afghanistan')]:event(n,b,years,title)

# Further dated battalion reorganizations, retained separately from common service.
for b in (1,2):row(130,b,'1959-03-01 d33;1963-04-01 d33;1968-02-01 '+('inactive' if b==1 else 'd47;1991-02-10 d34;1996-10-01 d35;2006-09-01 b33'))
row(130,3,'1963-04-01 d33;1968-02-01 d47;1991-02-10 d34;1996-10-01 inactive')
row(131,1,'1959-03-01 d33;1963-04-01 d33;1965-12-01 ind;1968-02-01 b33')
for b in (1,2):row(133,b,'1959-05-01 d34;1963-03-01 ind;1968-01-01 d47;1991-02-10 d34;1997-09-01 '+('d34' if b==1 else 'inactive'))
row(133,3,'1964-03-01 ind;1968-01-01 inactive')
for b in (1,2):row(134,b,'1959-05-01 d34;1963-04-01 b67')
for b in (1,2):row(135,b,'1959-02-22 d47;1991-02-10 d34;1992-09-01 '+('inactive' if b==1 else 'd34'))
for b in (3,4):row(135,b,('1959-02-22' if b==3 else '1963-04-01')+' d47;1968-02-01 inactive')
for b in (1,2,3):row(141,b,'1992-09-01 a49;1994-09-01 '+('inactive' if b==2 else 'a49;2004-05-01 d36'))
evidence(143,1,'Reactivated as an airborne battalion in 2010. Its association with the 173d Airborne Brigade began under the Associated Unit Pilot; later release back to Texas control is not described as an assignment to an airborne division.')
row(145,1,'2007-09-01 unk')
PERIOD_NOTES[145,1,'2007-09-01']='The combined-arms battalion was redesignated from 1st Battalion, 107th Cavalry. A precise later division assignment is not inferred from the regimental title.'
for b in (1,2,3):row(156,b,'1959-07-01 d39;1967-12-01 b256;1977-03-01 '+('inactive' if b==1 else 'b256'))
row(156,4,'1963-05-01 d39;1967-12-01 inactive;1991-07-01 ind;1993-02-01 inactive')
for b in (1,2):row(158,b,'1959-03-01 ind;1967-12-10 converted')
row(158,3,'1963-03-01 ind;1967-12-10 converted')
for b in (1,2):row(124,b,'1963-02-15 b53;1964-03-01 '+('ind' if b==1 else 'armbrig53')+';1968-01-20 b53')
row(124,3,'1968-01-20 b53;2006-01-01 unk;2008-01-01 converted')
row(151,'D','1967-12-01 ind;1977-03-01 converted;1989-10-01 ind')
event(151,'D','1969','Vietnam · Ranger company','Company D served independently; the entire regiment did not deploy to Vietnam.')
evidence(152,2,'Headquarters elements served in Ramadi in 2006–2007, attached successively to brigades of the 1st Armored and 3d Infantry Divisions. These were operational attachments.')
row(138,1,'2010-09-01 unk')
PERIOD_NOTES[138,1,'2010-09-01']='Redesignated from the 135th Support Detachment. This dated infantry conversion does not establish a precise division assignment.'

SOURCES[5113]=('https://history.army.mil/Portals/143/LineageAndHonorsDocuments/InfantryIncludingRangers/200th%20Infantry%20Regiment.pdf?ver=TjQCpxzXa694GD8rF6srVw%3D%3D','U.S. Army: 200th Infantry lineage, 23 September 2024')
ROWS[:]=[(n,b,5113 if n==200 else sid,steps) for n,b,sid,steps in ROWS]
event(200,2,'2007-2008','Iraq · Company C','The Army certificate credits Company C, not every element of the regiment, with Iraq service in these years.',5113)

# Exact effective dates take precedence; the remaining deliberately rounded
# windows retain conspicuous approximation labels in the generated page.
SOURCES.update({int(k):tuple(v) for k,v in json.loads(Path(__file__).with_name('infantry_timeline_sources_101_200.json').read_text(encoding='utf-8')).items()})
ROWS[:]=[r for r in ROWS if not(r[0]==187 and r[1] in (0,1,2,3))]
row(187,0,'1916-01-01 notformed;1942-11-12 inactive;1943-02-25 ab11;1951-02-01 ind;1956-07-01 ab101;1957-04-25 end',6187)
row(187,1,'1957-03-01 ab11;1958-07-01 d24;1959-02-08 ab82;1964-05-25 aa11;1965-06-30 inactive;1983-10-01 b193;1987-05-01 inactive;1987-09-16 ab101;2004-09-16 ab101',61871)
row(187,2,'1957-04-25 ab101;1964-02-01 ind;1964-02-03 inactive;1983-10-01 b193;1987-07-10 inactive;1987-09-16 ab101',61872)
row(187,3,'1957-04-25 inactive;1963-02-07 aa11;1964-02-01 ab101;2004-09-16 ab101',61873)
for b in (1,2):row(151,b,'1977-03-01 d38;1994-09-01 '+('b76' if b==1 else 'd38;2007-09-01 ind'),6151)
for b in (1,2):row(153,b,'1959-06-01 d39;1967-12-01 b39;2005-09-01 b39',6153)
row(153,3,'1967-12-01 b39;2005-09-01 converted',6153)
row(185,'modern','2016-02-02 b81',6185)
UNIT_LABELS[185,'modern']='1st Battalion, 185th Infantry · Former armor lineage'
PERIOD_NOTES[185,'modern','2016-02-02']='The battalion’s conversion from armor established a separate infantry lineage under the 81st Brigade. It is not a continuation of the earlier 185th Infantry.'
SOURCES.update({
5114:('https://www.army.mil/article/55106/ohio_michigan_prep_for_afghanistan','U.S. Army: 1-125 Infantry and 37th Brigade, April 2011'),
5115:('https://www.army.mil/article/277763/decades_of_influence_red_arrow_transformed_by_joint_readiness_training_exercise','U.S. Army: 3-126 Infantry and 32d Brigade, 2024'),
5116:('https://www.army.mil/article-amp/21903/illinois_families_benefit_from_web_cast_from_afghanistan','U.S. Army: 178th Infantry with 33d Brigade in Afghanistan, May 2009'),
5117:('https://history.army.mil/Portals/143/LineageAndHonorsDocuments/InfantryIncludingRangers/157th%20Infantry%20Regiment.pdf?ver=gU-2PtrBpeR2pt3HVUwMag%3D%3D','U.S. Army: newly constituted 157th Infantry lineage, 2012'),
5118:('https://en.wikipedia.org/wiki/35th_Infantry_Division_(United_States)','35th Division order of battle, including the World War I 139th Infantry (Wikipedia; secondary)'),
})
row(125,1,'2011-01-01 b37',5114)
row(126,3,'2024-01-01 b32',5115)
EVIDENCE[:]=[e for e in EVIDENCE if not(e[0]==126 and e[1]==1)]
NOTES[126]+=' The Army’s 2024 training report identifies the 3d Battalion with the 32d Brigade. The displayed year window brackets that report, not a transfer order.'
replace(178,'1916-01-01 unk;1940-10-06 converted;1947-01-01 unk')
row(178,1,'2009-05-29 b33',5116)
PERIOD_NOTES[178,1,'2009-05-29']='An Army report confirms the battalion with the 33d Infantry Brigade in Afghanistan. This is a dated observation, not its initial assignment date.'
event(178,1,'2009','Afghanistan','Security and provincial reconstruction support with the 33d Brigade.',5116)
row(157,'modern','2007-10-01 inactive;2008-09-01 end',5117)
row(157,1,'2008-09-01 unk',5117)
UNIT_LABELS[157,'modern']='157th Infantry · Separate 2007 organization'
NOTES[157]+=' The modern 157th was separately constituted in 2007 and organized with 1st Battalion in September 2008; inherited company honors do not create regimental continuity.'
replace(139,'1916-01-01 notformed;1954-10-28 d30;1959-01-01 unk')
row(139,'wwi','1918-01-01 d35;1919-01-01 unk',5118)
APPROXIMATE.add((139,'wwi','1918-01-01'))
OPERATIONS[:]=[e for e in OPERATIONS if e[0]!=139]
event(139,'wwi','1918','France','World War I regiment of the 35th Division; distinct from North Carolina’s 1954 organization.',5118)
NOTES[139]='The World War I 139th Infantry in the 35th Division and the North Carolina regiment constituted in 1954 in the 30th Division are distinct organizations. Their histories are not joined into a fictitious continuous assignment.'

# Deployment evidence establishes a battalion's presence, not an activation date
# or an organic division assignment. Keep these coverage rows explicitly unknown.
for n,b,start in [(102,1,2006),(115,1,2005),(118,4,2007),(120,1,2004),
                  (148,1,2004),(155,1,2005),(162,2,2004),(167,1,2005),
                  (144,3,2006),(186,1,2003)]:
    if not any(r[0]==n and r[1]==b for r in ROWS):
        row(n,b,f'{start}-01-01 unk')
        PERIOD_NOTES[n,b,f'{start}-01-01']='Documented deployment coverage begins in this year. The boundary is not an activation date; the organic division assignment remains unresolved.'
for n,b,years,title,note in [
    (102,1,'2006','Afghanistan','Companies supported provincial reconstruction teams.'),
    (102,1,'2010','Afghanistan','Task Force Iron Grey with the 86th Brigade.'),
    (115,1,'2005-2006','Iraq · Company B','Company B served with the 48th Brigade; this marker does not represent the whole battalion.'),
    (118,4,'2007-2008','Afghanistan','Service with the 218th Brigade.'),
    (118,4,'2012','Kuwait','Camp Buehring security and camp operations, April–December.'),
    (118,4,'2019','Kuwait','Deployed in October with the 30th Armored Brigade for Operation Spartan Shield.'),
    (120,1,'2004-2005','Iraq','30th Brigade under the operational command of the 1st Infantry Division; not a permanent organic transfer.'),
    (120,1,'2009-2010','Iraq','30th Brigade under the operational command of the 1st Cavalry Division.'),
    (148,1,'2004-2005','Kosovo','KFOR peacekeeping, August 2004–February 2005.'),
    (148,1,'2008','Kuwait and Iraq','Convoy security and escort operations; returned in December.'),
    (148,1,'2011-2012','Afghanistan','Operation Enduring Freedom, Regional Command North.'),
    (148,1,'2017','Jordan','Nine-month deployment including training with Jordanian forces.'),
    (155,1,'2005-2006','Iraq','Task Force Rifles.'),
    (155,1,'2009-2010','Iraq','Second documented Iraq tour.'),
    (162,2,'2004-2005','Iraq','Operation Iraqi Freedom.'),
    (162,2,'2009-2010','Iraq','Operation Iraqi Freedom.'),
    (162,2,'2014-2015','Afghanistan','June 2014–May 2015.'),
    (167,1,'2005','Iraq · Company A','Company A mobilized with additional soldiers from Companies B and C.'),
    (167,1,'2007','Iraq · Company C','Convoy security from Kuwait to bases throughout Iraq.'),
    (167,1,'2012','Afghanistan','Security support for NATO Training Mission–Afghanistan.'),
    (144,3,'2006-2007','Iraq · Company B','Company-level combat deployment.'),
    (144,3,'2012','Afghanistan','Task Force Bowie.'),
    (144,3,'2017-2018','Horn of Africa','Camp Lemonnier, Djibouti; October 2017–July 2018.'),
    (186,1,'2003','Iraq · Detached company','Roseburg company attached to 2d Battalion, 162d Infantry.'),
    (186,1,'2006','Afghanistan · Detached company','Medford company with Task Force Phoenix V.'),
    (186,1,'2009-2010','Iraq','Convoy security; returned in April 2010.'),
    (125,1,'2012','Afghanistan','Army unit commendation credits January–September 2012.')
]:event(n,b,years,title,note)

for n,b,sid,steps in ROWS:
    for step in steps.split(';'):
        start,code=step.split()
        if start.endswith('-01-01') and code not in ('unk','inactive','notformed','converted','priorbranch','merged'):
            APPROXIMATE.add((n,b,start))
        if (n,b,start) in APPROXIMATE:
            PERIOD_NOTES[n,b,start]='Approximate evidence window: the cited history records this wartime affiliation, but these displayed boundaries are not effective-date assignment orders. The date lookup identifies evidence within this window, not confirmed membership on each day.'
        if code in ('converted','priorbranch'):
            PERIOD_NOTES[n,b,start]='Lineage service in another branch or under a predecessor designation. This interval is not plotted as an infantry maneuver-division assignment.'
        if code=='merged':PERIOD_NOTES[n,b,start]='Consolidated, absorbed or redesignated into another organization. Follow the successor’s history rather than assuming continuing independent infantry service.'
