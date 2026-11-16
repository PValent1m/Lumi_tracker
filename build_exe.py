#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_exe.py
Script to package Lumi Tracker into a standalone single-file Windows
executable (.exe) using PyInstaller.
"""

import os
import sys
import subprocess

from i18n_cli import resolve_cli_lang, t

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

APP_NAME = "Lumi Tracker"
EXE_NAME = "LumiTracker"
REQUIRED_DATA_FILES = (
    "index.html",
    "luminescent_encounters.json",
    "ordered_locations.json",
)


def check_and_install_pyinstaller(lang):
    try:
        import PyInstaller
        print(t("build_pyinstaller_ok", lang, version=PyInstaller.__version__))
    except ImportError:
        print(t("build_pyinstaller_missing", lang))
        install_result = subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
        if install_result.returncode != 0:
            print(t("build_pyinstaller_install_err", lang))
            sys.exit(1)
        print(t("build_pyinstaller_installed", lang))


def build():
    lang = resolve_cli_lang()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)

    check_and_install_pyinstaller(lang)

    print("\n" + "=" * 60)
    print(t("build_banner_title", lang, app_name=APP_NAME.upper()))
    print("=" * 60)

    # Essential files that must be bundled into the executable
    for data_file in REQUIRED_DATA_FILES:
        if not os.path.exists(os.path.join(base_dir, data_file)):
            print(t("build_missing_file", lang, file=data_file))
            sys.exit(1)

    # Build PyInstaller command
    # On Windows, add-data separator is ';'
    pyinstaller_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",
        "--onefile",
        "--clean",
        "--name", EXE_NAME,
    ]
    for data_file in REQUIRED_DATA_FILES:
        pyinstaller_cmd.extend(["--add-data", f"{data_file}{os.pathsep}."])

    pyinstaller_cmd.append("app.py")

    print(t("build_running_cmd", lang, cmd=" ".join(pyinstaller_cmd)))
    build_result = subprocess.run(pyinstaller_cmd)

    if build_result.returncode == 0:
        exe_path = os.path.join(base_dir, "dist", f"{EXE_NAME}.exe")
        print("\n" + "=" * 60)
        print(t("build_success_title", lang))
        print("=" * 60)
        print(t("build_exe_location", lang, path=exe_path))
        print(t("build_exe_hint", lang))
        print("=" * 60 + "\n")
    else:
        print(t("build_failed", lang, code=build_result.returncode))
        sys.exit(build_result.returncode)


if __name__ == "__main__":
    build()
