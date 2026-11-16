@echo off
setlocal EnableDelayedExpansion
chcp 65001 >nul
cd /d "%~dp0"

set "APP_LANG=en"
if defined APPDATA (
    set "LANG_DIR=%APPDATA%\LumiTracker"
) else (
    set "LANG_DIR=%USERPROFILE%\LumiTracker"
)
set "LANG_FILE=%LANG_DIR%\lang.txt"

if exist "%LANG_FILE%" (
    set /p SAVED_LANG=<"%LANG_FILE%"
    if /i "!SAVED_LANG!"=="pt" set "APP_LANG=pt"
    if /i "!SAVED_LANG!"=="en" set "APP_LANG=en"
)

set "EXPLICIT_LANG="
set "EXPECT_LANG=0"
for %%A in (%*) do (
    set "ARG=%%~A"
    if "!EXPECT_LANG!"=="1" (
        if /i "!ARG!"=="pt" set "EXPLICIT_LANG=pt"
        if /i "!ARG!"=="pt-br" set "EXPLICIT_LANG=pt"
        if /i "!ARG!"=="en" set "EXPLICIT_LANG=en"
        if /i "!ARG!"=="en-us" set "EXPLICIT_LANG=en"
        set "EXPECT_LANG=0"
    ) else (
        if /i "!ARG!"=="--lang" set "EXPECT_LANG=1"
        if /i "!ARG!"=="-l" set "EXPECT_LANG=1"
        if /i "!ARG!"=="--lang=pt" set "EXPLICIT_LANG=pt"
        if /i "!ARG!"=="--lang=pt-br" set "EXPLICIT_LANG=pt"
        if /i "!ARG!"=="--lang=en" set "EXPLICIT_LANG=en"
        if /i "!ARG!"=="--lang=en-us" set "EXPLICIT_LANG=en"
        if /i "!ARG!"=="-l=pt" set "EXPLICIT_LANG=pt"
        if /i "!ARG!"=="-l=en" set "EXPLICIT_LANG=en"
    )
)

if defined EXPLICIT_LANG (
    set "APP_LANG=!EXPLICIT_LANG!"
    if not exist "%LANG_DIR%" mkdir "%LANG_DIR%"
    > "%LANG_FILE%" <nul set /p "=!APP_LANG!"
)

echo ============================================================
if /i "%APP_LANG%"=="pt" (
    title Lumi Tracker - Servidor Local
    echo   Lumi Tracker - Servidor Local de Contingência
) else (
    title Lumi Tracker - Local Server
    echo   Lumi Tracker - Local Fallback Server
)
echo ============================================================
echo.

:: Detect Python (local virtualenv, python, or py launcher)
set "PY_CMD="
if exist ".venv\Scripts\python.exe" (
    set "PY_CMD=.venv\Scripts\python.exe"
) else if exist "venv\Scripts\python.exe" (
    set "PY_CMD=venv\Scripts\python.exe"
) else (
    where python >nul 2>nul
    if !errorlevel! equ 0 (
        set "PY_CMD=python"
    ) else (
        where py >nul 2>nul
        if !errorlevel! equ 0 (
            set "PY_CMD=py"
        )
    )
)

if not defined PY_CMD (
    if /i "%APP_LANG%"=="pt" (
        echo [ERRO] Python não foi encontrado no sistema.
        echo Por favor, instale o Python 3.10+ e adicione ao PATH.
    ) else (
        echo [ERROR] Python was not found on the system.
        echo Please install Python 3.10+ and add it to PATH.
    )
    echo.
    pause
    exit /b 1
)

if /i "%APP_LANG%"=="pt" (
    echo Iniciando servidor HTTP local e abrindo navegador padrão...
) else (
    echo Starting local HTTP server and opening default browser...
)
echo.
%PY_CMD% server.py %*

if !errorlevel! neq 0 (
    echo.
    if /i "%APP_LANG%"=="pt" (
        echo [INFO] O servidor foi encerrado.
    ) else (
        echo [INFO] The server has stopped.
    )
    pause
)
