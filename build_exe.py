#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_exe.py
Script para empacotar o Luminescent Platinum - Playthrough Tracker em um executável (.exe)
único e independente para Windows utilizando PyInstaller.
"""

import os
import sys
import subprocess
import shutil

sys.stdout.reconfigure(encoding="utf-8")


def check_and_install_pyinstaller():
    try:
        import PyInstaller
        print(f"[OK] PyInstaller detectado: versão {PyInstaller.__version__}")
    except ImportError:
        print("[INFO] PyInstaller não encontrado. Instalando via pip...")
        res = subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
        if res.returncode != 0:
            print("[ERRO] Falha ao instalar PyInstaller.")
            sys.exit(1)
        print("[OK] PyInstaller instalado com sucesso!")


def build():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)

    check_and_install_pyinstaller()

    print("\n" + "=" * 60)
    print("  COMPILAÇÃO DE EXECUTÁVEL (.EXE) - LUMINESCENT TRACKER")
    print("=" * 60)

    # Arquivos essenciais que devem ser empacotados junto ao executável
    data_files = [
        "index.html",
        "luminescent_encounters.json",
        "ordered_locations.json"
    ]

    for f in data_files:
        if not os.path.exists(os.path.join(base_dir, f)):
            print(f"[ERRO] Arquivo obrigatório não encontrado: {f}")
            sys.exit(1)

    # Monta comando PyInstaller
    # No Windows, o separador de add-data é ';'
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",
        "--onefile",
        "--clean",
        "--name", "LuminescentTracker",
        "--add-data", f"index.html{os.pathsep}.",
        "--add-data", f"luminescent_encounters.json{os.pathsep}.",
        "--add-data", f"ordered_locations.json{os.pathsep}.",
    ]

    cmd.append("app.py")

    print(f"Executando comando:\n{' '.join(cmd)}\n")
    result = subprocess.run(cmd)

    if result.returncode == 0:
        exe_path = os.path.join(base_dir, "dist", "LuminescentTracker.exe")
        print("\n" + "=" * 60)
        print("  [SUCESSO] EXECUTÁVEL GERADO COM ÊXITO!")
        print("=" * 60)
        print(f"Local do executável: {exe_path}")
        print("Você pode mover esse arquivo .exe para qualquer pasta ou Área de Trabalho!")
        print("=" * 60 + "\n")
    else:
        print(f"\n[ERRO] A compilação falhou com código {result.returncode}.")
        sys.exit(result.returncode)


if __name__ == "__main__":
    build()
