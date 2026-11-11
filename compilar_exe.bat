@echo off
chcp 65001 >nul
title Luminescent Platinum - Compilador Executavel (.exe)
cd /d "%~dp0"

echo ============================================================
echo   Luminescent Platinum - Compilador de Executável (.exe)
echo ============================================================
echo.

python build_exe.py

echo.
pause
