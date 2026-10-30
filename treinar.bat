@echo off
title IA_FUAG - Treinamento de Modelo
chcp 65001 > nul
echo =============================================================================
echo               IA_FUAG - INICIANDO PIPELINE DE TREINAMENTO
echo =============================================================================
echo.

if not exist venv (
    echo [AVISO] O ambiente virtual 'venv' nao foi encontrado.
    echo Executando configuracao automatica primeiro...
    call setup.bat
)

call venv\Scripts\activate.bat
python train_model.py

echo.
pause
