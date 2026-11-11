@echo off
chcp 65001 >nul
title Luminescent Platinum - Servidor Local
cd /d "%~dp0"

echo ============================================================
echo   Luminescent Platinum - Servidor Local de Contingência
echo ============================================================
echo.

:: Verifica se o Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python não foi encontrado no sistema.
    echo Por favor, instale o Python 3.10+ e adicione ao PATH.
    echo.
    pause
    exit /b 1
)

echo Iniciando servidor HTTP local e abrindo navegador padrão...
echo.
python server.py

if %errorlevel% neq 0 (
    echo.
    echo [INFO] O servidor foi encerrado.
    pause
)
