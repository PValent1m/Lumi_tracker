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

if /i "%APP_LANG%"=="pt" (
    title Lumi Tracker - Diagnostico
    echo [1/3] Diretorio atual fixado em: %CD%
) else (
    title Lumi Tracker - Launcher
    echo [1/3] Working directory set to: %CD%
)

:: Check for local virtual environment
if exist ".venv\Scripts\python.exe" (
    if /i "%APP_LANG%"=="pt" (
        echo [2/3] Usando Python do ambiente virtual ^(.venv^)...
    ) else (
        echo [2/3] Using Python from virtual environment ^(.venv^)...
    )
    set "PY_CMD=.venv\Scripts\python.exe"
) else if exist "venv\Scripts\python.exe" (
    if /i "%APP_LANG%"=="pt" (
        echo [2/3] Usando Python do ambiente virtual ^(venv^)...
    ) else (
        echo [2/3] Using Python from virtual environment ^(venv^)...
    )
    set "PY_CMD=venv\Scripts\python.exe"
) else (
    if /i "%APP_LANG%"=="pt" (
        echo [2/3] Usando Python global do sistema...
    ) else (
        echo [2/3] Using system Python...
    )
    where python >nul 2>nul
    if !errorlevel! equ 0 (
        set "PY_CMD=python"
    ) else (
        set "PY_CMD=py"
    )
)

:: Check if pywebview is installed in the selected Python environment
%PY_CMD% -c "import webview" >nul 2>nul
if !errorlevel! neq 0 (
    if /i "%APP_LANG%"=="pt" (
        echo [AVISO] Biblioteca 'pywebview' nao encontrada. Instalando agora...
    ) else (
        echo [WARN] Library 'pywebview' not found. Installing now...
    )
    %PY_CMD% -m pip install pywebview
)

if /i "%APP_LANG%"=="pt" (
    echo [3/3] Iniciando app.py...
) else (
    echo [3/3] Starting app.py...
)
%PY_CMD% app.py %*
set "APP_EXIT=!errorlevel!"

if !APP_EXIT! neq 0 (
    echo.
    echo ========================================================
    if /i "%APP_LANG%"=="pt" (
        echo [ERRO] O app.py falhou ao iniciar ^(Codigo: !APP_EXIT!^).
        echo Iniciando servidor web local como alternativa...
    ) else (
        echo [ERROR] app.py failed to start ^(Code: !APP_EXIT!^).
        echo Starting local web server as fallback...
    )
    echo ========================================================
    %PY_CMD% server.py %*
)

echo.
pause
