from __future__ import annotations

import json
import re
import unicodedata
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parent
WORKBOOK_PATH = ROOT / "Soviet Force Structure 1989.xlsx"
OUTPUT_PATH = ROOT / "soviet-bases-data.json"

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
STRUCTURAL_FIELDS = {
    "Force",
    "Country",
    "Country_2",
    "Location Name",
    "Barracks",
    "lat/lon comb",
    "latitude",
    "longitude",
    "UIC",
    "CO",
    "CO Type",
    "BN",
    "BN Type",
    "RGT",
    "RGT Type",
    "BDE",
    "BDE Type",
    "DIV",
    "DIV Type",
    "CPS",
    "CPS Type",
    "ARM",
    "ARM Type",
    "MD",
}
FORMATION_SUFFIXES = {
    "BN": "Battalion",
    "RGT": "Regiment",
    "BDE": "Brigade",
    "DIV": "Division",
    "CPS": "Corps",
}
GROUP_DISTANCE_THRESHOLD = 0.05
MAX_FORMATIONS_PER_BASE = 24
MAX_REGIMENTS_PER_BASE = 12


def normalise_text(value: str | None) -> str:
    return " ".join((value or "").split()).strip()


def slugify(value: str) -> str:
    ascii_value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_value).strip("-").lower()
    return slug or "base"


def extract_numbers(text: str | None) -> list[float]:
    if not text:
        return []
    return [float(match) for match in re.findall(r"-?\d+(?:\.\d+)?", text)]


def parse_coordinate_pair(record: dict[str, str]) -> tuple[float | None, float | None]:
    latitude = extract_numbers(record.get("latitude"))
    longitude = extract_numbers(record.get("longitude"))
    combined = extract_numbers(record.get("lat/lon comb"))

    lat = latitude[0] if latitude else None
    lon = longitude[0] if longitude else None

    if lat is None and len(combined) >= 1:
        lat = combined[0]
    if lon is None and len(combined) >= 2:
        lon = combined[1]

    return lat, lon


def parse_int(value: str | None) -> int:
    if not value:
        return 0
    numbers = extract_numbers(value)
    if not numbers:
        return 0
    return int(round(numbers[0]))


def load_shared_strings(archive: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []

    root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    shared_strings: list[str] = []

    for si in root.findall("m:si", NS):
        text = "".join(node.text or "" for node in si.iterfind(".//m:t", NS))
        shared_strings.append(text)

    return shared_strings


def cell_text(cell: ET.Element, shared_strings: list[str]) -> str:
    cell_type = cell.attrib.get("t")
    value_node = cell.find("m:v", NS)

    if cell_type == "inlineStr":
        return "".join(node.text or "" for node in cell.iterfind(".//m:t", NS))
    if value_node is None:
        return ""

    value = value_node.text or ""
    if cell_type == "s" and value:
        return shared_strings[int(value)]
    return value


def unique_headers(row: ET.Element, shared_strings: list[str]) -> dict[str, str]:
    counts: dict[str, int] = {}
    headers: dict[str, str] = {}

    for cell in row.findall("m:c", NS):
        column = "".join(char for char in cell.attrib.get("r", "") if char.isalpha())
        raw_header = cell_text(cell, shared_strings)
        counts[raw_header] = counts.get(raw_header, 0) + 1
        header = raw_header if counts[raw_header] == 1 else f"{raw_header}_{counts[raw_header]}"
        headers[column] = header

    return headers


def load_records() -> tuple[list[dict[str, str]], list[str]]:
    with zipfile.ZipFile(WORKBOOK_PATH) as archive:
        shared_strings = load_shared_strings(archive)
        worksheet = ET.fromstring(archive.read("xl/worksheets/sheet1.xml"))
        rows = worksheet.findall("m:sheetData/m:row", NS)
        headers = unique_headers(rows[0], shared_strings)

        records: list[dict[str, str]] = []
        for row in rows[1:]:
            record: dict[str, str] = {}
            for cell in row.findall("m:c", NS):
                column = "".join(char for char in cell.attrib.get("r", "") if char.isalpha())
                record[headers.get(column, column)] = cell_text(cell, shared_strings)
            if record:
                records.append(record)

    ordered_headers = [value for _, value in sorted(headers.items())]
    return records, ordered_headers


def is_same_site(group: dict, latitude: float | None, longitude: float | None) -> bool:
    if latitude is None or longitude is None:
        return True
    if group["latitude"] is None or group["longitude"] is None:
        return True
    return (
        abs(group["latitude"] - latitude) <= GROUP_DISTANCE_THRESHOLD
        and abs(group["longitude"] - longitude) <= GROUP_DISTANCE_THRESHOLD
    )


def add_unique(items: list[str], seen: set[str], value: str) -> None:
    cleaned = normalise_text(value)
    if not cleaned or cleaned in seen:
        return
    seen.add(cleaned)
    items.append(cleaned)


def format_echelon(number: str | None, unit_type: str | None, suffix: str | None) -> str:
    parts = [normalise_text(number), normalise_text(unit_type)]
    label = " ".join(part for part in parts if part)
    if suffix and label:
        return f"{label} {suffix}"
    return label


def formation_line(record: dict[str, str]) -> str:
    parts = []

    for key, suffix in FORMATION_SUFFIXES.items():
        label = format_echelon(record.get(key), record.get(f"{key} Type"), suffix)
        if label:
            parts.append(label)

    arm_label = " ".join(
        part for part in [normalise_text(record.get("ARM")), normalise_text(record.get("ARM Type"))] if part
    )
    if arm_label:
        parts.append(arm_label)

    md_label = normalise_text(record.get("MD"))
    if md_label:
        parts.append(md_label)

    return " | ".join(parts)


def lowest_formation_type(record: dict[str, str]) -> str:
    for key in ("BN Type", "RGT Type", "BDE Type", "DIV Type", "CPS Type", "ARM Type"):
        value = normalise_text(record.get(key))
        if value:
            return value
    return ""


def equipment_columns(headers: list[str]) -> list[str]:
    return [header for header in headers if header and header not in STRUCTURAL_FIELDS]


def new_group(record: dict[str, str], display_name: str, location_name: str, latitude: float | None, longitude: float | None) -> dict:
    return {
        "name": display_name,
        "locationName": location_name,
        "force": normalise_text(record.get("Force")),
        "operatorCountry": normalise_text(record.get("Country")),
        "hostCountry": normalise_text(record.get("Country_2") or record.get("Country")),
        "latitude": latitude,
        "longitude": longitude,
        "coordSumLat": latitude or 0.0,
        "coordSumLon": longitude or 0.0,
        "coordCount": 1 if latitude is not None and longitude is not None else 0,
        "rowCount": 0,
        "militaryDistricts": [],
        "militaryDistrictsSeen": set(),
        "armies": [],
        "armiesSeen": set(),
        "corps": [],
        "corpsSeen": set(),
        "divisions": [],
        "divisionsSeen": set(),
        "brigades": [],
        "brigadesSeen": set(),
        "regiments": [],
        "regimentsSeen": set(),
        "formationLines": [],
        "formationLinesSeen": set(),
        "formationTypeCounts": Counter(),
        "equipmentTotals": Counter(),
    }


def merge_record(group: dict, record: dict[str, str], equipment_headers: list[str]) -> None:
    latitude, longitude = parse_coordinate_pair(record)
    if latitude is not None and longitude is not None:
        if group["latitude"] is None or group["longitude"] is None:
            group["latitude"] = latitude
            group["longitude"] = longitude
        group["coordSumLat"] += latitude
        group["coordSumLon"] += longitude
        group["coordCount"] += 1

    group["rowCount"] += 1

    add_unique(group["militaryDistricts"], group["militaryDistrictsSeen"], record.get("MD", ""))

    add_unique(
        group["armies"],
        group["armiesSeen"],
        " ".join(
            part for part in [normalise_text(record.get("ARM")), normalise_text(record.get("ARM Type"))] if part
        ),
    )
    add_unique(
        group["corps"],
        group["corpsSeen"],
        format_echelon(record.get("CPS"), record.get("CPS Type"), "Corps"),
    )
    add_unique(
        group["divisions"],
        group["divisionsSeen"],
        format_echelon(record.get("DIV"), record.get("DIV Type"), "Division"),
    )
    add_unique(
        group["brigades"],
        group["brigadesSeen"],
        format_echelon(record.get("BDE"), record.get("BDE Type"), "Brigade"),
    )
    add_unique(
        group["regiments"],
        group["regimentsSeen"],
        format_echelon(record.get("RGT"), record.get("RGT Type"), "Regiment"),
    )
    add_unique(group["formationLines"], group["formationLinesSeen"], formation_line(record))

    lowest_type = lowest_formation_type(record)
    if lowest_type:
        group["formationTypeCounts"][lowest_type] += 1

    for header in equipment_headers:
        count = parse_int(record.get(header))
        if count > 0:
            group["equipmentTotals"][header] += count


def build_groups(records: list[dict[str, str]], headers: list[str]) -> list[dict]:
    by_key: defaultdict[tuple[str, str, str, str], list[dict]] = defaultdict(list)
    equipment_headers = equipment_columns(headers)

    for record in records:
        display_name = normalise_text(record.get("Barracks") or record.get("Location Name"))
        location_name = normalise_text(record.get("Location Name") or record.get("Barracks"))
        if not display_name:
            continue

        latitude, longitude = parse_coordinate_pair(record)
        key = (
            display_name.lower(),
            location_name.lower(),
            normalise_text(record.get("Country")),
            normalise_text(record.get("Country_2") or record.get("Country")),
        )

        group = None
        for existing in by_key[key]:
            if is_same_site(existing, latitude, longitude):
                group = existing
                break

        if group is None:
            group = new_group(record, display_name, location_name, latitude, longitude)
            by_key[key].append(group)

        merge_record(group, record, equipment_headers)

    groups = [group for bucket in by_key.values() for group in bucket]
    groups.sort(key=lambda item: (item["name"].lower(), item["locationName"].lower(), item["hostCountry"].lower()))
    return groups


def finalise_groups(groups: list[dict]) -> list[dict]:
    slug_counts: Counter[str] = Counter()
    final_groups: list[dict] = []

    for group in groups:
        if group["coordCount"]:
            group["latitude"] = round(group["coordSumLat"] / group["coordCount"], 6)
            group["longitude"] = round(group["coordSumLon"] / group["coordCount"], 6)

        slug_base = slugify("-".join(part for part in [group["name"], group["locationName"], group["hostCountry"]] if part))
        slug_counts[slug_base] += 1
        group_id = slug_base if slug_counts[slug_base] == 1 else f"{slug_base}-{slug_counts[slug_base]}"

        top_equipment = [
            {"name": name, "count": count}
            for name, count in sorted(group["equipmentTotals"].items(), key=lambda item: (-item[1], item[0]))[:12]
        ]
        formation_types = [
            {"name": name, "count": count}
            for name, count in sorted(group["formationTypeCounts"].items(), key=lambda item: (-item[1], item[0]))[:8]
        ]

        final_groups.append(
            {
                "id": group_id,
                "name": group["name"],
                "locationName": group["locationName"],
                "force": group["force"],
                "operatorCountry": group["operatorCountry"],
                "hostCountry": group["hostCountry"],
                "latitude": group["latitude"],
                "longitude": group["longitude"],
                "rowCount": group["rowCount"],
                "militaryDistricts": group["militaryDistricts"],
                "armies": group["armies"],
                "corps": group["corps"],
                "divisions": group["divisions"],
                "brigades": group["brigades"],
                "regiments": group["regiments"][:MAX_REGIMENTS_PER_BASE],
                "formationTypes": formation_types,
                "formations": group["formationLines"][:MAX_FORMATIONS_PER_BASE],
                "formationOverflow": max(0, len(group["formationLines"]) - MAX_FORMATIONS_PER_BASE),
                "equipmentTotals": top_equipment,
            }
        )

    return final_groups


def build_payload() -> dict:
    records, headers = load_records()
    groups = finalise_groups(build_groups(records, headers))

    host_countries = sorted({group["hostCountry"] for group in groups if group["hostCountry"]})
    military_districts = sorted(
        {district for group in groups for district in group["militaryDistricts"] if district}
    )

    return {
        "summary": {
            "recordCount": len(records),
            "baseCount": len(groups),
            "mappedBaseCount": sum(1 for group in groups if group["latitude"] is not None and group["longitude"] is not None),
            "hostCountryCount": len(host_countries),
            "militaryDistrictCount": len(military_districts),
        },
        "filters": {
            "hostCountries": host_countries,
            "militaryDistricts": military_districts,
        },
        "bases": groups,
    }


def main() -> None:
    payload = build_payload()
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH} with {payload['summary']['baseCount']} aggregated bases.")


if __name__ == "__main__":
    main()
