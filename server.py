#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
server.py
Local HTTP fallback server for Lumi Tracker.
Starts an HTTP server on port 8000 (or the next available port) and automatically
opens the default web browser at the corresponding URL.
"""

import json
import os
import sys
import socket
import threading
import time
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from i18n_cli import (
    load_saved_lang,
    load_saved_state,
    normalize_lang,
    resolve_cli_lang,
    save_lang,
    save_state,
    t,
)

# Force UTF-8 encoding on Windows console
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

APP_NAME = "Lumi Tracker"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000


def get_base_dir():
    """Return the base directory for application files."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def find_free_port(start_port=DEFAULT_PORT, max_attempts=30):
    """Find an available TCP port starting at start_port."""
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind((DEFAULT_HOST, port))
                return port
            except OSError:
                continue
    return start_port


def open_browser_delayed(url, delay=0.6):
    """Open the default browser after a short delay."""
    time.sleep(delay)
    print(t("server_open_browser", load_saved_lang(), url=url))
    webbrowser.open(url)


def main():
    lang = resolve_cli_lang()
    base_dir = get_base_dir()
    os.chdir(base_dir)

    port = find_free_port(DEFAULT_PORT)
    server_address = (DEFAULT_HOST, port)
    url = f"http://localhost:{port}"

    class TrackerHTTPHandler(SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
            super().end_headers()

        def _send_json(self, status_code, payload):
            body = json.dumps(payload).encode("utf-8")
            self.send_response(status_code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            clean_path = self.path.split("?", 1)[0]
            if clean_path == "/api/lang":
                self._send_json(200, {"lang": load_saved_lang()})
                return
            if clean_path == "/api/state":
                self._send_json(200, load_saved_state())
                return
            super().do_GET()

        def do_POST(self):
            clean_path = self.path.split("?", 1)[0]
            if clean_path == "/api/lang":
                try:
                    content_length = int(self.headers.get("Content-Length", "0"))
                    raw_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
                    data = json.loads(raw_body.decode("utf-8"))
                    requested_lang = normalize_lang(data.get("lang"))
                    if not requested_lang:
                        self._send_json(400, {"ok": False, "error": "Invalid language"})
                        return
                    saved_lang = save_lang(requested_lang)
                    print(t("server_lang_changed", saved_lang, lang_code=saved_lang.upper()))
                    self._send_json(200, {"ok": True, "lang": saved_lang})
                except Exception as exc:
                    self._send_json(400, {"ok": False, "error": str(exc)})
                return
            if clean_path == "/api/state":
                try:
                    content_length = int(self.headers.get("Content-Length", "0"))
                    raw_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
                    data = json.loads(raw_body.decode("utf-8"))
                    if not isinstance(data, dict):
                        self._send_json(400, {"ok": False, "error": "Invalid state payload"})
                        return
                    saved = save_state(data)
                    self._send_json(200, {"ok": True, **saved})
                except Exception as exc:
                    self._send_json(400, {"ok": False, "error": str(exc)})
                return
            self.send_error(404, "Not Found")

        def log_message(self, log_format, *args):
            # Cleaner request logs in terminal
            sys.stdout.write(f"[{self.log_date_time_string()}] {log_format % args}\n")

    try:
        httpd = ThreadingHTTPServer(server_address, TrackerHTTPHandler)
    except Exception as e:
        print(t("server_start_error", lang, port=port, error=e))
        sys.exit(1)

    print("=" * 60)
    print(f"  {t('server_banner_title', lang, app_name=APP_NAME.upper())}")
    print("=" * 60)
    print(t("server_root_dir", lang, base_dir=base_dir))
    print(t("server_local_url", lang, url=url))
    print(t("server_active_lang", lang, lang_code=lang.upper()))
    print(t("server_ctrl_c", lang))
    print("=" * 60 + "\n")

    # Open browser in background thread
    threading.Thread(target=open_browser_delayed, args=(url,), daemon=True).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        current_lang = load_saved_lang()
        print(t("server_shutting_down", current_lang))
        httpd.server_close()
        print(t("server_stopped", current_lang))


if __name__ == "__main__":
    main()
