@echo off
title IA_FUAG - Captura de Gestos
chcp 65001 > nul
echo =============================================================================
echo               IA_FUAG - COLETOR DE FOTOS PARA DATASET
echo =============================================================================
echo.

if not exist venv (
    echo [AVISO] O ambiente virtual 'venv' nao foi encontrado.
    echo Executando configuracao automatica primeiro...
    call setup.bat
)

call venv\Scripts\activate.bat
python capture_gestures.py %*

echo.
pause
