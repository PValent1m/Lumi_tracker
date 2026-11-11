#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_exe.py
Script para empacotar o Lumi Tracker em um executável (.exe)
único e independente para Windows utilizando PyInstaller.
"""

import os
import sys
import subprocess

sys.stdout.reconfigure(encoding="utf-8")

APP_NAME = "Lumi Tracker"
EXE_NAME = "LumiTracker"
REQUIRED_DATA_FILES = (
    "index.html",
    "luminescent_encounters.json",
    "ordered_locations.json",
)


def check_and_install_pyinstaller():
    try:
        import PyInstaller
        print(f"[OK] PyInstaller detectado: versão {PyInstaller.__version__}")
    except ImportError:
        print("[INFO] PyInstaller não encontrado. Instalando via pip...")
        install_result = subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
        if install_result.returncode != 0:
            print("[ERRO] Falha ao instalar PyInstaller.")
            sys.exit(1)
        print("[OK] PyInstaller instalado com sucesso!")


def build():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)

    check_and_install_pyinstaller()

    print("\n" + "=" * 60)
    print(f"  COMPILAÇÃO DE EXECUTÁVEL (.EXE) - {APP_NAME.upper()}")
    print("=" * 60)

    # Arquivos essenciais que devem ser empacotados junto ao executável
    for data_file in REQUIRED_DATA_FILES:
        if not os.path.exists(os.path.join(base_dir, data_file)):
            print(f"[ERRO] Arquivo obrigatório não encontrado: {data_file}")
            sys.exit(1)

    # Monta comando PyInstaller
    # No Windows, o separador de add-data é ';'
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

    print(f"Executando comando:\n{' '.join(pyinstaller_cmd)}\n")
    build_result = subprocess.run(pyinstaller_cmd)

    if build_result.returncode == 0:
        exe_path = os.path.join(base_dir, "dist", f"{EXE_NAME}.exe")
        print("\n" + "=" * 60)
        print("  [SUCESSO] EXECUTÁVEL GERADO COM ÊXITO!")
        print("=" * 60)
        print(f"Local do executável: {exe_path}")
        print("Você pode mover esse arquivo .exe para qualquer pasta ou Área de Trabalho!")
        print("=" * 60 + "\n")
    else:
        print(f"\n[ERRO] A compilação falhou com código {build_result.returncode}.")
        sys.exit(build_result.returncode)


if __name__ == "__main__":
    build()
