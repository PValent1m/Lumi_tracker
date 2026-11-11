#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
server.py
Servidor local HTTP de contingência para o Luminescent Platinum - Playthrough Tracker.
Inicia um servidor HTTP na porta 8000 (ou na próxima porta disponível) e abre
automaticamente o navegador padrão na URL correspondente.
"""

import os
import sys
import socket
import threading
import time
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

# Força codificação UTF-8 no console Windows
sys.stdout.reconfigure(encoding="utf-8")


def get_base_dir():
    """Retorna o diretório base dos arquivos da aplicação."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def find_free_port(start_port=8000, max_attempts=30):
    """Encontra uma porta TCP livre começando em start_port."""
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    return start_port


def open_browser_delayed(url, delay=0.6):
    """Abre o navegador padrão após um breve intervalo."""
    time.sleep(delay)
    print(f"Abrindo navegador padrão em: {url}")
    webbrowser.open(url)


def main():
    base_dir = get_base_dir()
    os.chdir(base_dir)

    port = find_free_port(8000)
    server_address = ("127.0.0.1", port)
    url = f"http://localhost:{port}"

    class CustomHandler(SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            # Mensagens de requisição mais limpas no terminal
            sys.stdout.write(f"[{self.log_date_time_string()}] {format % args}\n")

    try:
        httpd = ThreadingHTTPServer(server_address, CustomHandler)
    except Exception as e:
        print(f"Erro ao iniciar servidor na porta {port}: {e}")
        sys.exit(1)

    print("=" * 60)
    print("  LUMINESCENT PLATINUM - SERVIDOR LOCAL DE CONTINGÊNCIA")
    print("=" * 60)
    print(f"  Diretório raiz : {base_dir}")
    print(f"  Endereço local : {url}")
    print("  Pressione Ctrl+C para encerrar o servidor a qualquer momento.")
    print("=" * 60 + "\n")

    # Inicia abertura do navegador em background
    threading.Thread(target=open_browser_delayed, args=(url,), daemon=True).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nEncerrando servidor local...")
        httpd.server_close()
        print("Servidor encerrado com sucesso.")


if __name__ == "__main__":
    main()
