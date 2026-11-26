#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
parse_encounters.py
Extraction, normalization, and export script for the encounter database
of Luminescent Platinum (https://github.com/TeamLumi/luminescent-team).

Exports to:
- luminescent_encounters.json
- luminescent_encounters.csv
"""

import os
import re
import csv
import sys
import json
from collections import Counter

from conditions_i18n import normalize_bilingual_condition
from i18n_cli import resolve_cli_lang, t

# Ensure UTF-8 stdout on Windows console
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Base data paths
GAMEDATA_DIR = os.path.join("lumi-repo", "__gamedata", "gamedata2.0")
DOCS_SPECIAL_DIR = os.path.join("lumi-repo", "docs", "special-events")
MONS_NAME_FILE = os.path.join(GAMEDATA_DIR, "english_ss_monsname.json")
POKEMON_LOC_TXT = os.path.join(GAMEDATA_DIR, "pokemon_locations.txt")
STATIC_LOC_JSON = os.path.join(GAMEDATA_DIR, "static_pokemon_locations.json")
ENCOUNTER_LOC_JSON = os.path.join(GAMEDATA_DIR, "encounter_locations.json")

OUTPUT_JSON = "luminescent_encounters.json"
OUTPUT_CSV = "luminescent_encounters.csv"


def load_dex_id_mapper():
    """Load Pokémon Name -> National Dex ID mapping table."""
    base_map = {}
    if os.path.exists(MONS_NAME_FILE):
        with open(MONS_NAME_FILE, "r", encoding="utf-8") as f:
            mons_data = json.load(f)
        for item in mons_data.get("labelDataArray", []):
            idx = item.get("arrayIndex")
            name = item.get("wordDataArray", [{}])[0].get("str")
            if name and name not in base_map:
                base_map[name] = idx

    # Expanded Pokédex additions and regional/clone forms
    extra_dex = {
        "Litwick": 607,
        "Lampent": 608,
        "Chandelure": 609,
        "Pikipek": 731,
        "Trumbeak": 732,
        "Toucannon": 733,
        "Tinkatink": 957,
        "Tinkatuff": 958,
        "Tinkaton": 959,
        "Galarian Farfetch'd": 83,
        "Gastrodon East Sea": 423,
        "Shellos East Sea": 422,
        "Clone Venusaur": 3,
        "Clone Charizard": 6,
        "Clone Blastoise": 9,
        "Clone Pikachu": 25,
        "Stitched Gengar": 94,
        "Crystal Onix": 95,
        "Spiky-eared Pichu": 172,
    }
    base_map.update(extra_dex)

    def get_id(name: str):
        if not name:
            return None
        if name in base_map:
            return base_map[name]

        # Handle form prefixes/suffixes
        clean = re.sub(
            r"^(Alolan|Galarian|Hisuian|Clone|Stitched|Crystal|Spiky-eared)\s+",
            "",
            name,
        )
        clean = re.sub(
            r"\s*\((Before|After|East Sea|West Sea|Sandy|Trash|Plant)\)", "", clean
        )
        clean = clean.replace("East Sea ", "").replace("West Sea ", "")

        if clean in base_map:
            return base_map[clean]

        if "Nidoran" in name:
            return 29 if "F" in name else 32

        return None

    return get_id


def load_level_ranges():
    """Map (routeName, pokemonName) -> (minLevel, maxLevel) from RomFS."""
    ranges = {}
    if os.path.exists(ENCOUNTER_LOC_JSON):
        with open(ENCOUNTER_LOC_JSON, "r", encoding="utf-8") as f:
            encounter_locations_data = json.load(f)
        for _, encounters in encounter_locations_data.items():
            for encounter in encounters:
                route = encounter.get("routeName")
                mon = encounter.get("pokemonName")
                min_lvl = encounter.get("minLevel")
                max_lvl = encounter.get("maxLevel")
                if route and mon and min_lvl is not None and max_lvl is not None:
                    key = (route, mon)
                    if key not in ranges:
                        ranges[key] = (min_lvl, max_lvl)
                    else:
                        prev_min, prev_max = ranges[key]
                        ranges[key] = (min(prev_min, min_lvl), max(prev_max, max_lvl))
    return ranges


def parse_mdx_special_events():
    """Extract instructions and conditions from MDX files in docs/special-events/."""
    conditions = {}
    mdx_files = [
        "static.mdx",
        "gifts.mdx",
        "legendaries.mdx",
        "trade.mdx",
    ]
    for filename in mdx_files:
        path = os.path.join(DOCS_SPECIAL_DIR, filename)
        if not os.path.exists(path):
            continue

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        rows = re.findall(r"<tr>(.*?)</tr>", content, re.DOTALL)
        for row in rows:
            if "<th" in row:
                continue

            name_match = re.search(
                r"<h3[^>]*>.*?<span class=\"heading-text\">(?:&emsp;)?([^<]+)</span>",
                row,
                re.DOTALL,
            )
            if not name_match:
                name_match = re.search(
                    r"<h3[^>]*>\s*(?:&emsp;)?\s*([A-Za-z0-9\s\'\.\(\)-]+?)\s*</h3>",
                    row,
                    re.DOTALL,
                )

            id_match = re.search(r'<h3 id="([^"]+)"', row)

            lis = re.findall(r"<li>(.*?)</li>", row, re.DOTALL)
            clean_lis = [re.sub(r"<[^>]+>", "", li).strip() for li in lis]
            text = " ".join(clean_lis).replace("\n", " ")
            text = re.sub(r"\s+", " ", text).strip()

            if name_match:
                mon_name = name_match.group(1).strip()
                conditions[mon_name.lower()] = text
            if id_match:
                slug = id_match.group(1).lower()
                conditions[slug] = text

    return conditions


def main():
    lang = resolve_cli_lang()

    if not os.path.exists(GAMEDATA_DIR):
        print(t("parse_missing_dir", lang, dir=GAMEDATA_DIR))
        sys.exit(1)

    print(t("parse_starting", lang))

    get_dex_id = load_dex_id_mapper()
    level_ranges = load_level_ranges()
    mdx_conditions = parse_mdx_special_events()

    records = []

    # 1. Process wild route encounters (pokemon_locations.txt)
    if os.path.exists(POKEMON_LOC_TXT):
        with open(POKEMON_LOC_TXT, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                mon_name = parts[0]
                locs = parts[1:]
                if locs and locs[-1] == "":
                    locs = locs[:-1]

                for i in range(0, len(locs) - 1, 4):
                    if i + 3 >= len(locs):
                        break
                    route_name = locs[i]
                    raw_method = locs[i + 1]
                    raw_level = locs[i + 2]
                    raw_rate = locs[i + 3]

                    # Determine level range
                    key = (route_name, mon_name)
                    if key in level_ranges:
                        min_lvl, max_lvl = level_ranges[key]
                        levels_str = f"{min_lvl}-{max_lvl}" if min_lvl != max_lvl else str(min_lvl)
                    else:
                        levels_str = str(raw_level)

                    # Standardized method & default English condition
                    conditions_raw = "None"
                    if raw_method in ("Grass", "Morning", "day", "night", "Daily Trophy Garden"):
                        method = "Walking"
                        if raw_method == "Daily Trophy Garden":
                            conditions_raw = "Daily Trophy Garden"
                    elif raw_method == "Swarm":
                        method = "Walking"
                        conditions_raw = "Daily Swarm"
                    elif raw_method == "Surfing":
                        method = "Surfing"
                        conditions_raw = "Requires Surf (HM03)"
                    elif raw_method in ("Incense", "Surfing Incense"):
                        method = "Incense"
                        if raw_method == "Surfing Incense":
                            conditions_raw = "Requires Incense Burner on water"
                        else:
                            conditions_raw = "Requires Incense Burner"
                    elif raw_method in ("Old Rod", "Good Rod", "Super Rod", "Radar", "Honey Tree"):
                        method = raw_method
                        if raw_method == "Radar":
                            conditions_raw = "Requires Poké Radar"
                        elif "Rod" in raw_method:
                            conditions_raw = f"Requires {raw_method}"
                        elif raw_method == "Honey Tree":
                            conditions_raw = "Honey Tree"
                    else:
                        method = raw_method

                    # Determine time_of_day
                    if raw_method == "Morning":
                        time_of_day = ["Morning"]
                        if conditions_raw == "None":
                            conditions_raw = "Available only in the morning (04:00 - 09:59)"
                    elif raw_method == "day":
                        time_of_day = ["Day"]
                        if conditions_raw == "None":
                            conditions_raw = "Available only during the day (10:00 - 19:59)"
                    elif raw_method == "night":
                        time_of_day = ["Night"]
                        if conditions_raw == "None":
                            conditions_raw = "Available only at night (20:00 - 03:59)"
                    else:
                        time_of_day = ["Morning", "Day", "Night"]

                    cond_en, cond_pt = normalize_bilingual_condition(conditions_raw)

                    records.append({
                        "id": get_dex_id(mon_name),
                        "pokemon": mon_name,
                        "location": route_name,
                        "method": method,
                        "rate": raw_rate,
                        "levels": levels_str,
                        "time_of_day": time_of_day,
                        "version": "All",
                        "conditions": cond_en,
                        "conditions_pt": cond_pt,
                    })

    # 2. Process special events (static_pokemon_locations.json + MDX)
    if os.path.exists(STATIC_LOC_JSON):
        with open(STATIC_LOC_JSON, "r", encoding="utf-8") as f:
            static_data = json.load(f)

        for mon_name, loc_list in static_data.items():
            for loc in loc_list:
                enc_type = loc.get("encounterType", "")
                route_name = loc.get("routeName", "")
                rate_str = loc.get("encounterRate", "100%")
                min_lvl = loc.get("minLevel")
                max_lvl = loc.get("maxLevel")
                link = loc.get("link", "")

                if min_lvl is not None and max_lvl is not None:
                    levels_str = f"{min_lvl}-{max_lvl}" if min_lvl != max_lvl else str(min_lvl)
                elif min_lvl is not None:
                    levels_str = str(min_lvl)
                else:
                    levels_str = "???"

                if enc_type in ("Gifts", "Starter"):
                    method = "Gift"
                elif enc_type in ("Static", "Legendaries"):
                    method = "Static"
                elif enc_type == "Trade":
                    method = "Trade"
                elif enc_type == "Walking":
                    method = "Walking"
                else:
                    method = enc_type

                # Lookup detailed conditions in MDX files via link anchor or name
                condition_text = None
                if link and "#" in link:
                    anchor = link.split("#")[-1].lower()
                    condition_text = mdx_conditions.get(anchor)

                if not condition_text:
                    condition_text = mdx_conditions.get(mon_name.lower())

                if not condition_text:
                    if enc_type == "Starter":
                        condition_text = "Starter Pokémon choice"
                    elif enc_type == "Legendaries":
                        condition_text = "Legendary Pokémon encounter"
                    elif enc_type == "Trade":
                        condition_text = "In-game trade with NPC"
                    elif enc_type == "Gifts":
                        condition_text = "NPC Gift / Received Egg"
                    elif enc_type == "Static":
                        condition_text = "Static overworld encounter / One-time interaction"
                    else:
                        condition_text = "None"

                cond_en, cond_pt = normalize_bilingual_condition(condition_text)

                records.append({
                    "id": get_dex_id(mon_name),
                    "pokemon": mon_name,
                    "location": route_name,
                    "method": method,
                    "rate": rate_str,
                    "levels": levels_str,
                    "time_of_day": ["Morning", "Day", "Night"],
                    "version": "All",
                    "conditions": cond_en,
                    "conditions_pt": cond_pt,
                })

    if not records:
        print(t("parse_no_records", lang))
        sys.exit(1)

    # Export JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    # Also regenerate luminescent_pokedex.json if generate_pokedex.py is present
    try:
        from generate_pokedex import build_pokedex, OUTPUT_POKEDEX_JSON
        dex_records = build_pokedex(OUTPUT_POKEDEX_JSON, OUTPUT_JSON)
        print(f"  - Pokédex JSON: {OUTPUT_POKEDEX_JSON} ({len(dex_records)} entries)")
    except Exception as exc:
        print(f"  [WARN] Could not regenerate Pokédex JSON: {exc}")

    # Export CSV
    fieldnames = [
        "id",
        "pokemon",
        "location",
        "method",
        "rate",
        "levels",
        "time_of_day",
        "version",
        "conditions",
        "conditions_pt",
    ]
    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in records:
            row = dict(r)
            row["time_of_day"] = json.dumps(r["time_of_day"], ensure_ascii=False)
            writer.writerow(row)

    # Statistics and Reports
    total_records = len(records)
    time_of_day_counter = Counter()
    null_report = []

    for idx, record in enumerate(records):
        tod = tuple(record["time_of_day"])
        if tod == ("Morning",):
            time_of_day_counter[t("parse_tod_morning", lang)] += 1
        elif tod == ("Day",):
            time_of_day_counter[t("parse_tod_day", lang)] += 1
        elif tod == ("Night",):
            time_of_day_counter[t("parse_tod_night", lang)] += 1
        elif len(tod) == 3:
            time_of_day_counter[t("parse_tod_any", lang)] += 1
        else:
            time_of_day_counter[t("parse_tod_other", lang, tod=tod)] += 1

        null_fields = [key for key, value in record.items() if value is None or value == ""]
        if not record.get("time_of_day"):
            null_fields.append("time_of_day")

        if null_fields:
            null_report.append((idx, record.get("pokemon"), record.get("location"), null_fields))

    print("\n" + "=" * 60)
    print(t("parse_report_title", lang))
    print("=" * 60)
    print(t("parse_total_exported", lang, total=total_records))
    print(t("parse_files_saved", lang))
    print(f"  - JSON: {OUTPUT_JSON}")
    print(f"  - CSV:  {OUTPUT_CSV}")

    print(t("parse_tod_section", lang))
    for period, count in time_of_day_counter.items():
        pct = (count / total_records) * 100
        print(f"  {period:<40}: {count:>5} ({pct:>5.1f}%)")

    print(t("parse_methods_section", lang))
    method_counter = Counter(record["method"] for record in records)
    for method_name, method_count in method_counter.most_common():
        print(f"  {method_name:<20}: {method_count:>5}")

    print(t("parse_validation_section", lang))
    if not null_report:
        print(t("parse_validation_ok_time", lang))
        print(t("parse_validation_ok_nulls", lang))
    else:
        print(t("parse_validation_warn", lang, count=len(null_report)))
        for entry in null_report[:10]:
            print(
                t(
                    "parse_validation_entry",
                    lang,
                    idx=entry[0],
                    pokemon=entry[1],
                    location=entry[2],
                    fields=entry[3],
                )
            )
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
