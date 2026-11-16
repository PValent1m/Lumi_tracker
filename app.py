#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
app.py
Desktop launcher for Lumi Tracker.
Uses pywebview to create a lightweight standalone native window on Windows,
with an embedded HTTP server and localStorage persistence in %APPDATA%/LumiTracker.
"""

import os
import shutil
import sys
import webview

from i18n_cli import (
    get_storage_dir,
    load_saved_lang,
    load_saved_state,
    resolve_cli_lang,
    save_lang,
    save_state,
    t,
)

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

APP_TITLE = "Lumi Tracker"


class LumiDesktopApi:
    """JS API bridge exposed to index.html for unified language and state persistence."""

    def get_lang(self):
        return load_saved_lang()

    def set_lang(self, lang):
        return save_lang(lang)

    def get_state(self):
        return load_saved_state()

    def set_state(self, state):
        return save_state(state)


def get_base_dir():
    """Return the application base directory (compatible with PyInstaller and script mode)."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def clear_webview_http_cache(storage_path):
    """
    Remove stale WebView2 HTTP/code cache directories while preserving
    Local Storage, Session Storage, and user progress data.
    """
    default_profile = os.path.join(storage_path, "EBWebView", "Default")
    for cache_dir_name in ("Cache", "Code Cache"):
        cache_dir = os.path.join(default_profile, cache_dir_name)
        if os.path.isdir(cache_dir):
            shutil.rmtree(cache_dir, ignore_errors=True)


def disable_bottle_static_cache():
    """
    Ensure pywebview's BottleServer attaches no-store cache headers directly to
    HTTPResponse objects returned by bottle.static_file (bottle.response headers
    are otherwise bypassed when static_file returns a new HTTPResponse).
    """
    try:
        import bottle
    except ImportError:
        return

    if getattr(bottle.static_file, "_lumi_no_cache", False):
        return

    orig_static_file = bottle.static_file

    def no_cache_static_file(*args, **kwargs):
        kwargs.setdefault("etag", False)
        resp = orig_static_file(*args, **kwargs)
        if hasattr(resp, "set_header"):
            resp.set_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
            resp.set_header("Pragma", "no-cache")
            resp.set_header("Expires", "0")
        return resp

    no_cache_static_file._lumi_no_cache = True
    bottle.static_file = no_cache_static_file


def main():
    lang = resolve_cli_lang()
    base_dir = get_base_dir()
    os.chdir(base_dir)

    storage_path = get_storage_dir()
    clear_webview_http_cache(storage_path)
    disable_bottle_static_cache()

    if sys.stdout:
        print(t("app_starting", lang, app_name=APP_TITLE, lang_code=lang.upper()))

    # Enable file downloads (required for the JSON Backup button)
    webview.settings["ALLOW_DOWNLOADS"] = True
    webview.settings["ALLOW_FILE_URLS"] = True

    # Create native Desktop window
    webview.create_window(
        title=APP_TITLE,
        url="index.html",
        js_api=LumiDesktopApi(),
        width=1200,
        height=800,
        resizable=True,
        min_size=(800, 600),
    )

    # Start the app with:
    # - http_server=True: serves assets over secure local HTTP (avoids fetch CORS issues)
    # - private_mode=False: ensures localStorage persists across sessions
    # - storage_path: dedicated folder in %APPDATA%/LumiTracker
    webview.start(
        http_server=True,
        private_mode=False,
        storage_path=storage_path,
    )


if __name__ == "__main__":
    main()
