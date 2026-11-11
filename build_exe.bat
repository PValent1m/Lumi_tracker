@echo off
chcp 65001 >nul
title Lumi Tracker - Compilador Executavel (.exe)
cd /d "%~dp0"

echo ============================================================
echo   Lumi Tracker - Compilador de Executável (.exe)
echo ============================================================
echo.

python build_exe.py

echo.
pause
