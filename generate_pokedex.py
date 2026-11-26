#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_pokedex.py
Builds luminescent_pokedex.json containing ALL obtainable Pokémon in
Pokémon Luminescent Platinum (513 base species + Regional forms + Lumi Special forms),
including types, sprite metadata, catchability, and bilingual (EN/PT) evolution trees.

Reads from local ./lumi-repo/__gamedata/gamedata2.0 if available, otherwise
fetches directly from TeamLumi/luminescent-team on GitHub.
"""

import json
import os
import sys
import urllib.request

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

GAMEDATA_DIR = os.path.join("lumi-repo", "__gamedata", "gamedata2.0")
GITHUB_RAW_GAMEDATA = (
    "https://raw.githubusercontent.com/TeamLumi/luminescent-team/main/__gamedata/gamedata2.0"
)
TEAM_LUMI_SPRITE_BASE = (
    "https://raw.githubusercontent.com/TeamLumi/luminescent-team/main/static/img/pkm"
)

ENCOUNTERS_JSON = "luminescent_encounters.json"
OUTPUT_POKEDEX_JSON = "luminescent_pokedex.json"

# Special alternate PersonalTable IDs included as standalone Pokédex entries:
# - Lumi Special Forms: Clone Venusaur (1013), Clone Charizard (1017), Clone Blastoise (1020),
#   Clone Pikachu (1043), Stitched Gengar (1073), Crystal Onix (1074), Spiky-eared Pichu (1103)
# - East Sea Forms (present in luminescent_encounters.json): Shellos East Sea (1177), Gastrodon East Sea (1178)
INCLUDED_SPECIAL_PERSONAL_IDS = {
    1013: ("Clone Venusaur", "special"),
    1017: ("Clone Charizard", "special"),
    1020: ("Clone Blastoise", "special"),
    1043: ("Clone Pikachu", "special"),
    1073: ("Stitched Gengar", "special"),
    1074: ("Crystal Onix", "special"),
    1103: ("Spiky-eared Pichu", "special"),
    1177: ("Shellos East Sea", "special"),
    1178: ("Gastrodon East Sea", "special"),
}

# Exact canonical name overrides to match luminescent_encounters.json 1-to-1
CANONICAL_NAME_OVERRIDES = {
    29: "Nidoran-F",
    32: "Nidoran-M",
    1067: "Galarian Farfetch'd",
    1103: "Spiky-eared Pichu",
    1177: "Shellos East Sea",
    1178: "Gastrodon East Sea",
}

LUMI_TO_RELUMI_PIKACHU_FORMS = {
    7: 7,
    8: 7,
    9: 7,
    10: 7,
    11: 7,
    12: 7,
    13: 7,
    14: 7,
    15: 8,
    16: 9,
    17: 10,
}

# Special non-evolution, non-wild acquisition notes (e.g. breeding / post-game quest)
SPECIAL_OBTAIN_NOTES = {
    "Phione": (
        "breeding",
        "Breed Manaphy or Phione with Ditto at Solaceon Daycare",
        "Cruzar Manaphy ou Phione com Ditto no Daycare de Solaceon",
    ),
    "Heatran": (
        "special",
        "Stark Mountain Interior (Post-Game Legendary Quest, Lv. 85)",
        "Interior da Stark Mountain (Missão Lendária Pós-Jogo, Nv. 85)",
    ),
}

BABY_BREEDING_NOTES = {
    "Pichu": ("Breed Pikachu or Raichu", "Cruzar Pikachu ou Raichu no Daycare"),
    "Cleffa": ("Breed Clefairy or Clefable", "Cruzar Clefairy ou Clefable no Daycare"),
    "Igglybuff": ("Breed Jigglypuff or Wigglytuff", "Cruzar Jigglypuff ou Wigglytuff no Daycare"),
    "Togepi": ("Breed Togetic or Togekiss", "Cruzar Togetic ou Togekiss no Daycare"),
    "Tyrogue": ("Breed Hitmonlee, Hitmonchan, or Hitmontop", "Cruzar Hitmonlee, Hitmonchan ou Hitmontop"),
    "Smoochum": ("Breed Jynx", "Cruzar Jynx no Daycare"),
    "Elekid": ("Breed Electabuzz or Electivire", "Cruzar Electabuzz ou Electivire no Daycare"),
    "Magby": ("Breed Magmar or Magmortar", "Cruzar Magmar ou Magmortar no Daycare"),
    "Azurill": ("Breed Marill or Azumarill holding Sea Incense", "Cruzar Marill ou Azumarill segurando Sea Incense"),
    "Wynaut": ("Breed Wobbuffet holding Lax Incense", "Cruzar Wobbuffet segurando Lax Incense"),
    "Budew": ("Breed Roselia or Roserade holding Rose Incense", "Cruzar Roselia ou Roserade segurando Rose Incense"),
    "Chingling": ("Breed Chimecho holding Pure Incense", "Cruzar Chimecho segurando Pure Incense"),
    "Bonsly": ("Breed Sudowoodo holding Rock Incense", "Cruzar Sudowoodo segurando Rock Incense"),
    "Mime Jr.": ("Breed Mr. Mime holding Odd Incense", "Cruzar Mr. Mime segurando Odd Incense"),
    "Happiny": ("Breed Chansey or Blissey holding Luck Incense", "Cruzar Chansey ou Blissey segurando Luck Incense"),
    "Munchlax": ("Breed Snorlax holding Full Incense", "Cruzar Snorlax segurando Full Incense"),
    "Riolu": ("Breed Lucario", "Cruzar Lucario no Daycare"),
    "Mantyke": ("Breed Mantine holding Wave Incense", "Cruzar Mantine segurando Wave Incense"),
    "Tinkatink": ("Breed Tinkatuff or Tinkaton at Solaceon Daycare", "Cruzar Tinkatuff ou Tinkaton no Daycare de Solaceon"),
}


def load_gamedata_json(filename: str) -> dict:
    """Load a gamedata2.0 JSON file locally if available, otherwise fetch from GitHub."""
    local_path = os.path.join(GAMEDATA_DIR, filename)
    if os.path.exists(local_path):
        with open(local_path, "r", encoding="utf-8") as f:
            return json.load(f)

    url = f"{GITHUB_RAW_GAMEDATA}/{filename}"
    req = urllib.request.Request(url, headers={"User-Agent": "LumiTracker-PokedexBuilder/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def label_at(label_array: list, idx: int) -> str:
    if 0 <= idx < len(label_array):
        words = label_array[idx].get("wordDataArray") or []
        if words:
            return words[0].get("str", "") or ""
    return ""


def get_generation(monsno: int) -> str:
    if monsno <= 151:
        return "Gen 1"
    if monsno <= 251:
        return "Gen 2"
    if monsno <= 386:
        return "Gen 3"
    if monsno <= 493:
        return "Gen 4"
    return "Lumi Extras"


def get_sprite_urls(pokemon_name: str, monsno: int, sprite_form_idx: int, form_category: str) -> tuple[str, str]:
    """Return (primarySpriteUrl, fallbackSpriteUrl) with full coverage for Lumi & Gen 8/9 forms."""
    lumi_webp = f"{TEAM_LUMI_SPRITE_BASE}/pm{monsno:04d}_{sprite_form_idx:02d}_00_00_L.webp"

    if form_category == "special":
        # Clone, Stitched, Crystal, Spiky-eared, East Sea forms use TeamLumi's exact artwork first
        if pokemon_name == "Shellos East Sea":
            return ("https://play.pokemonshowdown.com/sprites/gen5/shellos-east.png", lumi_webp)
        if pokemon_name == "Gastrodon East Sea":
            return ("https://play.pokemonshowdown.com/sprites/gen5/gastrodon-east.png", lumi_webp)
        return (lumi_webp, f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{monsno}.png")

    slug = (
        pokemon_name.lower()
        .replace("alolan ", "")
        .replace("galarian ", "")
        .replace("hisuian ", "")
        .replace("♀", "-f")
        .replace("♂", "-m")
    )
    if pokemon_name in ("Nidoran-F", "Nidoran-M"):
        slug = pokemon_name.lower()
    else:
        slug = "".join(ch for ch in slug if ch.isalnum())

    if pokemon_name.startswith("Alolan "):
        slug += "-alola"
    elif pokemon_name.startswith("Galarian "):
        slug += "-galar"
    elif pokemon_name.startswith("Hisuian "):
        slug += "-hisui"

    # Gen 9 / Hisui mons missing in Showdown gen5 sprites use TeamLumi's sprite as fallback (or dexani/home)
    if monsno > 898:
        return (lumi_webp, f"https://play.pokemonshowdown.com/sprites/dex/{slug}.png")

    showdown_url = f"https://play.pokemonshowdown.com/sprites/gen5/{slug}.png"
    fallback_url = lumi_webp if form_category != "base" or monsno > 649 else (
        f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{monsno}.png"
    )
    return (showdown_url, fallback_url)


def format_evo_method(
    method_id: int,
    param: int,
    level: int,
    item_names: list,
    move_names: list,
    type_names: list,
    id_to_name: dict,
) -> tuple[str, str]:
    """Return (method_en, method_pt) for a TeamLumi EvolveTable tuple."""
    item = label_at(item_names, param) if param else ""
    move = label_at(move_names, param) if param else ""
    ptype = label_at(type_names, param) if param else ""
    mon = id_to_name.get(param, "")

    table = {
        1: ("Friendship", "Amizade"),
        2: ("Friendship (Day)", "Amizade (Dia)"),
        3: ("Friendship (Night)", "Amizade (Noite)"),
        4: (f"Level {level}", f"Nível {level}"),
        5: ("Trade", "Troca"),
        6: (f"Trade holding {item}", f"Troca segurando {item}"),
        7: ("Karrablast/Shelmet Trade", "Troca Karrablast/Shelmet"),
        8: (f"Use {item}", f"Usar {item}"),
        9: (f"Level {level} (Atk > Def)", f"Nível {level} (Atk > Def)"),
        10: (f"Level {level} (Atk = Def)", f"Nível {level} (Atk = Def)"),
        11: (f"Level {level} (Def > Atk)", f"Nível {level} (Def > Atk)"),
        12: (f"Level {level}", f"Nível {level}"),
        13: (f"Level {level}", f"Nível {level}"),
        14: (f"Level {level} (Empty Slot + Poké Ball)", f"Nível {level} (Espaço na Party + Poké Ball)"),
        15: (f"Evolve Nincada at Level {level}", f"Evoluir Nincada no Nível {level}"),
        16: ("High Beauty", "Beleza Alta (Beauty)"),
        17: (f"Use {item} (Male)", f"Usar {item} (Macho)"),
        18: (f"Use {item} (Female)", f"Usar {item} (Fêmea)"),
        19: (f"Level up holding {item} (Day)", f"Subir nível segurando {item} (Dia)"),
        20: (f"Level up holding {item} (Night)", f"Subir nível segurando {item} (Noite)"),
        21: (f"Level up knowing {move}", f"Subir nível sabendo {move}"),
        22: (f"Level up with {mon} in party", f"Subir nível com {mon} na party"),
        23: (f"Level {level} (Male)", f"Nível {level} (Macho)"),
        24: (f"Level {level} (Female)", f"Nível {level} (Fêmea)"),
        25: ("Level up in Magnetic Field", "Subir nível em Campo Magnético"),
        26: ("Level up near Moss Rock", "Subir nível perto da Moss Rock"),
        27: ("Level up near Ice Rock", "Subir nível perto da Ice Rock"),
        28: (f"Level {level} (Upside-Down)", f"Nível {level} (Invertido)"),
        29: (f"Friendship + {ptype}-type Move", f"Amizade + Golpe tipo {ptype}"),
        30: (f"Level {level} (Dark-type in party)", f"Nível {level} (Tipo Dark na party)"),
        31: (f"Level {level} (in Rain)", f"Nível {level} (na Chuva)"),
        32: (f"Level {level} (Day)", f"Nível {level} (Dia)"),
        33: (f"Level {level} (Night)", f"Nível {level} (Noite)"),
        34: (f"Level {level} (Female)", f"Nível {level} (Fêmea)"),
        39: ("Level up at Mt. Coronet Summit", "Subir nível no topo do Mt. Coronet"),
        40: (f"Level {level} (19:00–19:59)", f"Nível {level} (19:00–19:59)"),
        41: (f"Level {level} (Regional)", f"Nível {level} (Regional)"),
        42: (f"Use {item}", f"Usar {item}"),
        43: (f"{param or level or 3} Critical Hits in one battle", f"{param or level or 3} Críticos na mesma batalha"),
        44: (f"Take {param or level or 49}+ recoil/damage", f"Receber {param or level or 49}+ de dano"),
        46: (f"Level {level} (Amped Nature)", f"Nível {level} (Nature Amped)"),
        47: (f"Level {level} (Low-Key Nature)", f"Nível {level} (Nature Low-Key)"),
        48: (f"Level up holding {item}", f"Subir nível segurando {item}"),
        49: (f"Level up with {mon} in party", f"Subir nível com {mon} na party"),
        50: (f"Level {level}", f"Nível {level}"),
        51: (f"Level {level}", f"Nível {level}"),
        52: (f"Walk {param or level} steps as follower", f"Caminhar {param or level} passos seguindo"),
        53: (f"Have {item} in Bag", f"Ter {item} na Bolsa"),
        55: (f"Knows {move}", f"Sabendo {move}"),
        56: (f"Knows {move}", f"Sabendo {move}"),
    }
    return table.get(method_id, (f"Level {level}" if level else "Special Evolution", f"Nível {level}" if level else "Evolução Especial"))


def build_pokedex(output_path: str = OUTPUT_POKEDEX_JSON, encounters_path: str = ENCOUNTERS_JSON) -> list:
    personal_list = load_gamedata_json("PersonalTable.json")["Personal"]
    evolve_list = load_gamedata_json("EvolveTable.json")["Evolve"]
    mons_names = load_gamedata_json("english_ss_monsname.json")["labelDataArray"]
    form_names = load_gamedata_json("english_ss_zkn_form.json")["labelDataArray"]
    type_names = load_gamedata_json("english_ss_typename.json")["labelDataArray"]
    item_names = load_gamedata_json("english_ss_itemname.json")["labelDataArray"]
    move_names = load_gamedata_json("english_ss_wazaname.json")["labelDataArray"]

    # Load encounters to cross-link catchable status & route counts
    encounters = []
    if os.path.exists(encounters_path):
        with open(encounters_path, "r", encoding="utf-8") as f:
            encounters = json.load(f)

    enc_routes_by_mon: dict[str, list[str]] = {}
    enc_methods_by_mon: dict[str, list[str]] = {}
    for e in encounters:
        mon = e.get("pokemon")
        loc = e.get("location")
        method = e.get("method")
        if not mon:
            continue
        if loc:
            enc_routes_by_mon.setdefault(mon, [])
            if loc not in enc_routes_by_mon[mon]:
                enc_routes_by_mon[mon].append(loc)
        if method:
            enc_methods_by_mon.setdefault(mon, [])
            if method not in enc_methods_by_mon[mon]:
                enc_methods_by_mon[mon].append(method)

    # Build FORM_MAP: monsno -> [personalId or -1, ...]
    form_map: dict[int, list[int]] = {}
    personal_by_id: dict[int, dict] = {}
    for p in personal_list:
        pid = p["id"]
        monsno = p["monsno"]
        personal_by_id[pid] = p
        form_map.setdefault(monsno, []).append(pid if p.get("valid_flag") == 1 else -1)

    def resolve_target_personal_id(monsno: int, formno: int) -> int | None:
        forms = form_map.get(monsno, [])
        if 0 <= formno < len(forms) and forms[formno] != -1:
            return forms[formno]
        return None

    # Select included Pokédex entries:
    # 1. All 513 valid base species (pid == monsno)
    # 2. All Regional forms (Alolan / Galarian / Hisuian)
    # 3. Included Special Lumi forms + East Sea forms
    selected_entries: dict[int, dict] = {}
    for p in personal_list:
        if p.get("valid_flag") != 1 or p.get("monsno", 0) <= 0:
            continue
        pid = p["id"]
        monsno = p["monsno"]
        base_str = label_at(mons_names, monsno)
        alt_str = label_at(form_names, pid)

        form_category = None
        display_name = None

        if pid == monsno:
            form_category = "base"
            display_name = CANONICAL_NAME_OVERRIDES.get(pid, base_str)
        elif pid in INCLUDED_SPECIAL_PERSONAL_IDS:
            display_name, form_category = INCLUDED_SPECIAL_PERSONAL_IDS[pid]
        elif alt_str.startswith("Alolan "):
            form_category = "alolan"
            display_name = CANONICAL_NAME_OVERRIDES.get(pid, alt_str)
        elif alt_str.startswith("Galarian "):
            form_category = "galarian"
            display_name = CANONICAL_NAME_OVERRIDES.get(pid, alt_str)
        elif alt_str.startswith("Hisuian "):
            form_category = "hisuian"
            display_name = CANONICAL_NAME_OVERRIDES.get(pid, alt_str)

        if not display_name or not form_category:
            continue

        raw_form_idx = form_map[monsno].index(pid)
        sprite_form_idx = raw_form_idx
        if monsno == 25 and raw_form_idx in LUMI_TO_RELUMI_PIKACHU_FORMS:
            sprite_form_idx = LUMI_TO_RELUMI_PIKACHU_FORMS[raw_form_idx]

        t1 = label_at(type_names, p["type1"])
        t2 = label_at(type_names, p["type2"])
        types = [t1] if p["type1"] == p["type2"] or not t2 else [t1, t2]

        primary_sprite, fallback_sprite = get_sprite_urls(
            display_name, monsno, sprite_form_idx, form_category
        )

        selected_entries[pid] = {
            "personalId": pid,
            "dexId": monsno,
            "formIndex": sprite_form_idx,
            "pokemon": display_name,
            "types": types,
            "generation": get_generation(monsno),
            "formCategory": form_category,
            "spriteUrl": primary_sprite,
            "fallbackSpriteUrl": fallback_sprite,
        }

    id_to_name = {pid: info["pokemon"] for pid, info in selected_entries.items()}
    # Also fill base names for any lookup in move/party evo params
    for m_idx in range(1, len(mons_names)):
        if m_idx not in id_to_name:
            b = label_at(mons_names, m_idx)
            if b:
                id_to_name[m_idx] = b

    # Decode EvolveTable edges among selected_entries
    edges_out: dict[int, dict[int, list[tuple[str, str]]]] = {}
    edges_in: dict[int, list[tuple[int, str, str]]] = {}

    evolve_by_id = {e["id"]: e.get("ar", []) for e in evolve_list}
    for src_pid in selected_entries:
        ar = evolve_by_id.get(src_pid, [])
        for j in range(0, len(ar), 5):
            if j + 4 >= len(ar):
                break
            method_id, param, target_monsno, target_formno, level = ar[j : j + 5]
            if method_id <= 0 or target_monsno <= 0:
                continue
            target_pid = resolve_target_personal_id(target_monsno, target_formno)
            if target_pid is None or target_pid not in selected_entries:
                continue
            m_en, m_pt = format_evo_method(
                method_id, param, level, item_names, move_names, type_names, id_to_name
            )
            pair_list = edges_out.setdefault(src_pid, {}).setdefault(target_pid, [])
            if (m_en, m_pt) not in pair_list:
                pair_list.append((m_en, m_pt))

    # Nincada (290) -> Shedinja (292) is handled as an engine side-effect of method 14
    if 290 in selected_entries and 292 in selected_entries:
        edges_out.setdefault(290, {})[292] = [
            (
                "Level 20 (Empty Party Slot + Poké Ball in Bag)",
                "Nível 20 (Espaço na Party + Poké Ball na Bolsa)",
            )
        ]

    for src_pid, targets_dict in edges_out.items():
        for dst_pid, methods_list in targets_dict.items():
            combined_en = " / ".join(m[0] for m in methods_list)
            combined_pt = " / ".join(m[1] for m in methods_list)
            edges_in.setdefault(dst_pid, []).append((src_pid, combined_en, combined_pt))

    # Build recursive evolution tree helper (cycle-safe)
    def find_roots(pid: int) -> list[int]:
        visited = set()
        roots = []

        def dfs_up(cur: int):
            if cur in visited:
                return
            visited.add(cur)
            parents = edges_in.get(cur, [])
            if not parents:
                if cur not in roots:
                    roots.append(cur)
                return
            for parent_pid, _, _ in parents:
                dfs_up(parent_pid)

        dfs_up(pid)
        return roots or [pid]

    def build_tree_node(
        pid: int, method_en: str = "", method_pt: str = "", path_seen: frozenset = frozenset()
    ) -> dict:
        entry = selected_entries[pid]
        children = []
        if pid not in path_seen:
            next_seen = path_seen | {pid}
            for dst_pid, methods_list in edges_out.get(pid, {}).items():
                c_en = " / ".join(m[0] for m in methods_list)
                c_pt = " / ".join(m[1] for m in methods_list)
                children.append(build_tree_node(dst_pid, c_en, c_pt, next_seen))
        return {
            "pokemon": entry["pokemon"],
            "dexId": entry["dexId"],
            "spriteUrl": entry["spriteUrl"],
            "fallbackSpriteUrl": entry["fallbackSpriteUrl"],
            "method_en": method_en,
            "method_pt": method_pt,
            "evolvesInto": children,
        }

    form_sort_rank = {
        "base": 0,
        "alolan": 1,
        "galarian": 2,
        "hisuian": 3,
        "special": 4,
    }

    pokedex_records = []
    for pid, entry in sorted(
        selected_entries.items(),
        key=lambda kv: (kv[1]["dexId"], form_sort_rank.get(kv[1]["formCategory"], 9), kv[0]),
    ):
        mon_name = entry["pokemon"]
        routes = enc_routes_by_mon.get(mon_name, [])
        methods = enc_methods_by_mon.get(mon_name, [])
        is_catchable = len(routes) > 0

        parents = edges_in.get(pid, [])
        evolves_from = None
        if parents:
            # Prefer matching formCategory parent if multiple exist
            preferred_parent = parents[0]
            for cand in parents:
                if selected_entries[cand[0]]["formCategory"] == entry["formCategory"]:
                    preferred_parent = cand
                    break
            p_pid, m_en, m_pt = preferred_parent
            evolves_from = {
                "pokemon": selected_entries[p_pid]["pokemon"],
                "dexId": selected_entries[p_pid]["dexId"],
                "method_en": m_en,
                "method_pt": m_pt,
            }

        evolves_into = []
        for dst_pid, methods_list in edges_out.get(pid, {}).items():
            evolves_into.append(
                {
                    "pokemon": selected_entries[dst_pid]["pokemon"],
                    "dexId": selected_entries[dst_pid]["dexId"],
                    "method_en": " / ".join(m[0] for m in methods_list),
                    "method_pt": " / ".join(m[1] for m in methods_list),
                }
            )

        roots = find_roots(pid)
        evo_trees = [build_tree_node(r) for r in roots]

        special_note_en = ""
        special_note_pt = ""
        if mon_name in SPECIAL_OBTAIN_NOTES:
            obtain_cat, special_note_en, special_note_pt = SPECIAL_OBTAIN_NOTES[mon_name]
        elif is_catchable:
            obtain_cat = "wild"
        elif evolves_from:
            obtain_cat = "evolution"
        elif mon_name in BABY_BREEDING_NOTES:
            obtain_cat = "breeding"
            special_note_en, special_note_pt = BABY_BREEDING_NOTES[mon_name]
        else:
            obtain_cat = "special"

        record = {
            **entry,
            "isCatchable": is_catchable,
            "routeCount": len(routes),
            "routes": routes,
            "encounterMethods": methods,
            "obtainCategory": obtain_cat,
            "evolvesFrom": evolves_from,
            "evolvesInto": evolves_into,
            "evolutionChain": evo_trees,
        }
        if special_note_en:
            record["specialNote_en"] = special_note_en
            record["specialNote_pt"] = special_note_pt

        pokedex_records.append(record)

    # Verify 100% coverage of luminescent_encounters.json species
    pokedex_names = {r["pokemon"] for r in pokedex_records}
    missing_from_encounters = set(enc_routes_by_mon.keys()) - pokedex_names
    if missing_from_encounters:
        raise RuntimeError(
            f"Pokédex is missing {len(missing_from_encounters)} encounter names: {sorted(missing_from_encounters)}"
        )

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(pokedex_records, f, indent=2, ensure_ascii=False)

    return pokedex_records


def main():
    print("Generating luminescent_pokedex.json...")
    records = build_pokedex()
    wild_cnt = sum(1 for r in records if r["isCatchable"])
    evo_cnt = sum(1 for r in records if not r["isCatchable"] and r["obtainCategory"] == "evolution")
    other_cnt = sum(1 for r in records if not r["isCatchable"] and r["obtainCategory"] != "evolution")
    forms_cnt = sum(1 for r in records if r["formCategory"] != "base")
    print(
        f"[OK] Exported {len(records)} Pokédex entries to {OUTPUT_POKEDEX_JSON} "
        f"(Base: {len(records) - forms_cnt}, Regional/Special Forms: {forms_cnt} | "
        f"Catchable: {wild_cnt}, Evolution-only: {evo_cnt}, Breeding/Other: {other_cnt})"
    )


if __name__ == "__main__":
    main()
