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
    title Lumi Tracker - Compilador Executavel ^(.exe^)
    echo   Lumi Tracker - Compilador de Executável ^(.exe^)
) else (
    title Lumi Tracker - Executable Builder ^(.exe^)
    echo   Lumi Tracker - Executable Builder ^(.exe^)
)
echo ============================================================
echo.

python build_exe.py %*

echo.
pause
