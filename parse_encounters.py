#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
parse_encounters.py
Script de extração, normalização e exportação da base de dados de encontros
do projeto Luminescent Platinum (https://github.com/TeamLumi/luminescent-team).

Exporta para:
- luminescent_encounters.json
- luminescent_encounters.csv
"""

import os
import re
import csv
import sys
import json
from collections import Counter

# Assegura stdout em utf-8 no console Windows
sys.stdout.reconfigure(encoding='utf-8')

# Caminhos base dos dados
GAMEDATA_DIR = os.path.join("lumi-repo", "__gamedata", "gamedata2.0")
DOCS_SPECIAL_DIR = os.path.join("lumi-repo", "docs", "special-events")
MONS_NAME_FILE = os.path.join(GAMEDATA_DIR, "english_ss_monsname.json")
POKEMON_LOC_TXT = os.path.join(GAMEDATA_DIR, "pokemon_locations.txt")
STATIC_LOC_JSON = os.path.join(GAMEDATA_DIR, "static_pokemon_locations.json")
ENCOUNTER_LOC_JSON = os.path.join(GAMEDATA_DIR, "encounter_locations.json")

OUTPUT_JSON = "luminescent_encounters.json"
OUTPUT_CSV = "luminescent_encounters.csv"


def load_dex_id_mapper():
    """Carrega tabela de correspondência Nome do Pokémon -> National Dex ID."""
    base_map = {}
    if os.path.exists(MONS_NAME_FILE):
        with open(MONS_NAME_FILE, "r", encoding="utf-8") as f:
            mons_data = json.load(f)
        for item in mons_data.get("labelDataArray", []):
            idx = item.get("arrayIndex")
            name = item.get("wordDataArray", [{}])[0].get("str")
            if name and name not in base_map:
                base_map[name] = idx

    # Adições específicas da Pokédex expandida e formas regionais/clones
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

        # Tratamento de prefixos de formas
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
    """Mapeia (routeName, pokemonName) -> (minLevel, maxLevel) a partir do RomFS."""
    ranges = {}
    if os.path.exists(ENCOUNTER_LOC_JSON):
        with open(ENCOUNTER_LOC_JSON, "r", encoding="utf-8") as f:
            el_data = json.load(f)
        for _, encs in el_data.items():
            for e in encs:
                route = e.get("routeName")
                mon = e.get("pokemonName")
                min_lvl = e.get("minLevel")
                max_lvl = e.get("maxLevel")
                if route and mon and min_lvl is not None and max_lvl is not None:
                    key = (route, mon)
                    if key not in ranges:
                        ranges[key] = (min_lvl, max_lvl)
                    else:
                        prev_min, prev_max = ranges[key]
                        ranges[key] = (min(prev_min, min_lvl), max(prev_max, max_lvl))
    return ranges


def parse_mdx_special_events():
    """Extrai instruções e condições dos arquivos MDX em docs/special-events/."""
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

            name_m = re.search(
                r"<h3[^>]*>.*?<span class=\"heading-text\">(?:&emsp;)?([^<]+)</span>",
                row,
                re.DOTALL,
            )
            if not name_m:
                name_m = re.search(
                    r"<h3[^>]*>\s*(?:&emsp;)?\s*([A-Za-z0-9\s\'\.\(\)-]+?)\s*</h3>",
                    row,
                    re.DOTALL,
                )

            id_m = re.search(r'<h3 id="([^"]+)"', row)

            lis = re.findall(r"<li>(.*?)</li>", row, re.DOTALL)
            clean_lis = [re.sub(r"<[^>]+>", "", li).strip() for li in lis]
            text = " ".join(clean_lis).replace("\n", " ")
            text = re.sub(r"\s+", " ", text).strip()

            if name_m:
                mon_name = name_m.group(1).strip()
                conditions[mon_name.lower()] = text
            if id_m:
                slug = id_m.group(1).lower()
                conditions[slug] = text

    return conditions


def main():
    if not os.path.exists(GAMEDATA_DIR):
        print(
            f"[ERRO] Diretório de dados não encontrado: '{GAMEDATA_DIR}'.\n"
            "Clone o repositório do Luminescent Platinum em './lumi-repo' "
            "(https://github.com/TeamLumi/luminescent-team) antes de executar este script."
        )
        sys.exit(1)

    print("Iniciando extração e normalização de encontros...")

    get_dex_id = load_dex_id_mapper()
    level_ranges = load_level_ranges()
    mdx_conditions = parse_mdx_special_events()

    records = []

    # 1. Processar encontros de rotas selvagens (pokemon_locations.txt)
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

                    # Determinar níveis (respeitando faixas se min != max)
                    key = (route_name, mon_name)
                    if key in level_ranges:
                        min_lvl, max_lvl = level_ranges[key]
                        levels_str = f"{min_lvl}-{max_lvl}" if min_lvl != max_lvl else str(min_lvl)
                    else:
                        levels_str = str(raw_level)

                    # Determinar method padronizado
                    conditions = "Nenhuma"
                    if raw_method in ("Grass", "Morning", "day", "night", "Daily Trophy Garden"):
                        method = "Walking"
                        if raw_method == "Daily Trophy Garden":
                            conditions = "Trophy Garden Diário"
                    elif raw_method == "Swarm":
                        method = "Walking"
                        conditions = "Enxame Diário (Swarm)"
                    elif raw_method == "Surfing":
                        method = "Surfing"
                        conditions = "Requer Surf (HM03)"
                    elif raw_method in ("Incense", "Surfing Incense"):
                        method = "Incense"
                        if raw_method == "Surfing Incense":
                            conditions = "Requer Incense Burner na água"
                        else:
                            conditions = "Requer Incense Burner"
                    elif raw_method in ("Old Rod", "Good Rod", "Super Rod", "Radar", "Honey Tree"):
                        method = raw_method
                        if raw_method == "Radar":
                            conditions = "Requer Poké Radar"
                        elif "Rod" in raw_method:
                            conditions = f"Requer {raw_method}"
                        elif raw_method == "Honey Tree":
                            conditions = "Árvore de Mel"
                    else:
                        method = raw_method

                    # Determinar time_of_day
                    if raw_method == "Morning":
                        time_of_day = ["Morning"]
                        if conditions == "Nenhuma":
                            conditions = "Disponível apenas pela manhã (04:00 - 09:59)"
                    elif raw_method == "day":
                        time_of_day = ["Day"]
                        if conditions == "Nenhuma":
                            conditions = "Disponível apenas durante o dia (10:00 - 19:59)"
                    elif raw_method == "night":
                        time_of_day = ["Night"]
                        if conditions == "Nenhuma":
                            conditions = "Disponível apenas à noite (20:00 - 03:59)"
                    else:
                        time_of_day = ["Morning", "Day", "Night"]

                    records.append({
                        "id": get_dex_id(mon_name),
                        "pokemon": mon_name,
                        "location": route_name,
                        "method": method,
                        "rate": raw_rate,
                        "levels": levels_str,
                        "time_of_day": time_of_day,
                        "version": "All",
                        "conditions": conditions,
                    })

    # 2. Processar eventos especiais (static_pokemon_locations.json + MDX)
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

                # Determinar método padronizado
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

                # Buscar condições ricas nos arquivos MDX via link ou nome
                condition_text = None
                if link and "#" in link:
                    anchor = link.split("#")[-1].lower()
                    condition_text = mdx_conditions.get(anchor)

                if not condition_text:
                    condition_text = mdx_conditions.get(mon_name.lower())

                if not condition_text:
                    if enc_type == "Starter":
                        condition_text = "Escolha de Pokémon inicial"
                    elif enc_type == "Legendaries":
                        condition_text = "Encontro com Pokémon Lendário"
                    elif enc_type == "Trade":
                        condition_text = "Troca in-game com NPC"
                    elif enc_type == "Gifts":
                        condition_text = "Presente de NPC / Ovo recebido"
                    elif enc_type == "Static":
                        condition_text = "Encontro fixo no mapa / Interação única"
                    else:
                        condition_text = "Nenhuma"

                records.append({
                    "id": get_dex_id(mon_name),
                    "pokemon": mon_name,
                    "location": route_name,
                    "method": method,
                    "rate": rate_str,
                    "levels": levels_str,
                    "time_of_day": ["Morning", "Day", "Night"],
                    "version": "All",
                    "conditions": condition_text,
                })

    if not records:
        print("[ERRO] Nenhum registro extraído. Abortando para não sobrescrever os arquivos de saída.")
        sys.exit(1)

    # Exportar JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    # Exportar CSV
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
    ]
    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in records:
            # Serializa time_of_day como string JSON no CSV
            row = dict(r)
            row["time_of_day"] = json.dumps(r["time_of_day"], ensure_ascii=False)
            writer.writerow(row)

    # Estatísticas e Relatórios
    total_records = len(records)
    tod_counter = Counter()
    null_report = []

    for idx, r in enumerate(records):
        tod = tuple(r["time_of_day"])
        if tod == ("Morning",):
            tod_counter["Exclusivo Manhã"] += 1
        elif tod == ("Day",):
            tod_counter["Exclusivo Dia"] += 1
        elif tod == ("Night",):
            tod_counter["Exclusivo Noite"] += 1
        elif len(tod) == 3:
            tod_counter["Qualquer Horário (Manhã, Dia, Noite)"] += 1
        else:
            tod_counter[f"Outro período ({tod})"] += 1

        # Verificação de campos nulos ou sem horário
        null_fields = [k for k, v in r.items() if v is None or v == ""]
        if not r.get("time_of_day"):
            null_fields.append("time_of_day")

        if null_fields:
            null_report.append((idx, r.get("pokemon"), r.get("location"), null_fields))

    print("\n" + "=" * 60)
    print("RELATÓRIO DE EXTRAÇÃO E EXPORTAÇÃO")
    print("=" * 60)
    print(f"Total de registros exportados: {total_records}")
    print(f"Arquivos salvos:")
    print(f"  - JSON: {OUTPUT_JSON}")
    print(f"  - CSV:  {OUTPUT_CSV}")

    print("\n--- Contagem de Encontros por Período ---")
    for period, count in tod_counter.items():
        pct = (count / total_records) * 100
        print(f"  {period:<40}: {count:>5} ({pct:>5.1f}%)")

    print("\n--- Métodos de Encontro Padronizados ---")
    method_counter = Counter(r["method"] for r in records)
    for m, cnt in method_counter.most_common():
        print(f"  {m:<20}: {cnt:>5}")

    print("\n--- Relatório de Validação e Integridade ---")
    if not null_report:
        print("  [OK] Nenhuma entrada sem horário encontrada.")
        print("  [OK] Todos os registros possuem campos válidos (sem valores nulos).")
    else:
        print(f"  [ALERTA] Encontrados {len(null_report)} registros com campos ausentes:")
        for entry in null_report[:10]:
            print(f"    - Registro {entry[0]}: Pokémon={entry[1]}, Local={entry[2]}, Campos Ausentes={entry[3]}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
