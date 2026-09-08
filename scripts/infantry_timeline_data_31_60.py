"""Reviewed 31-60 extension. Dates are effective dates, ends exclusive.

String elements identify companies or predecessor battalions, not invented
numbered battalions. i_<division> preserves an inactive unit's paper assignment.
Month/year-only changes use an explicitly unknown interval, never a guessed day.
"""

SOURCES = {
307: ('https://www.army.mil/article/218041/army_activates_new_battalion_to_train_infantrymen', 'U.S. Army: 3d Battalion, 47th Infantry activation, March 2019'),
308: ('https://www.army.mil/article-amp/189849/new_bct_battalion_activates_at_fort_leonard_wood', 'U.S. Army: 2d Battalion, 48th Infantry activation, June 2017'),
309: ('https://www.army.mil/article/225308/3_54_reactivates_to_enable_success_of_198th_infantry_brigades_22_week_infantry_osut', 'U.S. Army: 3d Battalion, 54th Infantry activation, July 2019'),
310: ('https://www.armyupress.army.mil/Portals/7/combat-studies-institute/csi-books/OrderofBattle1.pdf#page=426', 'Combat Studies Institute: U.S. Army Order of Battle, 1919-1941, vol. 1, pp. 391-397'),
301: ('https://armyhistory.org/31st-infantry-regiment/', 'Army Historical Foundation: 31st Infantry history'),
302: ('https://www.25thida.org/units/infantry/35th-infantry-regiment/', '25th Infantry Division Association: 35th Infantry and battalion lineages'),
303: ('https://www.philippinescouts.org/the-scouts/units/43rd-infantry-ps', 'Philippine Scouts Heritage Society: 43rd Infantry'),
304: ('https://www.philippinescouts.org/the-scouts/units/45th-infantry-ps', 'Philippine Scouts Heritage Society: 45th Infantry'),
305: ('https://www.i-served.com/f51lineage.htm', 'Company F, 51st Infantry: reproduced Army lineage, 15 June 2011'),
306: ('https://www.officialmilitaryribbons.com/pdf/army_infantry_rangers_lineage_honors_pdf/31st%20Infantry%20Regiment.pdf', '31st Infantry: legible copy of Army lineage certificate'),
}

ROWS = [
(31,0,306,'1916-01-01 notformed;1916-07-01 unk;1921-10-22 phil;1931-06-26 ind;1941-01-01 unk;1942-01-01 phil;1942-04-09 captured;1946-01-19 d7;1957-07-01 end'),
(32,0,89,'1916-01-01 notformed;1916-07-01 unk;1918-07-31 d16;1919-03-08 ind;1921-11-01 inactive;1940-07-01 d7;1957-07-01 end'),
(32,1,90,'1957-07-01 d7;1971-03-31 d2;1978-10-21 inactive;1980-08-07 d7;1987-06-10 inactive;1996-02-16 m10;2004-09-16 m10'),
(33,0,1033,'1916-01-01 notformed;1916-07-01 unk;1919-06-01 ind;1921-07-03 panama;1938-10-10 ind;1944-06-26 inactive;1946-02-01 ind;1948-09-01 inactive;1950-01-04 ind;1954-12-02 d23;1956-05-26 inactive'),
(34,0,91,'1916-01-01 notformed;1916-07-01 unk;1917-12-06 d7;1923-03-24 d8;1927-08-15 d4;1933-10-01 d8;1940-06-05 inactive;1940-07-01 d8;1943-06-12 d24;1958-06-05 end'),
(34,1,92,'1958-06-05 d24;1970-04-15 inactive;1987-02-27 training;1992-09-30 inactive;1996-01-15 training'),
(35,0,93,'1916-01-01 notformed;1916-07-01 unk;1918-08-07 d18;1919-02-14 ind;1922-10-17 hawaii;1941-10-01 d25;1957-02-01 end'),
(35,1,302,'1957-02-01 d25;1967-08-01 d4;1970-04-10 i_d4;1972-06-05 d25;1987-07-27 inactive'),
(35,2,94,'1957-02-01 inactive;1962-02-19 d25;1967-08-01 d4;1970-12-15 d25;1972-06-05 inactive;1995-08-16 d25;2005-11-16 d25'),
(36,0,95,'1916-01-01 notformed;1916-07-01 unk;1918-07-05 d12;1919-01-31 ind;1921-10-13 inactive;1923-03-24 i_d9;1940-08-01 inactive;1941-04-15 a3;1945-11-10 inactive;1947-07-07 end'),
(36,'aib36',95,'1947-07-07 i_a3;1947-07-15 a3;1957-10-01 end'),
(36,'aib37',95,'1947-07-07 i_a3;1947-07-15 a3;1957-10-01 end'),
(36,'aib13',95,'1947-07-07 i_a3;1947-07-15 a3;1957-10-01 end'),
(36,1,96,'1957-02-15 a1;1957-12-23 i_a1;1962-02-03 a3;1989-06-16 inactive;1997-02-16 a1;2008-09-16 a1'),
(37,0,1037,'1916-01-01 notformed;1916-07-01 unk;1919-06-01 ind;1921-10-20 inactive;1923-03-24 i_d9;1940-08-01 inactive;1941-08-01 ind;1945-02-05 inactive;1946-08-01 ind;1949-01-25 inactive'),
(38,0,97,'1916-01-01 notformed;1917-05-15 unk;1917-10-01 d3;1939-10-16 d2;1957-11-08 end'),
(38,1,98,'1957-11-08 ind;1958-03-04 inactive;1962-02-19 d2;1986-12-16 inactive;1987-08-28 training;2006-04-27 inactive;2006-06-01 d2;2014-03-16 d4'),
(39,0,1039,'1916-01-01 notformed;1917-05-15 unk;1917-11-19 d4;1921-09-21 i_d4;1927-08-15 i_d7;1933-10-01 i_d4;1940-08-01 i_d9;1940-08-09 d9;1946-11-30 inactive;1947-07-15 d9;1957-04-01 end'),
(39,2,99,'1957-04-01 d4;1963-10-01 inactive;1966-02-01 d9;1969-09-25 i_d9;1972-04-21 d9;1983-01-21 inactive;1987-04-03 training'),
(39,3,100,'1957-04-01 d9;1957-12-01 inactive;1966-02-01 d9;1969-09-25 i_d9;1972-07-21 d9;1983-01-21 inactive;1987-04-03 training;1988-12-16 inactive;2016-10-01 training'),
(40,0,1040,'1916-01-01 notformed;1917-05-15 unk;1918-07-05 d14;1919-02-01 unk;1919-03-01 ind;1921-11-01 inactive;1923-03-24 i_d8;1940-07-01 inactive;1944-11-11 disbanded'),
(41,0,1041,'1916-01-01 notformed;1917-05-15 unk;1918-07-09 d10;1919-02-18 ind;1921-09-22 inactive;1940-07-15 a2;1946-03-25 end'),
(41,'aib41',101,'1946-03-25 a2;1957-07-01 end'),
(41,1,101,'1957-07-01 a2;1992-06-15 i_a2;1992-12-16 a2;1995-12-15 inactive;1996-02-16 a1;2007-04-16 a1;2008-03-15 i_a1;2009-08-16 a1;2015-04-16 d4'),
(41,3,102,'1957-07-01 inactive;1961-04-25 ind;1962-12-21 inactive;1978-10-01 a2;1991-05-21 cav1;1992-12-16 a2;1996-01-16 d4;1996-02-15 inactive;2011-01-16 a1'),
(42,0,1042,'1916-01-01 notformed;1917-05-15 unk;1918-07-05 d12;1919-01-31 ind;1921-07-03 panama;1927-03-14 unk;1927-08-01 i_panama;1928-01-01 unk;1929-01-01 inactive;1944-11-11 disbanded'),
(43,0,1043,'1916-01-01 notformed;1917-06-01 unk;1921-10-22 phil;1922-09-30 end'),
(43,0,303,'1922-09-30 inactive;1931-06-26 i_phil;1946-01-01 unk;1947-01-01 phil;1947-10-25 end'),
(43,1,303,'1941-04-01 phil;1942-05-01 unk;1942-06-01 captured;1946-01-01 end'),
(44,0,1044,'1916-01-01 notformed;1917-06-01 unk;1919-06-01 ind;1921-03-01 hawaii;1921-10-22 ind;1921-11-28 inactive;1922-07-17 disbanded'),
(44,'ps',1044,'1931-06-26 i_phil;1944-11-11 disbanded;1946-01-01 unk;1947-01-01 phil;1949-01-01 unk;1950-01-01 inactive'),
(45,0,1045,'1916-01-01 notformed;1917-06-01 unk;1919-06-01 ind;1921-10-22 phil;1942-04-09 end'),
(45,0,304,'1942-04-09 captured;1946-03-26 phil;1948-12-20 inactive;1951-10-10 disbanded'),
(46,0,1046,'1916-01-01 notformed;1917-05-15 unk;1918-07-05 d9;1919-02-15 ind;1921-11-16 inactive;1922-07-31 disbanded;1941-08-28 i_a5;1941-10-01 a5;1943-09-20 end'),
(46,'aib47',103,'1943-09-20 a5;1945-10-08 i_a5;1948-07-06 a5;1950-02-01 i_a5;1950-09-01 a5;1956-03-16 i_a5;1957-02-15 end'),
(46,'aib15',105,'1943-09-20 a5;1945-10-08 i_a5;1948-07-06 a5;1950-02-01 i_a5;1950-09-01 a5;1956-03-16 i_a5;1957-02-15 end'),
(46,1,103,'1957-02-15 a1;1957-12-23 i_a1;1958-02-25 inactive;1958-04-01 ind;1962-02-03 a1;1967-05-12 b198;1969-02-15 d23;1971-11-01 b196;1972-09-13 a1;1984-08-01 inactive;1987-01-30 training;2010-12-08 inactive;2012-03-01 training'),
(46,2,104,'1957-10-01 a3;1962-02-03 a1;1972-09-13 inactive;1987-01-30 training'),
(46,5,105,'1959-07-01 inactive;1967-10-02 ind;1968-03-31 b198;1969-02-15 d23;1971-05-22 inactive;2000-10-01 training'),
(47,0,106,'1916-01-01 notformed;1917-05-15 unk;1917-11-19 d4;1921-09-22 i_d4;1927-08-15 i_d7;1933-10-01 inactive;1940-08-01 i_d9;1940-08-10 d9;1946-12-31 inactive;1947-07-15 d9;1957-04-01 end'),
(47,2,107,'1957-04-01 d4;1963-10-01 inactive;1966-02-01 d9;1970-10-13 i_d9;1972-11-21 d9;1988-08-15 inactive;1996-04-15 training;1999-04-05 inactive;1999-04-15 training'),
(47,3,108,'1957-04-01 d9;1957-12-01 inactive;1959-04-10 i_d81;1959-05-01 d81;1963-04-01 inactive;1966-02-01 d9;1969-08-01 i_d9;1973-03-21 d9;1991-02-16 b199;1994-01-14 inactive;1996-10-02 training;1999-02-01 inactive;1999-03-01 training;2003-12-15 inactive;2006-04-27 training'),
(48,0,109,'1916-01-01 notformed;1917-05-15 unk;1918-07-31 d20;1919-02-28 ind;1921-10-14 inactive;1922-07-31 disbanded;1942-02-27 i_a7;1942-03-02 a7;1943-09-20 end'),
(48,'aib48',109,'1943-09-20 a7;1945-10-08 i_a7;1950-11-24 a7;1953-11-15 i_a7;1957-02-15 end'),
(48,'aib38',109,'1943-09-20 a7;1945-10-11 i_a7;1950-11-24 a7;1953-11-15 i_a7;1957-02-15 end'),
(48,'aib23',109,'1943-09-20 a7;1945-10-11 i_a7;1950-11-24 a7;1953-11-15 i_a7;1957-02-15 end'),
(48,1,110,'1957-02-15 a1;1957-12-23 i_a1;1958-02-25 inactive;1958-04-01 ind;1963-09-01 a3;1989-06-16 inactive;1996-04-15 training'),
(49,0,1049,'1916-01-01 notformed;1917-05-15 unk;1918-08-12 attached83;1919-01-01 unk;1919-02-01 ind;1921-11-18 inactive;1922-07-31 disbanded;1941-07-18 i_a8;1942-04-01 a8;1943-09-20 end'),
(49,'aib58',120,'1943-09-20 a8;1945-11-11 i_a8;1951-07-10 end'),
(50,0,1050,'1916-01-01 notformed;1917-05-15 unk;1918-07-31 d20;1919-02-28 ind;1921-12-31 inactive;1922-07-31 disbanded;1942-01-08 i_a6;1942-02-15 a6;1943-09-20 end'),
(50,'aib44',111,'1943-09-20 a6;1945-09-19 i_a6;1950-09-05 a6;1956-03-16 i_a6;1957-07-01 end'),
(50,1,111,'1957-07-01 a2;1967-09-01 ind;1970-12-16 a2;1983-03-15 inactive;1987-08-28 training'),
(51,0,1051,'1916-01-01 notformed;1917-05-15 unk;1917-11-16 d6;1921-09-22 i_d6;1927-08-15 i_d9;1933-10-01 i_d6;1939-10-16 inactive;1941-04-15 a4;1943-09-10 end'),
(51,'F',305,'1943-09-10 a4;1946-05-01 const14;1948-12-20 i_a4;1954-06-15 a4;1957-04-01 inactive;1967-09-25 ind;1968-12-26 inactive;1986-12-16 ind;1991-11-15 inactive;1995-04-16 ind;2009-03-15 inactive;2011-01-16 a1'),
(52,0,112,'1916-01-01 notformed;1917-05-15 unk;1917-11-16 d6;1921-09-01 i_d6;1927-08-15 i_d9;1933-10-01 i_d6;1940-10-01 inactive;1942-07-15 a9;1943-10-09 end'),
(52,'aib52',112,'1943-10-09 a9;1945-10-13 i_a9;1950-09-14 i_d71;1953-02-25 i_a9;1956-07-23 inactive;1956-08-15 ind;1958-06-24 inactive;1959-07-01 end'),
(52,1,113,'1943-10-09 a9;1945-10-13 i_a9;1950-09-14 i_d71;1953-02-25 i_a9;1957-03-01 ind;1962-02-03 a1;1967-05-12 b198;1969-02-15 d23;1971-11-30 ind;1972-09-15 a1;1987-11-16 inactive;1988-01-16 ind;1991-10-16 b177;1994-10-15 inactive;2001-12-19 end'),
(52,2,114,'1943-10-09 a9;1945-10-13 i_a9;1950-09-14 i_d71;1953-02-25 i_a9;1957-03-01 inactive;1957-10-01 a3;1962-02-03 a1;1963-09-10 i_a1;1967-05-12 a1;1972-09-15 inactive;2003-12-03 end'),
(52,'A',113,'2001-12-19 inactive;2004-01-16 b172;2006-12-16 inactive;2007-04-17 d2'),
(52,'B',114,'2003-12-03 inactive;2005-10-16 d25'),
(52,'C',115,'1959-07-01 inactive;1966-06-01 ind;1972-08-15 inactive;2000-09-16 d2;2005-07-27 d2'),
(52,'D',116,'1959-07-01 inactive;1966-06-01 ind;1969-11-22 inactive;1971-06-30 ind;1972-11-26 inactive;2002-07-16 d25;2006-06-01 inactive;2006-12-16 d25;2014-10-15 inactive;2015-09-16 ind'),
(52,'F',117,'1959-07-01 inactive;1967-12-20 ind;1969-02-01 inactive;1996-06-16 ind;1997-09-15 inactive;2006-06-01 d2'),
(53,0,1053,'1916-01-01 notformed;1917-11-01 unk;1917-12-01 d6;1922-09-23 i_d6;1923-03-24 i_d7;1940-07-01 d7;1942-01-01 unk;1950-09-29 training101;1953-12-01 inactive'),
(54,0,118,'1916-01-01 notformed;1917-05-15 unk;1917-11-16 d6;1922-10-24 i_d6;1923-03-24 i_d7;1940-10-01 inactive;1942-07-15 a10;1943-09-20 end'),
(54,2,119,'1943-09-20 a10;1945-10-23 i_a10;1950-09-14 i_d71;1953-02-25 i_a10;1957-04-01 inactive;1957-09-23 ind;1963-07-15 a4;1971-05-10 inactive;1987-08-28 training'),
(55,0,1055,'1916-01-01 notformed;1917-05-15 unk;1917-11-16 d7;1921-09-22 inactive;1922-07-31 disbanded;1942-06-09 i_a11;1942-08-15 a11;1943-09-20 end'),
(56,0,1056,'1916-01-01 notformed;1917-05-15 unk;1917-11-16 d7;1921-09-21 inactive;1922-07-31 disbanded;1942-07-07 i_a12;1942-09-15 a12;1943-11-11 end'),
(57,0,1057,'1916-01-01 notformed;1917-05-15 unk;1918-07-31 d15;1919-05-18 ind;1921-10-22 phil;1942-04-09 captured;1946-04-06 phil;1949-06-01 inactive;1951-10-10 disbanded'),
(58,0,1058,'1916-01-01 notformed;1917-05-15 unk;1917-11-19 d4;1922-06-21 inactive;1922-07-31 disbanded;1942-04-08 inactive;1942-04-24 ind;1944-01-26 end'),
(58,2,120,'1944-01-26 ind;1945-03-02 inactive;1951-07-10 i_a8;1956-07-23 inactive;1956-08-15 ind;1957-07-01 a2;1963-07-01 inactive;1975-04-01 a2;1981-05-31 inactive;1987-08-28 training'),
(59,0,1059,'1916-01-01 notformed;1917-05-15 unk;1917-11-19 d4;1922-09-28 disbanded;1942-07-07 i_a13;1942-10-15 a13;1943-09-20 end'),
(59,'aib59',1059,'1943-09-20 a13;1945-11-09 unk;1945-11-13 i_a13;1947-08-21 a13;1952-02-22 end'),
(59,'aib67',1059,'1943-09-20 a13;1945-11-09 unk;1945-11-13 i_a13;1948-03-23 a13;1952-02-22 end'),
(59,'aib16',1059,'1943-09-20 a13;1945-11-09 unk;1945-11-13 i_a13;1948-01-22 a13;1952-02-22 end'),
(59,0,1059,'1952-02-22 a13;1952-03-01 d96;1959-05-20 end'),
(60,0,121,'1916-01-01 notformed;1917-05-15 unk;1917-11-17 d5;1921-09-02 i_d5;1927-08-15 i_d8;1933-10-01 i_d5;1939-10-16 inactive;1940-08-01 i_d9;1940-08-10 d9;1946-11-30 unk;1946-12-29 inactive;1947-07-15 d9;1957-12-01 end'),
(60,2,122,'1957-12-01 inactive;1958-02-15 b2;1962-02-19 inactive;1966-02-01 d9;1970-10-13 i_d9;1972-10-21 d9;1991-02-15 inactive;1996-04-15 training'),
(60,3,123,'1957-12-01 inactive;1966-02-01 d9;1969-08-01 i_d9;1972-11-21 d9;1988-08-15 inactive;2005-11-16 training'),
]

NOTES = {
31: 'The 1941 Philippine Division reassignment is dated only to the year in the Army certificate. That year is shown as uncertain; the division is shown from the following January. Surrender and captivity are distinguished from formal inactivation.',
33: 'The Panama Canal Division became inactive in 1932; the regiment remained assigned on paper until 1938 while attached to the Pacific Sector. June 1919 is the earliest separate-regiment status established here, not a claimed assignment date. Canal and Caribbean defense service did not produce a combat campaign honor.',
36: 'The 1947 successor battalions were the 36th, 37th and 13th Armored Infantry Battalions. Their numbers are not additional battalions of the modern 37th or 13th Infantry regiments. The 1st Battalion row follows Company A after it separated in February 1957.',
37: 'Regular Army Inactive organizations could train with Reserve officers while remaining inactive on the Regular Army rolls. June 1919 marks the earliest separate-regiment status established here. Alaskan Defense Command service was outside an assigned division.',
38: 'The prewar 1st Battalion was inactive from 1 October 1933 to 1 May 1939 even while the regiment remained assigned to the 3d Division.',
39: 'The common row closes when the 2d Battle Group separated in April 1957. Remaining regimental elements retained the 9th Division affiliation until the December 1957 reorganization.',
40: 'Relief from the 14th Division is dated only to February 1919, which is shown as uncertain. Later Reserve-officer training did not turn the Regular Army Inactive regiment into an active combat organization.',
42: 'Inactivation occurred in stages during March-July 1927; relief from the Panama Canal Division is dated only to 1928. These transition windows remain uncertain. Later ROTC and Reserve-officer training belonged to a Regular Army Inactive organization.',
43: 'Only the 1st Battalion returned to active service in 1941. Postwar reorganization is dated only to 1946 here. The 96th, 97th and 98th Infantry Battalions (Philippine Scouts) succeeded the regiment in 1947; they are not battalions numbered 96-98 within this regiment.',
44: 'Two distinct 20th-century organizations used this number. The 1917 regiment and the Philippine Scout regiment constituted in 1931 have separate rows; shared numbering does not establish one continuous lineage. Year-only Scout activation and inactivation dates remain uncertain.',
45: 'The Scout heritage society dates the Bataan surrender to 9 April 1942; some secondary accounts give 10 April. The postwar 1st Battalion became the 77th Infantry (Philippine Scouts). The Philippine Division was subsequently named the 12th Infantry Division (Philippine Scouts).',
46: 'World War II service belongs to the successor armored infantry battalions. Later numbered battalion headquarters descend from companies; the old battalion number does not determine the modern lineage.',
47: 'The 2d Battle Group separated in April 1957; the other elements remained with the 9th Division until December. The 3d Battle Group served in the Army Reserve with the 81st Division before its later Regular Army service.',
49: 'The 83d Division relationship in France was an attachment for depot and replacement work. January 1919 return timing is not precise. The 58th Armored Infantry Battalion later merged with a 58th Infantry lineage in 1951; follow the 58th timeline for that continuation.',
51: 'The Company F row includes its Company C, 10th Armored Infantry Battalion and constabulary predecessors. A temporary attachment is not a formal division assignment. The secondary regimental history and reproduced company certificate disagree on the 1939-1940 relief date; the regimental row follows the former.',
52: 'The 1st and 2d Battalion headquarters became Companies A and B in 2001 and 2003. Separate company rows start at those redesignations. C, D and F also held inactive battle-group designations; their labels follow the later companies. Pre-1957 battalion rows trace their predecessor companies in armored infantry battalions.',
53: 'The 1942-1950 gap includes Alaska service and organizational changes whose precise dates are not established by the sources used here. The 1950-1953 association with the 101st Airborne Division was a training attachment, not an overseas combat deployment. The November 1917 assignment is recorded only to the month here.',
54: 'The 2d Battalion row traces Company B through the 61st and 561st Armored Infantry Battalions before its 1957 redesignation. Inactive paper assignments to the 71st Infantry and 10th Armored Divisions are explicitly labeled inactive.',
55: 'The regiment broke up in September 1943. Its successor 55th, 63d and 21st Armored Infantry Battalions served with the 11th Armored Division. They are identified in the service notes rather than extending a nonexistent tactical regiment through the war.',
56: 'In November 1943 the regiment became the 66th, 17th and 56th Armored Infantry Battalions of the 12th Armored Division. Their subsequent service is recorded in separate notes, not as an uninterrupted regimental assignment.',
57: 'Postwar reorganization expanded the former 1st Battalion into the 78th Infantry (Philippine Scouts), with a new 1st Battalion constituted for the 57th. The Philippine Division later bore the 12th Infantry Division (Philippine Scouts) designation.',
58: 'The 2d Battalion row traces Company B of the 203d Infantry Battalion and its 1951 consolidation with Company B, 58th Armored Infantry Battalion. The latter descended from the 49th Infantry; its earlier World War II combat credit is not presented as a deployment of the 58th Infantry regiment.',
59: 'The armored infantry battalions inactivated on different dates during 9-12 November 1945; that window is uncertain here. Their postwar service was in the Organized Reserve Corps. The common row resumes at their 1952 consolidation.',
60: 'Regimental inactivation took place during 30 November-28 December 1946. The transition window is shown as uncertain rather than assigning every element the same day.',
}

ROWS += [
(31,4,88,'1957-07-01 inactive;1965-01-01 unk;1966-01-01 b196;1969-02-15 d23;1971-10-26 ind;1991-10-02 training;1995-02-01 inactive;1996-04-16 m10;2005-09-16 m10'),
(48,2,308,'2017-06-16 training'),
(54,3,309,'2019-07-31 training'),
]
UPDATES = {
(47,3):(307,'2013-04-01 unk;2013-05-01 inactive;2019-03-01 training'),
(51,'F'):(1051,'2013-11-15 inactive;2014-11-16 ind'),
(41,3):(1041,'2018-01-01 unk;2019-01-01 inactive'),
}
STEP_SOURCES = {(53,0,'1940-08-01'):310,(53,0,'1941-11-29'):310}
# Only a formation year is established in the secondary summary of the 53d.
# Keep the whole pre-formation portion of that year uncertain.
ROWS = [(n,b,s,t.replace('1917-11-01 unk','1917-01-01 unk').replace('1940-07-01 d7;1942-01-01 unk','1940-07-01 unk;1940-08-01 d7;1941-11-29 ind;1942-01-01 unk') if n==53 else t) for n,b,s,t in ROWS]
NOTES[53] += ' The Army order of battle dates activation to 1 August 1940 and divisional relief to 29 November 1941. The secondary history gives July for activation, so July is left uncertain.'
NOTES[47] += ' April 2013 inactivation is documented only to the month in the later Army article; the whole month is shown as uncertain.'
NOTES[41] = 'The 3d Battalion was replaced during 2018, according to the regimental history. That year is shown as uncertain and the following January begins the last-documented inactive interval; it is not an exact inactivation date.'
NOTES[31] += ' The 4th Battalion activation is shown within a 1965 uncertainty window; its brigade assignment is established by the following January. Its 1991 training headquarters briefly carried the Company F designation.'

EVIDENCE = [
(31,1,'Korea','The 1st Battle Group remained with the 7th Division after 1957; the later battalion served in Korea until inactivation in 1987. Exact intervening dates are not established here.',1031),
(31,2,'Korea and Fort Ord','The Korean battalion inactivated in 1971, with a later Fort Ord activation in 1974 and inactivation in 1988. The earlier 2d Battle Group at Fort Rucker became the 5th Battalion.',1031),
(31,3,'Army Reserve','The 3d Battle Group served in the Army Reserve with the 63d Infantry Division in southern California.',301),
(31,5,'Fort Rucker and Fort Benning','The former 2d Battle Group became the 5th Battalion in 1964. It later served with the 197th Infantry Brigade at Fort Benning and inactivated in 1971.',1031),
(31,6,'Vietnam, Cambodia and training','The 6th Battalion served in Vietnam in 1968-1970 and entered Cambodia in 1970. It later served as opposing forces at Fort Irwin, before reflagging in 1988.',1031),
(32,2,'Alaska and Fort Ord','The 2d Battalion activated in Alaska on 18 October 1939, before the regiment returned to active service in 1940. It later served with the 7th Division at Fort Ord.',1032),
(32,3,'Fort Ord and training','The 3d Battalion served with the 7th Division at Fort Ord, followed by training service at Fort Benning in the late 1980s and early 1990s.',1032),
(33,1,'Caribbean defense','The battalion moved to Trinidad in 1941; detachments guarded bauxite production in Surinam. It moved from Surinam to Aruba in June 1943.',1033),
(33,3,'Korean War personnel transfer','The 3d Battalion furnished personnel to the 65th Infantry during the Korean War. That transfer is not treated as a deployment of the entire 33d Infantry Regiment.',1033),
(34,2,'Mechanized service','The 2d Battalion is documented in the 1982 National Training Center account Dragons at War. A complete dated assignment lineage is not established here.',1034),
(34,3,'Corregidor and training','The wartime 3d Battalion assaulted Corregidor in February 1945. A later 3d Battalion served as a basic training organization at Fort Jackson.',1034),
(36,2,'Wartime successor','In 1947 the former 2d Battalion became the 37th Armored Infantry Battalion. Its numbered successor row appears above; this is not the separate 37th Infantry Regiment.',95),
(36,3,'Wartime successor','In 1947 the former 3d Battalion became the 13th Armored Infantry Battalion in the 3d Armored Division.',95),
(39,1,'Germany','The 1st Battalion served with the 8th Infantry Division at Baumholder during the early 1970s. Exact assignment boundaries are not established by this account.',1039),
(39,4,'Vietnam and training','The 4th Battalion served with the 9th Infantry Division in Vietnam after activation in 1966. Later training service included Fort Dix and Fort Jackson; another activation occurred in 2017.',1039),
(41,2,'Cold War mechanized infantry','The regimental account identifies four mechanized infantry battalions in the 2d Armored Division during the 1980s. Exact dates for the 2d Battalion are not established here.',1041),
(41,4,'Cold War mechanized infantry','The 4th Battalion was among the regiment\'s mechanized battalions associated with the 2d Armored Division during the 1980s. This note does not infer uninterrupted service.',1041),
(43,'ps96','Postwar successor','The 1st Battalion became the 96th Infantry Battalion on 25 October 1947. The Scout successors inactivated in May 1949 and disbanded in 1951.',303),
(43,'ps97','Postwar successor','The 2d Battalion became the 97th Infantry Battalion on 25 October 1947. Its later inactivation and disbandment followed those of the other Scout successor battalions.',303),
(43,'ps98','Postwar successor','The 3d Battalion became the 98th Infantry Battalion on 25 October 1947.',303),
(44,'wwi','13th Division','The 1917 regiment trained with the 13th Division in 1918 and did not deploy to France. Precise assignment boundaries are not established here.',1044),
(46,3,'Fort Knox training','The 3d Battalion is documented among the 46th Infantry training battalions at Fort Knox. Activation and inactivation boundaries require further evidence.',1046),
(46,4,'Domestic deployment and training','The 4th Battalion helped respond to the Chicago disorders in April 1968 and later served as a training battalion at Fort Knox.',1046),
(48,2,'Germany and training','The 2d Battalion served in the 3d Armored Division in Germany and inactivated on 15 October 1991. A training battalion was reactivated at Fort Leonard Wood in June 2017.',1048),
(49,'aib80','Armored successor','The 80th Armored Infantry Battalion descended from the regiment\'s 2d Battalion and served with the 8th Armored Division after the September 1943 breakup.',1049),
(49,'aib36','Armored successor','The 36th Armored Infantry Battalion descended from the remainder of the 49th Armored Infantry. It is distinct from the 36th Infantry Regiment\'s own similarly numbered successor.',1049),
(50,'aib50','Armored successor','The 50th Armored Infantry Battalion served with the 6th Armored Division and inactivated on 18 September 1945.',1050),
(50,'aib9','Armored successor','The former 2d Battalion became the 9th Armored Infantry Battalion in September 1943. Its 6th Armored Division service ended with inactivation on 18 September 1945.',1050),
(51,1,'Mechanized battalion','The 1st Battalion served with the 2d Armored Division after 1957, the 4th Armored Division after 1963, and the 1st Armored Division from 10 May 1971. It inactivated on 16 June 1984.',1051),
(51,'E','Long-range surveillance','Company E served in Germany as V Corps\' surveillance company from 1986. Its overseas service included Bosnia, Kosovo and Iraq; tour boundaries are not established here.',1051),
(51,'aib51','Armored and constabulary predecessor','The 51st Armored Infantry Battalion became the 51st Constabulary Squadron in May 1946.',1051),
(51,'aib53','Armored and constabulary predecessor','The regiment\'s former 1st Battalion became the 53d Armored Infantry Battalion in 1943, then a constabulary squadron in May 1946.',1051),
(54,1,'Earlier armored lineage','The original 1st Battalion became the 61st Armored Infantry Battalion in 1943, later the 561st. This is separate from the later Company B lineage used by the modern 2d Battalion.',118),
(54,3,'Earlier service','The headquarters lineage served in World War II and, after a 1966 activation, in Vietnam before inactivation in 1972. The later Army article dates its 2019 training activation to 31 July, rather than the August date in secondary accounts.',309),
(54,'aib20','Armored successor','The former 2d Battalion became the 20th Armored Infantry Battalion in September 1943, later the 520th. It belonged to the 10th Armored Division.',118),
(54,'aib54','Armored successor','The 54th Armored Infantry Battalion was another successor of the 1943 breakup. Postwar redesignations and inactive assignments are recorded in the parent certificate.',118),
(55,'aib55','Armored successor','The 55th Armored Infantry Battalion succeeded the regimental headquarters and other elements after September 1943, with the 11th Armored Division.',1055),
(55,'aib63','Armored successor','The former 1st Battalion became the 63d Armored Infantry Battalion of the 11th Armored Division.',1055),
(55,'aib21','Armored successor','The former 2d Battalion became the 21st Armored Infantry Battalion; the original 3d Battalion was disbanded.',1055),
(56,'aib66','Armored successor','The former 1st Battalion became the 66th Armored Infantry Battalion of the 12th Armored Division in November 1943.',1056),
(56,'aib17','Armored successor','The former 2d Battalion became the 17th Armored Infantry Battalion of the 12th Armored Division.',1056),
(56,'aib56','Armored successor','The former 3d Battalion became the 56th Armored Infantry Battalion of the 12th Armored Division.',1056),
(58,1,'Separate brigade','The 1st Battalion served with the separate 197th Infantry Brigade at Fort Benning in the 1960s-1980s. Exact boundaries are not established here.',1058),
(58,'D','Vietnam','Company D served separately in Vietnam under the 93d Military Police Battalion. The regimental account groups the separate companies\' service within 1966-1972 without individual tour dates.',1058),
(58,'E','Vietnam','Company E served under the 4th Infantry Division in Vietnam. Exact tour dates are not established here.',1058),
(58,'F','Vietnam','Company F served under the 101st Airborne Division (Airmobile) in Vietnam. Exact tour dates are not established here.',1058),
(59,1,'Army Reserve','The 1st Battalion served with the 191st Infantry Brigade before inactivation in 1968. The precise start and end dates are not established here.',1059),
(60,1,'Alaska','The 1st Battalion served with the separate 172d Infantry Brigade in Alaska during the 1960s-1980s. This was not a Vietnam deployment.',1060),
(60,5,'Vietnam','The mechanized 5th Battalion deployed with the 9th Division, then exchanged places with 1st Battalion, 16th Infantry in September 1968 and served with the 1st Division.',1060),
]

SERVICE = [
(32,1,'2003-2004','Iraq',90),(32,1,'2006-2007','Afghanistan',90),(32,1,'2009','Nuristan Province, Afghanistan',90),
(35,1,'1967-1968','Vietnam',302),(35,2,'1966-1967','Vietnam',94),(35,2,'1967-1969','Vietnam',94),(35,2,'1969-1970','Vietnam',94),(35,2,'2006-2007','Iraq',94),(35,2,'2008-2009','Iraq',94),
(36,1,'2004','Iraq',96),
(38,1,'2007-2008','Iraq',98),(38,1,'2009-2010','Iraq',98),(38,1,'2012-2013','Afghanistan',98),
(39,2,'1967-1969','Vietnam',99),(39,3,'1967-1969','Vietnam',100),
(41,1,'1991','Iraq and Kuwait',101),(41,1,'2004-2005','Iraq',101),(41,1,'2011-2012','Afghanistan',101),(41,1,'2014','Afghanistan',101),(41,3,'1990-1991','Saudi Arabia and Kuwait',102),
(46,1,'1969-1970','Vietnam',103),(46,1,'1971','Vietnam',103),(46,5,'1969-1970','Vietnam',105),
(47,2,'1967-1969','Vietnam',107),(47,2,'1969-1970','Vietnam',107),(47,3,'1967-1969','Vietnam',108),
(50,1,'1968-1969','Vietnam',111),(50,1,'1969-1970','Vietnam',111),
(51,'F','1990-1991','Southwest Asia',305),(51,'F','2007-2008','Iraq',305),
(52,1,'1969-1970','Vietnam',113),(52,1,'1971','Vietnam',113),
(52,'B','2008','Baghdad, Iraq',114),(52,'C','1968-1969','Vietnam',115),(52,'C','2003-2004','Iraq',115),(52,'C','2006-2007','Iraq',115),
(52,'D','1967','Vietnam',116),(52,'D','1968','Vietnam',116),(52,'D','2005','Nineveh Province, Iraq',116),(52,'D','2008-2009','Iraq',116),(52,'F','1967-1968','Vietnam',117),(52,'F','2007-2008','Iraq',117),
(60,2,'1966-1969','Vietnam',122),(60,2,'1969-1970','Vietnam',122),(60,3,'1966-1969','Vietnam',123),
]

TOURS = [
(31,0,'1918-1920','Siberia','Intervention service with the American Expeditionary Force, Siberia.'),
(31,0,'1932','Shanghai','Protection of the International Settlement during the Shanghai crisis.'),
(31,0,'1941-1942','Philippines','Defense of Luzon and Bataan, ending in surrender.'),
(31,0,'1950-1953','Korea','Combat service with the 7th Infantry Division.'),
(31,4,'2001-2002','Afghanistan','Elements participated in Afghanistan operations; this was not a single whole-battalion movement.'),
(31,4,'2003','Horn of Africa','Company C and other elements served in Djibouti and Ethiopia.'),
(31,4,'2004-2005','Iraq','Task Force 4-31 operated around Baghdad.'),
(31,4,'2006-2007','Iraq','A second task force tour south of Baghdad.'),
(31,4,'2009-2010','Iraq','Task force deployment and return to Fort Drum.'),
(31,4,'2015-2016','Afghanistan','Advising and security duties.'),
(31,4,'2018-2019','Afghanistan','Theater response force service.'),
(31,4,'2021','Kabul evacuation','Battalion elements supported the evacuation from Afghanistan.'),
(32,1,'2011-2012','Afghanistan','Operations in Zhari District, Kandahar Province, during Operation Enduring Freedom XI-XII.'),
(33,0,'1941-1944','Caribbean defense','Battalions served in Trinidad and its associated defense area; detachments also served in Surinam and Aruba.'),
(37,0,'1941-1944','Aleutian Islands','Alaska and Aleutian garrison service under the Alaskan Defense Command.'),
(41,1,'1997','Bosnia-Herzegovina','Task force peacekeeping deployment; Company B remained at Fort Riley.'),
(41,1,'2002','Kuwait','Operation Desert Spring rotation with the 3d Infantry Division; this was an operational relationship.'),
(41,1,'2003-2004','Iraq','Invasion and occupation service; companies returned at different times.'),
(41,1,'2016','Afghanistan','Bravo and Delta companies served in Kandahar; this marker concerns those companies.'),
(41,1,'2018','Afghanistan','Battalion patrols supported Task Force Southwest in Helmand.'),
(49,0,'1918-1919','France','Depot and replacement service with the 83d Division; not a claimed front-line combat campaign.'),
(51,'F','1967-1968','Vietnam','Long-range patrol service; the official lineage inactivation date is 26 December 1968.'),
(53,0,'1942-1943','Alaska and Adak','The regiment left the 7th Division and served in Alaska; precise assignment boundaries remain unresolved.'),
(57,0,'1941-1942','Philippines','Defense of the Philippines with the Philippine Division.'),
]

CAMPAIGNS = {
32:[('1943','Aleutian Islands'),('1944','Eastern Mandates and Leyte'),('1945','Ryukyus'),('1950-1953','Korean War')],
34:[('1918','Lorraine'),('1944-1945','New Guinea and the Philippines'),('1950','Defense of Korea'),('1951','Korea: summer-fall campaign'),('1953','Korea: summer campaign')],
35:[('1941-1945','Central Pacific, Solomons and Luzon'),('1950-1953','Korean War')],
36:[('1944-1945','Western Europe')],
38:[('1918','France'),('1944-1945','Western Europe'),('1950-1953','Korean War')],
39:[('1918','France'),('1942-1943','North Africa and Sicily'),('1944-1945','Western Europe')],
41:[('1942-1943','North Africa and Sicily'),('1944-1945','Western Europe')],
45:[('1941-1942','Philippine Islands')],
47:[('1918','France'),('1942-1943','North Africa and Sicily'),('1944-1945','Western Europe')],
51:[('1918','France')],52:[('1918','France')],53:[('1918','France')],54:[('1918','France')],55:[('1918','Lorraine')],56:[('1918','Lorraine')],58:[('1918','France')],59:[('1918','France')],
60:[('1918','France'),('1942-1943','North Africa and Sicily'),('1944-1945','Western Europe')],
}

OPERATIONS = [
(43,1,'1941-1942','Philippines','Detachments fought in northern Luzon and Mindanao. Some survivors continued as guerrillas after the organized surrender.',303),
(46,'aib47','1944-1945','Western Europe','Company A predecessor lineage records Normandy, Northern France, Rhineland, Ardennes-Alsace and Central Europe campaigns.',103),
(46,'aib15','1944-1945','Western Europe','The Company E predecessor lineage records five western European campaigns with the 5th Armored Division.',105),
(48,'aib38','1944-1945','Western Europe','The Company A lineage records western European campaigns, including the fighting at St. Vith.',110),
(48,'aib48','1944','Vielsalm, Belgium','The 48th Armored Infantry Battalion fought at the Salm River during the Ardennes offensive.',1048),
(49,'aib58','1944-1945','Western Europe','The annexed Company B, 49th Infantry lineage earned Rhineland and Central Europe credit as part of the 58th Armored Infantry Battalion.',120),
(50,'aib44','1944-1945','Western Europe','The Company A predecessor lineage records Normandy, Northern France, Rhineland, Ardennes-Alsace and Central Europe service.',111),
(51,'F','1944-1945','Western Europe','Company F\'s predecessor served as Company C, 10th Armored Infantry Battalion, in the 4th Armored Division.',305),
(52,1,'1944-1945','Western Europe','The predecessor Company A, 60th Armored Infantry Battalion, served with the 9th Armored Division.',113),
(54,2,'1944-1945','Western Europe','Company B of the 61st Armored Infantry Battalion earned Rhineland, Ardennes-Alsace and Central Europe campaign credit.',119),
(59,'aib59','1945','Germany','The 59th Armored Infantry Battalion fought with the 13th Armored Division in the Rhineland and Central Europe campaigns.',1059),
]

# Successor coverage through the end of the European war; not inactivation dates.
SOURCES[311] = ('https://eucmh.com/2021/03/04/11th-armored-division-ww-2/', 'ETO Theater Historian: 11th Armored Division order of battle, reproduced by EUCMH')
SOURCES[312] = ('https://dpaa-mil.sites.crmforce.mil/dpaaProfile?id=a0Jt000001nzWRBEA2', 'Defense POW/MIA Accounting Agency: Paul A. Kling and the Herrlisheim fighting')
for reg, elements, start, div, sid in [(55, (55,63,21), '1943-09-20', 'a11', 1055), (56, (66,17,56), '1943-11-11', 'a12', 1056)]:
    for element in elements:
        ROWS.append((reg, 'aib'+str(element), sid, start+' '+div+';1945-05-09 end'))
    NOTES[reg] = 'The armored successor rows cover formation through the end of the European war on 8 May 1945. Their closing boundary is a coverage limit, not an inactivation date; later service is not established here.'
EVIDENCE = [entry for entry in EVIDENCE if entry[0] not in (55,56)]
for element in (55,63,21):
    OPERATIONS.append((55,'aib'+str(element),'1944-1945','Western Europe','Served in the 11th Armored Division during its European campaign. The division arrived in France in December 1944 and entered Germany in March 1945.',311))
for element in (17,66):
    OPERATIONS.append((56,'aib'+str(element),'1945','Herrlisheim, France','The battalion participated in the January fighting to retake Herrlisheim with the 12th Armored Division.',312))
