# Lumi Tracker - An Pokémon Encounter Organizer

Encounter progress tracker for **Pokémon Luminescent Platinum**. Browse Pokémon by route/location (in campaign progression order), encounter method, and time of day, while keeping track of which mons you have already caught.

## Features

- **Dual Mode via Sidemenu (`Encontros / Rotas` & `Pokédex Completa`)**:
  - **Encounters / Routes**: Progression-ordered route guide (`ordered_locations.json` + `luminescent_encounters.json`) with catch-origin tracking (`Caught here` vs `In Dex ([Route])` + one-click transfer).
  - **Complete Pokédex**: Tracks all **559** obtainable Luminescent Platinum entries (513 base species + Regional forms + Lumi Special forms), including evolution-only and breeding-only Pokémon, interactive evolution chains, and an origin editor modal.
- **"Available Now" Mode**: Automatically filters encounters based on the current system time (Morning, Day, or Night) and the selected route, while hiding already-caught Pokémon.
- **Persistent Progress**: Saves caught Pokémon, capture origins, and filter preferences in `localStorage` and `%APPDATA%\LumiTracker\state.json`, with **JSON Backup / Import** support.
- **Bilingual Support (EN / PT)**: Defaults to English with a compact `EN | PT` header toggle in the UI and unified language persistence (`%APPDATA%\LumiTracker\lang.txt` + `localStorage`). All CLI scripts and `.bat` launchers also support `--lang en|pt`.
- **Desktop or Browser Mode**: Runs in a native desktop window via `pywebview` (`app.py`) or through a local fallback HTTP server (`server.py`).

## Prerequisites

- **Python 3.10+**
- **Microsoft Edge WebView2** (included by default on Windows 10/11, required by `pywebview` in desktop mode).
- **Internet Connection**: The UI in `index.html` loads Tailwind CSS via CDN (`cdn.tailwindcss.com`) and sprites from Pokémon Showdown / PokéAPI.

## Getting Started

### 1. Install Dependencies

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the App

* **Desktop App (Recommended):**
  ```bash
  python app.py
  ```
  Or double-click `launch_app.bat` (which detects `.venv` / `venv`, installs `pywebview` if missing, and falls back to `server.py` if desktop mode fails).

* **Local Web Server (Default Browser):**
  ```bash
  python server.py
  ```
  Or run `start_server.bat`.

* **Language Override via CLI:**
  Pass `--lang pt` or `--lang en` (or `-l pt` / `-l en`) to `app.py`, `server.py`, `build_exe.py`, `parse_encounters.py`, or any `.bat` launcher to switch and persist the active language.

## Building the Windows Executable (`.exe`)

To build a standalone single-file executable (`dist/LumiTracker.exe`) on Windows:

```bash
pip install -r requirements-dev.txt
python build_exe.py
```

Or run `build_exe.bat`.

> Official builds will be available soon under the **Releases** tab!!

## Updating the Encounter Database

`luminescent_encounters.json` and `ordered_locations.json` are already included and ready to use. If you want to re-extract the data from the official [TeamLumi/luminescent-team](https://github.com/TeamLumi/luminescent-team) repository:

1. Clone the upstream repository into the `lumi-repo` folder:
   ```bash
   git clone https://github.com/TeamLumi/luminescent-team lumi-repo
   ```
2. Run the parser script:
   ```bash
   python parse_encounters.py
   ```

## Project Structure

- `app.py`: Native desktop launcher powered by `pywebview`.
- `server.py`: Local fallback HTTP server (`localhost:8000+`).
- `i18n_cli.py`: Shared CLI language resolution, persistence, and translations (`en`/`pt`).
- `conditions_i18n.py`: Bilingual condition translations for encounter notes.
- `index.html`: Web interface (Encounters & Complete Pokédex views, Sidemenu, and Detail Modal).
- `luminescent_encounters.json`: Normalized wild/static/gift/trade encounter database.
- `luminescent_pokedex.json`: Complete Pokédex database (all obtainable species, forms, types, and bilingual evolution chains).
- `ordered_locations.json`: Campaign-ordered list of locations.
- `generate_pokedex.py`: Script to build `luminescent_pokedex.json` from TeamLumi gamedata.
- `parse_encounters.py`: Script to extract and normalize encounter data from `lumi-repo/` (and regenerate the Pokédex).
- `build_exe.py`: PyInstaller bundler for Windows.
- `launch_app.bat`, `start_server.bat`, `build_exe.bat`: Windows convenience launchers.

## Credits

- Encounter and location data based on [Luminescent Platinum (TeamLumi/luminescent-team)](https://github.com/TeamLumi/luminescent-team).
- Sprites loaded from [Pokémon Showdown](https://play.pokemonshowdown.com/sprites/) and [PokéAPI](https://github.com/PokeAPI/sprites).
