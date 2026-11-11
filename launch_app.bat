@echo off
setlocal
cd /d "%~dp0"
title Lumi Tracker - Diagnostico

echo [1/3] Diretorio atual fixado em: %CD%

:: Verifica se existe ambiente virtual local
if exist ".venv\Scripts\python.exe" (
    echo [2/3] Usando Python do ambiente virtual ^(.venv^)...
    set "PY_CMD=.venv\Scripts\python.exe"
) else if exist "venv\Scripts\python.exe" (
    echo [2/3] Usando Python do ambiente virtual ^(venv^)...
    set "PY_CMD=venv\Scripts\python.exe"
) else (
    echo [2/3] Usando Python global do sistema...
    where python >nul 2>nul
    if %errorlevel% equ 0 (
        set "PY_CMD=python"
    ) else (
        set "PY_CMD=py"
    )
)

:: Verifica se o pywebview esta instalado nesse Python
%PY_CMD% -c "import webview" >nul 2>nul
if %errorlevel% neq 0 (
    echo [AVISO] Biblioteca 'pywebview' nao encontrada. Instalando agora...
    %PY_CMD% -m pip install pywebview
)

echo [3/3] Iniciando app.py...
%PY_CMD% app.py

if %errorlevel% neq 0 (
    echo.
    echo ========================================================
    echo [ERRO] O app.py falhou ao iniciar ^(Codigo: %errorlevel%^).
    echo Iniciando servidor web local como alternativa...
    echo ========================================================
    %PY_CMD% server.py
)

echo.
pause