"""61-100 numbering extension; distinct organizations never imply shared lineage.

Unknown windows bracket month-only changes. A coverage boundary is not an
activation/inactivation date. Source and per-period notes preserve that distinction.
"""
import json
from pathlib import Path

SOURCES = {int(k): tuple(v) for k,v in json.loads(
    Path(__file__).with_name('infantry_timeline_sources_61_100.json').read_text(encoding='utf-8')).items()}
SOURCES.update({
401: ('https://history.army.mil/portals/143/Images/Publications/catalog/23-4.pdf', 'U.S. Army: Order of Battle of the United States Land Forces in the World War, vol. 3, part 2, divisions 11-20'),
402: ('https://en.wikipedia.org/wiki/Infantry_Branch_(United_States)', 'Infantry Branch numbering history (Wikipedia; secondary)'),
403: ('https://www.globalsecurity.org/military/agency/army/1-61in.htm', '1st Battalion, 61st Infantry history (GlobalSecurity; secondary)'),
404: ('https://www.army.mil/article-amp/291647/1st_battalion_61st_infantry_salutes_its_vietnam_veterans', 'U.S. Army: 1st Battalion, 61st Infantry, Vietnam veterans and training mission, April 2026'),
405: ('https://en.wikipedia.org/wiki/69th_Infantry_Regiment_(New_York)', '69th New York Infantry and the distinct Regular Army organizations (Wikipedia; secondary)'),
406: ('https://en.wikipedia.org/wiki/71st_New_York_Infantry_Regiment', '71st New York Infantry history (Wikipedia; secondary)'),
407: ('https://www.army.mil/ranger/heritage.html', 'U.S. Army: Ranger heritage and overseas operations'),
408: ('https://www.25thida.org/units/infantry/87th-infantry-regiment/', '25th Infantry Division Association: 87th Infantry battalion and company histories'),
409: ('https://www.army.mil/article/190321/warrior_transition_battalion_empowers_soldiers_to_heal_thrive', 'U.S. Army: 3d Battalion, 85th Infantry Warrior Transition Battalion, 2017'),
410: ('https://www.archives.gov/files/st-louis/pdf/infantry-regiment-index.pdf', 'National Archives: Infantry Regiment morning-report index, including the 91st Infantry in 1942'),
411: ('https://en.wikipedia.org/wiki/99th_Infantry_Battalion_(United_States)', '99th separate Infantry Battalion (Wikipedia; secondary)'),
412: ('https://www.100thbattalion.org/wp-content/uploads/100th-Infantry-Regiment_2.pg4-7.pdf', '100th Battalion, 442d Infantry: Army lineage certificate reproduced by the veterans association'),
413: ('https://dmna.ny.gov/pressroom/?id=1321477197', 'New York DMNA: 1st Battalion, 69th Infantry in the 27th Brigade, 42nd Division, November 2011'),
414: ('https://museum.dmna.ny.gov/unit-history/conflict/world-war-1-1914-1918/165th-infantry-regiment-69th-new-york', 'New York State Military Museum: 165th Infantry (69th New York) in World War I'),
415: ('https://en.wikipedia.org/wiki/100th_Infantry_Battalion_(United_States)', '100th Infantry Battalion and its operational attachments (Wikipedia; secondary)'),
416: ('https://www.generalstaff.org/NAF/Pt_I_1941-1942/941uxib.pdf', 'George Nafziger: American Infantry Regiments, 1941–1945 (compiled order of battle; secondary)'),
})

ROWS = [
(61,0,1061,'1916-01-01 notformed;1917-05-15 unk;1917-11-17 d5;1921-09-02 i_d5;1927-08-15 i_d8;1933-10-01 i_d5;1939-10-16 inactive;1944-11-11 disbanded;1950-08-10 i_d8;1950-08-17 d8;1956-09-01 inactive;1962-01-17 end'),
(61,1,403,'1962-01-17 inactive;1962-02-19 d5;1971-08-02 d4;1974-08-21 d5;1989-06-19 inactive;1993-06-13 training'),
(62,0,1062,'1916-01-01 notformed;1917-05-15 unk;1917-12-17 d8;1919-06-01 unk;1919-07-01 ind;1921-11-25 inactive;1922-07-31 disbanded;1942-08-31 i_a14;1942-11-15 a14;1943-09-20 end'),
(63,0,1063,'1916-01-01 notformed;1917-05-15 unk;1918-07-05 d11;1918-11-29 ind;1922-07-31 disbanded;1941-05-10 inactive;1941-06-01 d6;1949-01-10 inactive;1950-10-04 d6;1956-04-03 inactive'),
(64,0,1064,'1916-01-01 notformed;1917-05-15 unk;1917-11-16 d7;1922-07-31 disbanded;1941-07-18 inactive;1952-08-04 disbanded'),
(65,0,4124,'1916-01-01 ind;1950-09-22 d3;1954-11-03 ind;1954-12-02 d23;1956-04-10 inactive;1959-02-15 end'),
(65,1,4124,'1959-02-15 b92;1964-05-01 b92'),
(65,2,4124,'1978-09-01 b92;1992-09-01 inactive'),
(65,'E',4124,'1971-04-01 unk;1980-02-29 end'),
(66,0,1066,'1916-01-01 notformed;1943-07-10 i_d71;1943-07-15 d71;1946-04-05 unk;1946-04-10 i_d71;1953-02-25 end'),
(67,0,1067,'1916-01-01 notformed;1918-07-05 unk;1918-08-01 d9;1919-02-15 disbanded'),
(68,0,1068,'1916-01-01 notformed;1918-07-09 unk;1918-08-01 d9;1919-02-15 disbanded'),
(68,'tanks',1068,'1933-10-01 inactive;1940-01-01 ind;1940-07-15 end'),
(69,0,405,'1916-01-01 notformed;1918-07-09 i_d10;1918-08-10 d10;1919-02-13 disbanded'),
(69,'tanks',405,'1933-10-01 inactive;1944-11-11 disbanded'),
(69,'ny',405,'1916-01-01 unk;1917-08-05 d42;1919-05-07 inactive;1920-12-30 i_d44;1921-12-11 d44;1927-02-27 b93;1940-06-20 d27;1946-01-01 unk;2011-11-15 end'),
(69,1,413,'2011-11-15 d42'),
(70,0,1070,'1916-01-01 notformed;1918-07-09 i_d10;1918-08-10 d10;1919-02-13 disbanded'),
(71,0,1071,'1916-01-01 notformed;1918-07-09 unk;1918-09-01 d11;1919-02-03 disbanded'),
(71,'ny',406,'1916-01-01 unk;1940-09-16 d44;1946-01-01 unk'),
(74,0,1074,'1916-01-01 notformed;1918-07-09 unk;1918-08-01 d12;1919-01-31 disbanded;1941-07-18 inactive;1952-08-04 disbanded'),
(74,'rct',1074,'1944-11-11 notformed;1945-01-06 ind;1945-10-26 inactive;1954-10-08 ind;1956-09-16 inactive'),
(75,0,1075,'1916-01-01 notformed;1918-07-10 unk;1918-09-01 d13;1919-02-27 disbanded;1941-07-18 inactive;1952-08-04 disbanded'),
(75,'ranger',4125,'1943-10-03 ind;1945-07-01 inactive;1954-11-20 ind;1956-03-21 inactive;1969-01-01 end'),
(75,'ranger',4125,'1984-07-01 ind;1986-02-03 ind'),
(75,1,4126,'1969-02-01 ind;1971-10-25 inactive;1974-01-31 ind;1986-02-03 ind'),
(75,2,4127,'1969-02-01 ind;1972-08-15 inactive;1974-10-01 ind;1986-02-03 ind'),
(75,3,4128,'1969-02-01 ind;1971-03-15 inactive;1984-10-02 ind;1986-02-03 ind'),
(75,'stb',4130,'1969-02-01 ind;1971-08-25 inactive;2007-10-16 ind'),
(75,'mi',4129,'1969-02-01 ind;1971-08-31 inactive;2020-06-16 ind'),
(85,0,1085,'1916-01-01 notformed;1918-07-31 unk;1918-10-01 d18;1919-02-13 disbanded;1943-07-15 m10;1945-11-26 inactive;1948-06-18 i_m10;1948-07-01 m10;1957-07-01 inactive'),
(85,3,409,'2007-08-22 medical'),
(86,0,1086,'1916-01-01 notformed;1918-07-31 unk;1918-10-01 d18;1919-02-13 disbanded;1942-11-25 inactive;1942-12-12 unk;1943-05-02 ind;1943-07-15 m10;1945-11-27 inactive;1948-06-18 i_m10;1948-07-01 m10;1957-07-01 inactive'),
(87,0,4131,'1916-01-01 notformed;1941-11-15 ind;1944-02-22 m10;1945-11-21 inactive;1948-06-18 i_m10;1948-07-01 m10;1957-07-01 end'),
(87,1,4132,'1957-07-01 m10;1958-06-14 d2;1963-09-04 d8;1983-10-01 inactive;1987-05-02 m10;2004-09-16 m10'),
(87,2,4133,'1957-07-01 inactive;1963-01-25 i_d2;1963-02-15 d2;1963-09-04 d8;1966-05-01 inactive;1973-08-31 d8;1986-06-16 inactive;1988-05-02 m10;2004-09-16 m10'),
(87,3,1087,'1975-01-01 ar96;1994-09-15 inactive'),
(87,4,408,'1986-06-16 d25;1995-07-15 inactive'),
(87,5,408,'1987-05-01 b193;1994-07-15 ind;1999-09-15 inactive'),
(88,0,1088,'1916-01-01 notformed;1941-10-10 training_ww2;1942-05-01 unk;1942-06-01 ind;1943-04-01 unk;1943-05-01 abbrig1;1943-12-03 ab13;1945-03-01 disbanded'),
(89,0,1089,'1916-01-01 notformed;1918-08-01 unk;1918-09-01 d20;1919-02-28 ind;1919-03-01 unk;1919-04-01 disbanded'),
(89,3,1089,'1941-01-02 ind;1943-10-21 inactive'),
(89,'A',1089,'1941-01-02 ind;1943-11-19 inactive'),
(89,'L',1089,'1941-06-20 ind;1944-07-30 inactive'),
(90,0,1090,'1916-01-01 notformed;1918-08-31 unk;1918-10-01 d20;1919-02-28 ind;1919-03-13 unk;1919-03-23 disbanded;1943-07-10 i_m10;1943-07-15 m10;1944-02-13 unk;1944-02-23 training_ww2;1945-08-10 inactive'),
(91,0,416,'1916-01-01 unk;1942-03-10 ind;1942-03-11 unk'),
(99,'separate',411,'1942-07-01 unk;1942-08-01 ind;1945-11-02 inactive;1954-10-08 ind;1956-09-30 training_ww2;1958-03-24 inactive'),
(100,'separate',412,'1942-06-04 notformed;1942-06-12 ind;1946-08-15 inactive;1947-07-31 reserve;1959-05-29 reserve;1964-05-01 reserve'),
]

# The primary order of battle establishes these formations within a month.
# Exact dates are deliberately not inferred from their division HQ's dates.
for n,div,month,demob in [(72,11,9,'1919-01-17'),(73,12,7,'1919-01-18'),
    (76,13,8,'1919-01-12'),(77,14,8,'1919-01-17'),(78,14,8,'1919-01-17'),
    (79,15,9,'1919-01-01'),(80,15,9,'1919-01-01'),(81,16,9,'1919-01-17'),
    (82,16,9,'1919-01-17'),(83,17,8,'1919-01-07'),(84,17,8,'1919-01-07'),
    (87,19,9,'1919-01-19'),(88,19,9,'1919-01-19')]:
    b='wwi' if n in (87,88) else 0
    ROWS.append((n,b,401,f'1916-01-01 notformed;1918-{month:02}-01 unk;1918-{month+1:02}-01 d{div};{demob} unk;1920-01-01 disbanded'))

for n in range(92,101):
    ROWS.append((n,0,402,'1916-01-01 never'))
for n in (96,97,98):
    ROWS.append((n,'scouts',303,'1947-10-25 unk;1949-05-01 unk;1949-06-01 inactive;1951-10-10 disbanded'))
for n in (62,68,19):
    ROWS.append((62,'aib'+str(n),1062,'1943-09-20 a14;1945-05-09 end'))
for n in (266,267,268,269):
    ROWS.append((66,'aib'+str(n),1066,'1953-02-25 i_a13'))

UNIT_LABELS = {
(69,'ny'):'69th New York / 165th Infantry · Separate National Guard lineage',
(69,1):'1st Battalion, 69th New York Infantry',
(71,'ny'):'71st New York Infantry · Separate National Guard lineage',
(74,'rct'):'474th Infantry / 74th Regimental Combat Team · Separate lineage',
(75,'ranger'):'5307th Composite Unit / 475th Infantry / 75th Rangers · Separate lineage',
(75,1):'Company C, 75th Infantry / 1st Ranger Battalion lineage',
(75,2):'Company H, 75th Infantry / 2d Ranger Battalion lineage',
(75,3):'Company F, 75th Infantry / 3d Ranger Battalion lineage',
(75,'stb'):'Company N / Ranger Special Troops Battalion lineage',
(75,'mi'):'Company P / Ranger Military Intelligence Battalion lineage',
(85,3):'3d Battalion, 85th Infantry · Warrior Transition Battalion',
(99,'separate'):'99th Infantry Battalion (Separate)',
(100,'separate'):'100th Infantry Battalion / 100th Battalion, 442d Infantry',
}
for n in (68,69): UNIT_LABELS[n,'tanks']=f'{n}th Infantry (Light Tanks) · Separate organization'
for n in (96,97,98): UNIT_LABELS[n,'scouts']=f'{n}th Infantry Battalion (Philippine Scouts) · Separate battalion'
for n in (266,267,268,269): UNIT_LABELS[66,'aib'+str(n)]=f'{n}th Armored Infantry Battalion · Successor'
for n in (62,68,19): UNIT_LABELS[62,'aib'+str(n)]=f'{n}th Armored Infantry Battalion · Successor'

NOTES = {
61:'The 1st Battalion row begins with its 1962 reorganization. Earlier battalions share regimental service. The modern training mission is also documented by the Army in April 2026.',
62:'The regiment became Philippine Scouts in 1921. Its later armored organization split in 1943 into the 62d, 68th and 19th Armored Infantry Battalions. Their rows end at the European war coverage boundary, not an inactivation date.',
63:'The three wartime battalions share the regimental division row; their existence does not establish later independent battalion lineages.',
65:'Puerto Rico Infantry became the 65th in 1920. The later National Guard battalions belonged to the separate 92d Infantry Brigade, not a 92d Infantry Division. The 1992 reorganization retained only the 1st Battalion; Company E dates show organizational scope rather than a verified divisional assignment.',
66:'This is the infantry regiment constituted in July 1943 for the 71st Division. The earlier 66th Infantry (Light Tanks), redesignated as armor in 1940, is a separate organization. Inactivation took place 5–9 April 1946; the 1953 armored successors were inactive paper organizations.',
67:'The 1918 infantry organization is distinct from the later 67th Infantry (Medium Tanks), which became the 67th Armored Regiment in 1940. Armor service is not silently continued as an infantry-regiment assignment.',
68:'The World War I regiment and the 1933 Light Tanks organization are distinct. The tank row closes at the July 1940 conversion to armor; later armor deployments are outside this infantry timeline.',
69:'Three organizations used this number: the 1918 Regular Army regiment, the inactive 1933 Light Tanks regiment, and New York’s Fighting 69th. Separate rows prevent an invented shared lineage. The 2011 battalion boundary is the date of a confirming DMNA report, not a transfer order.',
71:'The Regular Army’s 1918 regiment is distinct from the New York National Guard regiment. New York service is shown separately; its later assignment history is incomplete here. The 1946 boundary limits verified wartime coverage and is not an inactivation order.',
74:'The World War I 74th and the 474th Infantry/74th Regimental Combat Team are separate organizations. The 99th Infantry Battalion joined the latter during World War II and again in the 1950s; see the 99th numbering page for its separate history.',
75:'The World War I 75th Infantry did not become the Ranger regiment. The Ranger lineage begins with the 5307th Composite Unit in 1943 and continues through the 475th Infantry. Ranger battalion rows include their lettered-company predecessors; regimental affiliation is not division assignment.',
85:'The 10th Light Division became the 10th Mountain Division in 1944 and was named the 10th Infantry Division when reactivated in 1948. The chart normalizes these names. The later 3d Battalion was a medical recovery organization, not a combat battalion assigned to a division.',
86:'The World War II organization was constituted in November 1942. Its phased activation is shown as an uncertain interval. “10th Mountain” includes the division’s earlier Light and later Infantry designations.',
87:'The 1918 organization and the mountain regiment constituted in 1941 are shown separately. The 10th Division’s Light, Mountain and Infantry names are normalized. The 3d Battalion’s Army Reserve command was not the 96th Infantry Division.',
88:'The World War I organization is separate from the airborne battalion formed in 1941, expanded into a glider regiment in 1942. It reached France in 1945 but was absorbed into the 326th Glider Infantry before combat.',
89:'The World War II activation was piecemeal: Company A, 3d Battalion and Company L have separate rows. This does not imply that the entire regimental headquarters was active. The 1919 demobilization day remains unresolved.',
90:'The 1943 organization served briefly in the 10th Light Division. Sources differ between 13 and 22 February 1944 for its relief; that interval is left unresolved before replacement-training service.',
91:'The compiled order of battle lists activation as a separate regiment on 10 March 1942; only that dated observation is plotted. The following unknown interval does not imply a transfer the next day. National Archives morning reports corroborate the organization. Do not confuse it with the U.S. 91st Division or Philippine Army’s 91st Regiment.',
}
for n in (72,73,76,77,78,79,80,81,82,83,84):
    NOTES[n]='Organized during the month preceding the first division bar. The unknown interval beginning in 1919 covers demobilization, not an inferred assignment to another division. This short-lived World War I organization trained in the United States and did not deploy overseas.'
for n in range(92,101):
    NOTES[n]='Regular Army infantry regimental numbers 92–100 were allotted but never constituted. This is a numbering record, not a regiment with invented divisions or battalions. Separately numbered battalions, where documented, are identified below and do not establish a regiment of the same number.'
NOTES[100]+=' The 100th Battalion served with the 442d Infantry. Operational attachments in Italy and France must be distinguished from a permanent divisional assignment.'

PERIOD_NOTES = {}
for n,b,sid,steps in ROWS:
    for step in steps.split(';'):
        start,code=step.split()
        if code=='never': PERIOD_NOTES[n,b,start]='This regimental number was never constituted in the numbering history cited below. Related separate battalions are distinct organizations, not battalions of a regiment with this number.'
        if sid==401 and code.startswith('d') and code!='disbanded':
            PERIOD_NOTES[n,b,start]='Division membership is documented after organization in the preceding month. The displayed boundary brackets a month-only formation date; it is not a claimed assignment order effective on this day.'
        if n==91 and code=='ind': PERIOD_NOTES[n,b,start]='The compiled order of battle records activation as a separate regiment on this day. The one-day bar is a dated observation, not an assertion that separate status lasted only one day.'
        if code=='medical': PERIOD_NOTES[n,b,start]='Medical recovery and transition support at Fort Drum. This battalion is not represented as an operational element of the 10th Mountain Division.'
        if code=='reserve': PERIOD_NOTES[n,b,start]='Army Reserve service. Battalion, battle-group and regimental redesignations are recorded here without inferring a maneuver-division assignment.'
        if code=='training_ww2': PERIOD_NOTES[n,b,start]='Training service outside an established maneuver-division assignment. This label does not imply membership in the later TRADOC command.'
        if code=='ar96': PERIOD_NOTES[n,b,start]='Assigned to the 96th Army Reserve Command, an administrative command distinct from the 96th Infantry Division.'

EVIDENCE = [
(61,3,'Training predecessor','The training battalion at Fort Jackson was reflagged as 1st Battalion in June 1993. An exact earlier divisional sequence is not established here.',403),
(63,2,'Luzon, 1945','The battalion’s distinguished service included Mount Santo Domingo; its divisional assignment is covered by the common regimental row.',1063),
(63,3,'Luzon, 1945','The battalion’s wartime service included the Montalban fighting under the regimental 6th Division assignment.',1063),
(68,1,'Light Tanks organization','In the separately constituted tank regiment, 1st Battalion activated 1 January 1940 and inactivated 30 June 1940 before the conversion to armor.',1068),
(68,2,'Light Tanks organization','The separate tank regiment’s 2d Battalion activated 1 January 1940. This is not evidence of continuity from the 1918 regiment.',1068),
(71,1,'New York regiment, Aleutians','Headquarters Company of New York’s 1st Battalion was detached for the 1943 Attu operation. The attachment did not transfer the entire regiment from the 44th Division.',406),
(71,2,'New York regiment, Europe','The New York regiment’s 2d Battalion earned a Presidential Unit Citation in World War II. It is distinct from the 1918 Regular Army organization.',406),
(71,3,'New York regiment, Europe','Company I of the New York regiment’s 3d Battalion earned a Presidential Unit Citation during World War II.',406),
(79,'scouts','Separate Philippine Scouts organization','On 6 April 1946 the former 1st Battalion, 43d Infantry (PS), was redesignated the 79th Infantry (PS). This is not the 1918 regiment; a precise later division chronology is not established here.',303),
(87,'C','Vietnam security service','Company C served in Vietnam during 1966–1972. It is not plotted as the later 3d Battalion or as an entire regiment deployed to Vietnam.',1087),
(87,'D','Vietnam rifle-security company','The association records Company D’s Vietnam-era service separately from the later 4th Battalion. Company service alone does not establish a divisional transfer of the parent regiment.',408),
(91,'records','Archival confirmation','The National Archives index includes Company M, 91st Infantry, in 1942 and Company K in 1943. These records establish unit names, not complete division assignment dates.',410),
]
UNIT_LABELS[91,'records']='91st Infantry · Company records'
UNIT_LABELS[79,'scouts']='79th Infantry (Philippine Scouts) · Separate organization'
SERVICE=[]
TOURS=[]
UPDATES={}
STEP_SOURCES={}
CAMPAIGNS={61:[('1918','France')],63:[('1944','New Guinea'),('1945','Luzon')],64:[('1918','Lorraine')],65:[('1944-1945','France and Germany'),('1950-1953','Korean War')],66:[('1945','Central Europe')],85:[('1945','Italy')],86:[('1945','Italy')]}
OPERATIONS = [
(61,1,'1968-1971','Vietnam','The battalion deployed with the 1st Brigade, 5th Infantry Division; these year labels summarize service, not exact movement dates.',403),
(69,'ny','1918','France · 165th Infantry','New York’s regiment served with the 42d Division as the 165th Infantry.',414),
(69,'ny','1943-1945','Makin, Saipan and Okinawa','The 165th Infantry served in the Pacific with the 27th Division.',405),
(71,'ny','1944-1945','France, Germany and Austria','New York’s 71st served with the 44th Division in the European theater.',406),
(74,'rct','1945','Europe · 474th Infantry','The separate 474th served in Europe before its postwar redesignation as the 74th Regimental Combat Team.',1074),
(75,'ranger','1944-1945','Burma','The 5307th Composite Unit and its 475th Infantry successor fought in the China-Burma-India theater.',4125),
(75,1,'1969-1971','Vietnam · Company C predecessor','Company C, 75th Infantry, carried the lineage later redesignated as 1st Battalion.',4126),
(75,2,'1969-1972','Vietnam · Company H predecessor','Company H, 75th Infantry, carried the later 2d Battalion lineage.',4127),
(75,3,'1969-1971','Vietnam · Company F predecessor','Company F, 75th Infantry, carried the later 3d Battalion lineage.',4128),
(75,'stb','1969-1971','Vietnam · Company N predecessor','Service belongs to the lettered-company predecessor, not a Special Troops Battalion already bearing that title.',4130),
(75,'mi','1969-1971','Vietnam · Company P predecessor','Service belongs to the company predecessor, not a Military Intelligence Battalion already bearing that title.',4129),
(75,1,'1983','Grenada','Rangers participated in Operation Urgent Fury.',407),
(75,2,'1983','Grenada','Rangers participated in Operation Urgent Fury.',407),
(75,'ranger','1989','Panama','The regiment participated in Operation Just Cause.',407),
(75,3,'1993','Somalia','Elements deployed with Task Force Ranger.',407),
(75,'ranger','2001','Afghanistan','Ranger operations opened a long period of repeated deployments; this marker is not a continuous tour.',407),
(75,'ranger','2003','Iraq','Rangers participated in the opening operations in Iraq.',407),
(87,0,'1943','Aleutian Islands','The regiment took part in the Kiska operation before its 10th Division assignment.',1087),
(87,0,'1945','Italy','Mountain infantry combat in the northern Apennines and Po Valley.',4131),
(87,1,'2002','Afghanistan','Elements fought in Operation Anaconda.',1087),
(87,1,'2005-2006','Iraq','Battalion deployment recorded in the regimental history.',1087),
(87,3,'1991','Germany','Army Reserve battalion personnel provided security support during the Gulf War; this was not a Persian Gulf combat deployment.',1087),
(87,4,'1991-1992','Sinai','Multinational Force and Observers peacekeeping rotation.',408),
(87,5,'1989','Panama','Participation in Operation Just Cause.',408),
(88,0,'1945','France','The glider regiment arrived overseas but was absorbed into the 326th before entering combat.',1088),
(89,'L','1941-1944','Bermuda','Separate garrison duty; this is not a deployment of the entire regiment.',1089),
(99,'separate','1944-1945','Western Europe','The Norwegian-American separate battalion served in France, Belgium and Germany.',411),
(100,'separate','1943-1944','Italy · attached to the 34th Division','Operational attachment of the separate battalion, later incorporated into the 442d Infantry; not an assignment of a 100th Infantry Regiment.',415),
(100,'separate','1944','France · 442d Infantry','The battalion fought with the 442d during its attachment to the 36th Division in the Vosges.',415),
(100,'separate','2005-2006','Iraq','Credited service years in the Army lineage certificate; not exact departure and return dates.',4183),
(100,'separate','2008-2009','Iraq','Credited service years in the Army lineage certificate.',4183),
]
for bn in (62,68,19):
    OPERATIONS.append((62,'aib'+str(bn),'1944-1945','Western Europe','Armored infantry successor service with the 14th Armored Division.',1062))
