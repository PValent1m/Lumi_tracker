#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
i18n_cli.py
Shared internationalization and language persistence helpers for Lumi Tracker
CLI scripts, desktop launcher, and local server.
"""

import json
import os
import sys

DEFAULT_LANG = "en"
SUPPORTED_LANGS = ("en", "pt")
STORAGE_DIR_NAME = "LumiTracker"
LANG_FILE_NAME = "lang.txt"
STATE_FILE_NAME = "state.json"


def get_storage_dir() -> str:
    """Return the persistent LumiTracker storage directory and ensure it exists."""
    app_data_dir = os.environ.get("APPDATA", os.path.expanduser("~"))
    storage_path = os.path.join(app_data_dir, STORAGE_DIR_NAME)
    os.makedirs(storage_path, exist_ok=True)
    return storage_path


def get_lang_file_path() -> str:
    """Return the path to the persisted language file."""
    return os.path.join(get_storage_dir(), LANG_FILE_NAME)


def normalize_lang(val: str | None) -> str | None:
    """Normalize a language identifier to 'en' or 'pt', or None if unrecognized."""
    if not val or not isinstance(val, str):
        return None
    cleaned = val.strip().lower().replace("_", "-")
    if cleaned in ("en", "en-us", "en-gb", "english", "inglês", "ingles"):
        return "en"
    if cleaned in ("pt", "pt-br", "pt-pt", "portuguese", "português", "portugues"):
        return "pt"
    return None


def load_saved_lang() -> str:
    """Load the persisted language from lang.txt, defaulting to 'en'."""
    lang_path = get_lang_file_path()
    try:
        if os.path.exists(lang_path):
            with open(lang_path, "r", encoding="utf-8") as f:
                parsed = normalize_lang(f.read())
                if parsed:
                    return parsed
    except OSError:
        pass
    return DEFAULT_LANG


def save_lang(lang: str | None) -> str:
    """Normalize and persist the active language to lang.txt."""
    normalized = normalize_lang(lang) or DEFAULT_LANG
    lang_path = get_lang_file_path()
    try:
        with open(lang_path, "w", encoding="utf-8") as f:
            f.write(normalized)
    except OSError:
        pass
    return normalized


def get_state_file_path() -> str:
    """Return the path to the persisted tracker state file."""
    return os.path.join(get_storage_dir(), STATE_FILE_NAME)


def load_saved_state() -> dict:
    """Load persisted caught species and filter preferences from state.json."""
    state_path = get_state_file_path()
    if not os.path.exists(state_path):
        return {"exists": False, "caught": [], "prefs": {}}
    try:
        with open(state_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return {"exists": False, "caught": [], "prefs": {}}
        caught = [str(item) for item in data.get("caught", []) if isinstance(item, str)] if isinstance(data.get("caught"), list) else []
        prefs = data.get("prefs") if isinstance(data.get("prefs"), dict) else {}
        return {"exists": True, "caught": caught, "prefs": prefs}
    except (OSError, ValueError):
        return {"exists": False, "caught": [], "prefs": {}}


def save_state(partial_state: dict | None) -> dict:
    """Merge and persist caught species and/or filter preferences to state.json."""
    current = load_saved_state()
    caught = list(current["caught"])
    prefs = dict(current["prefs"])

    if isinstance(partial_state, dict):
        if isinstance(partial_state.get("caught"), list):
            caught = [str(item) for item in partial_state["caught"] if isinstance(item, str)]
        if isinstance(partial_state.get("prefs"), dict):
            prefs = dict(partial_state["prefs"])

    payload = {"caught": caught, "prefs": prefs}
    state_path = get_state_file_path()
    try:
        with open(state_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
    except OSError:
        pass
    return {"exists": True, **payload}


def resolve_cli_lang(argv: list[str] | None = None) -> str:
    """
    Resolve the active language from CLI arguments (--lang / -l), LUMI_LANG env var,
    or persisted storage. When --lang / -l is explicitly supplied, persist it.
    """
    args = sys.argv[1:] if argv is None else argv
    explicit_lang = None

    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ("--lang", "-l") and i + 1 < len(args):
            explicit_lang = normalize_lang(args[i + 1])
            i += 2
            continue
        if arg.startswith("--lang="):
            explicit_lang = normalize_lang(arg.split("=", 1)[1])
        elif arg.startswith("-l="):
            explicit_lang = normalize_lang(arg.split("=", 1)[1])
        i += 1

    if explicit_lang:
        return save_lang(explicit_lang)

    env_lang = normalize_lang(os.environ.get("LUMI_LANG"))
    if env_lang:
        return env_lang

    return load_saved_lang()


CLI_MESSAGES = {
    "en": {
        # server.py
        "server_banner_title": "{app_name} - LOCAL FALLBACK SERVER",
        "server_root_dir": "  Root directory : {base_dir}",
        "server_local_url": "  Local address  : {url}",
        "server_active_lang": "  Active language: {lang_code}",
        "server_ctrl_c": "  Press Ctrl+C to stop the server at any time.",
        "server_open_browser": "Opening default browser at: {url}",
        "server_start_error": "Error starting server on port {port}: {error}",
        "server_shutting_down": "\nShutting down local server...",
        "server_stopped": "Server stopped successfully.",
        "server_lang_changed": "[INFO] Language changed via UI to: {lang_code}",
        # build_exe.py
        "build_pyinstaller_ok": "[OK] PyInstaller detected: version {version}",
        "build_pyinstaller_missing": "[INFO] PyInstaller not found. Installing via pip...",
        "build_pyinstaller_install_err": "[ERROR] Failed to install PyInstaller.",
        "build_pyinstaller_installed": "[OK] PyInstaller installed successfully!",
        "build_banner_title": "  EXECUTABLE BUILD (.EXE) - {app_name}",
        "build_missing_file": "[ERROR] Required file not found: {file}",
        "build_running_cmd": "Running command:\n{cmd}\n",
        "build_success_title": "  [SUCCESS] EXECUTABLE BUILT SUCCESSFULLY!",
        "build_exe_location": "Executable location: {path}",
        "build_exe_hint": "You can move this .exe file to any folder or your Desktop!",
        "build_failed": "\n[ERROR] Build failed with exit code {code}.",
        # parse_encounters.py
        "parse_missing_dir": (
            "[ERROR] Data directory not found: '{dir}'.\n"
            "Clone the Luminescent Platinum repository into './lumi-repo' "
            "(https://github.com/TeamLumi/luminescent-team) before running this script."
        ),
        "parse_starting": "Starting encounter extraction and normalization...",
        "parse_no_records": "[ERROR] No records extracted. Aborting to avoid overwriting output files.",
        "parse_report_title": "EXTRACTION AND EXPORT REPORT",
        "parse_total_exported": "Total exported records: {total}",
        "parse_files_saved": "Saved files:",
        "parse_tod_section": "\n--- Encounters Count by Period ---",
        "parse_tod_morning": "Morning Only",
        "parse_tod_day": "Day Only",
        "parse_tod_night": "Night Only",
        "parse_tod_any": "Any Time (Morning, Day, Night)",
        "parse_tod_other": "Other period ({tod})",
        "parse_methods_section": "\n--- Standardized Encounter Methods ---",
        "parse_validation_section": "\n--- Validation and Integrity Report ---",
        "parse_validation_ok_time": "  [OK] No entries without time_of_day found.",
        "parse_validation_ok_nulls": "  [OK] All records have valid fields (no null values).",
        "parse_validation_warn": "  [WARN] Found {count} records with missing fields:",
        "parse_validation_entry": "    - Record {idx}: Pokémon={pokemon}, Location={location}, Missing Fields={fields}",
        # app.py
        "app_starting": "[INFO] Starting {app_name} Desktop ({lang_code})...",
    },
    "pt": {
        # server.py
        "server_banner_title": "{app_name} - SERVIDOR LOCAL DE CONTINGÊNCIA",
        "server_root_dir": "  Diretório raiz : {base_dir}",
        "server_local_url": "  Endereço local : {url}",
        "server_active_lang": "  Idioma ativo   : {lang_code}",
        "server_ctrl_c": "  Pressione Ctrl+C para encerrar o servidor a qualquer momento.",
        "server_open_browser": "Abrindo navegador padrão em: {url}",
        "server_start_error": "Erro ao iniciar servidor na porta {port}: {error}",
        "server_shutting_down": "\nEncerrando servidor local...",
        "server_stopped": "Servidor encerrado com sucesso.",
        "server_lang_changed": "[INFO] Idioma alterado pela interface para: {lang_code}",
        # build_exe.py
        "build_pyinstaller_ok": "[OK] PyInstaller detectado: versão {version}",
        "build_pyinstaller_missing": "[INFO] PyInstaller não encontrado. Instalando via pip...",
        "build_pyinstaller_install_err": "[ERRO] Falha ao instalar PyInstaller.",
        "build_pyinstaller_installed": "[OK] PyInstaller instalado com sucesso!",
        "build_banner_title": "  COMPILAÇÃO DE EXECUTÁVEL (.EXE) - {app_name}",
        "build_missing_file": "[ERRO] Arquivo obrigatório não encontrado: {file}",
        "build_running_cmd": "Executando comando:\n{cmd}\n",
        "build_success_title": "  [SUCESSO] EXECUTÁVEL GERADO COM ÊXITO!",
        "build_exe_location": "Local do executável: {path}",
        "build_exe_hint": "Você pode mover esse arquivo .exe para qualquer pasta ou Área de Trabalho!",
        "build_failed": "\n[ERRO] A compilação falhou com código {code}.",
        # parse_encounters.py
        "parse_missing_dir": (
            "[ERRO] Diretório de dados não encontrado: '{dir}'.\n"
            "Clone o repositório do Luminescent Platinum em './lumi-repo' "
            "(https://github.com/TeamLumi/luminescent-team) antes de executar este script."
        ),
        "parse_starting": "Iniciando extração e normalização de encontros...",
        "parse_no_records": "[ERRO] Nenhum registro extraído. Abortando para não sobrescrever os arquivos de saída.",
        "parse_report_title": "RELATÓRIO DE EXTRAÇÃO E EXPORTAÇÃO",
        "parse_total_exported": "Total de registros exportados: {total}",
        "parse_files_saved": "Arquivos salvos:",
        "parse_tod_section": "\n--- Contagem de Encontros por Período ---",
        "parse_tod_morning": "Exclusivo Manhã",
        "parse_tod_day": "Exclusivo Dia",
        "parse_tod_night": "Exclusivo Noite",
        "parse_tod_any": "Qualquer Horário (Manhã, Dia, Noite)",
        "parse_tod_other": "Outro período ({tod})",
        "parse_methods_section": "\n--- Métodos de Encontro Padronizados ---",
        "parse_validation_section": "\n--- Relatório de Validação e Integridade ---",
        "parse_validation_ok_time": "  [OK] Nenhuma entrada sem horário encontrada.",
        "parse_validation_ok_nulls": "  [OK] Todos os registros possuem campos válidos (sem valores nulos).",
        "parse_validation_warn": "  [ALERTA] Encontrados {count} registros com campos ausentes:",
        "parse_validation_entry": "    - Registro {idx}: Pokémon={pokemon}, Local={location}, Campos Ausentes={fields}",
        # app.py
        "app_starting": "[INFO] Iniciando {app_name} Desktop ({lang_code})...",
    },
}


def t(key: str, lang: str = DEFAULT_LANG, **kwargs) -> str:
    """Return a formatted localized CLI string for the given key and language."""
    normalized = normalize_lang(lang) or DEFAULT_LANG
    table = CLI_MESSAGES.get(normalized, CLI_MESSAGES[DEFAULT_LANG])
    template = table.get(key) or CLI_MESSAGES[DEFAULT_LANG].get(key, key)
    return template.format(**kwargs) if kwargs else template
