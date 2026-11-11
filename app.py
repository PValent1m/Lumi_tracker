#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
app.py
Lançador Desktop para o Luminescent Platinum - Playthrough Tracker.
Usa pywebview para criar uma janela nativa independente e leve no Windows,
com servidor HTTP embutido e persistência de localStorage em %APPDATA%/LumiTracker.
"""

import os
import sys
import webview


def get_base_dir():
    """Retorna o diretório base da aplicação (compatível com PyInstaller e script)."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def main():
    BASE_DIR = get_base_dir()
    os.chdir(BASE_DIR)

    # Diretório seguro e persistente para localStorage, cookies e dados do WebView2
    appdata = os.environ.get("APPDATA", os.path.expanduser("~"))
    storage_path = os.path.join(appdata, "LumiTracker")
    os.makedirs(storage_path, exist_ok=True)

    # Habilita downloads de arquivos (necessário para o botão de Backup JSON)
    webview.settings["ALLOW_DOWNLOADS"] = True
    webview.settings["ALLOW_FILE_URLS"] = True

    # Cria a janela nativa do Desktop
    window = webview.create_window(
        title="Luminescent Platinum - Playthrough Tracker",
        url="index.html",
        width=1200,
        height=800,
        resizable=True,
        min_size=(800, 600),
    )

    # Inicia o app com:
    # - http_server=True: serve os assets via HTTP local seguro (evita bloqueios de CORS no fetch)
    # - private_mode=False: garante persistência do localStorage entre sessões
    # - storage_path: pasta dedicada em %APPDATA%/LumiTracker
    webview.start(
        http_server=True,
        private_mode=False,
        storage_path=storage_path,
    )


if __name__ == "__main__":
    main()
