# Luminescent Platinum - Playthrough & Encounter Tracker

Encounter and playthrough progress tracker for **Pokémon Luminescent Platinum**. Browse Pokémon by route/location (in campaign progression order), encounter method, and time of day, while keeping track of which species you have already caught.

## Features

- **Progression-Ordered Route Filter**: Routes ordered in `ordered_locations.json` combined with the `luminescent_encounters.json` database.
- **"Available Now" Mode**: Automatically filters encounters based on the current system time (Morning, Day, or Night) and the selected route, while hiding already-caught Pokémon.
- **Persistent Progress**: Saves caught Pokémon and filter preferences in `localStorage` (stored in `%APPDATA%\LumiTracker` in desktop mode), with **JSON Backup / Import** support.
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
  Or double-click `iniciar_app.bat` (which detects `.venv` / `venv`, installs `pywebview` if missing, and falls back to `server.py` if desktop mode fails).

* **Local Web Server (Default Browser):**
  ```bash
  python server.py
  ```
  Or run `iniciar_servidor.bat`.

## Building the Windows Executable (`.exe`)

To build a standalone single-file executable (`dist/LuminescentTracker.exe`) on Windows:

```bash
pip install -r requirements-dev.txt
python build_exe.py
```

Or run `compilar_exe.bat`.

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
- `index.html`: Web interface and tracker logic.
- `luminescent_encounters.json`: Normalized encounter database.
- `ordered_locations.json`: Campaign-ordered list of locations.
- `parse_encounters.py`: Script to extract and normalize data from `lumi-repo/`.
- `build_exe.py`: PyInstaller bundler for Windows.
- `iniciar_app.bat`, `iniciar_servidor.bat`, `compilar_exe.bat`: Windows convenience launchers.

## Credits

- Encounter and location data based on [Luminescent Platinum (TeamLumi/luminescent-team)](https://github.com/TeamLumi/luminescent-team).
- Sprites loaded from [Pokémon Showdown](https://play.pokemonshowdown.com/sprites/) and [PokéAPI](https://github.com/PokeAPI/sprites).
