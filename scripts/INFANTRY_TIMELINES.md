# Infantry timeline series

The site serves static HTML. The 26th Infantry page is the hand-edited format
reference; the generator creates the other 199 pages and adds navigation links.

```powershell
python scripts/build_infantry_timelines.py
# Rebuild only the second group, preserving generated content for 1-30:
python scripts/build_infantry_timelines.py --start 31 --end 60
# Rebuild the third group:
python scripts/build_infantry_timelines.py --start 61 --end 100
# Rebuild the remaining site regiments:
python scripts/build_infantry_timelines.py --start 101 --end 200
python scripts/check_infantry_timelines.py --browser
```

The builder requires `beautifulsoup4`. Browser validation additionally requires
`selenium` and Chrome. Neither is required by website visitors.

Edit the reviewed data before regenerating:

- `infantry_timeline_data.py`: effective assignment and status transitions.
- `infantry_timeline_sources.json`: Army lineage source URLs.
- `infantry_timeline_supplements.py`: later changes, additional battalions and
  sources with incomplete dates.
- `infantry_timeline_events.py`: selected operations and credited service years.
- `infantry_timeline_data_31_60.py`: reviewed assignments, companies, armored
  predecessors, selected deployments and evidence notes for regiments 31-60.
- `infantry_timeline_data_61_100.py`: the next forty numbered pages, with
  separately named lineages, month-only coverage windows and numbering records.
- `infantry_timeline_sources_61_100.json`: additional Army lineage certificates.
- `infantry_timeline_data_101_200.py`: remaining regiments, distinct reused
  identities, National Guard battalions and selected deployments.
- `infantry_timeline_sources_101_200.json`: additional Army lineage certificates.
- `infantry_timeline_patches.json`: local artwork and original Commons filenames.

The generator reads the current 26th page each time. It does not replace its
historical content. Hand edits to the other generated timeline pages will be
replaced on the next build. Shared CSS and JavaScript apply to all 200 pages.

Dates have exclusive ends. The final open interval explicitly means **last
documented**, not independently verified continuous service through the page
cutoff. An unknown interval does not imply inactivity. Company lineage,
regimental service, division assignment and temporary operational attachment
are distinct. Award/campaign years must not be presented as exact tour dates.
Inactive paper assignments retain their division label while remaining inactive.
Month- or year-only transitions use uncertainty windows rather than guessed days.
Approximate wartime affiliation windows in the 101–200 group are labeled in
cards, charts and date results. They identify evidence coverage, not effective
assignment dates or confirmed membership on every day within the interval.
Historical successor coverage may close at the end of its documented period;
that boundary is not an inactivation date unless the source establishes it.

Battalion notes are included when sources establish service but not complete
assignment boundaries. Existing artwork-only placeholders are not treated as
evidence of additional battalion lineages. Each page identifies this scope.

Patch artwork is stored locally, using SVG originals or Wikimedia's PNG
renditions. Source file and license links appear on the pages. The 1st Armored
Division artwork is by Noclador, CC BY-SA 4.0; no artwork edits were made.
The 45th Infantry Division vector is by Stannered, used under CC BY 2.5.
The 31st Division SVG has its missing default XML namespace restored for
browser compatibility; its artwork is unchanged.

Checks cover all local assets/links, source anchors, accessibility references,
date ordering, overlap within each unit, every unit filter, five date lookups,
deployment buttons, bookmarks, mobile layout and static content without JS.

Numbers 92-100 were not constituted as Regular Army infantry regiments. Their
pages explicitly describe the numbering gap and distinguish separate battalions
(including the 99th, 100th and Philippine Scout battalions 96-98). Reused
numbers, notably 69, 71, 74, 75, 87 and 88, are not treated as continuous lineages.
The 91st page identifies an archival record but leaves its assignment chronology
unresolved rather than borrowing the history of a similarly numbered division.
The 177th and 189th–192d entries retain unresolved regimental identity notices;
similarly numbered brigades and training institutes are not silently substituted.
