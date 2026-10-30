@echo off
title IA_FUAG - Teste em Tempo Real
chcp 65001 > nul
echo =============================================================================
echo               IA_FUAG - TESTADOR DO MODELO NA WEBCAM
echo =============================================================================
echo.

if not exist venv (
    echo [AVISO] O ambiente virtual 'venv' nao foi encontrado.
    echo Executando configuracao automatica primeiro...
    call setup.bat
)

call venv\Scripts\activate.bat
python test_model.py

echo.
pause
