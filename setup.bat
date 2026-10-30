@echo off
title IA_FUAG - Instalacao do Ambiente
chcp 65001 > nul
echo =============================================================================
echo               IA_FUAG - CONFIGURACAO INICIAL DO AMBIENTE
echo =============================================================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao foi encontrado no PATH do sistema.
    echo Por favor, instale o Python (recomendado 3.9, 3.10 ou 3.11).
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/3] Criando ambiente virtual (venv)...
python -m venv venv
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao criar o ambiente virtual.
    pause
    exit /b 1
)

echo [2/3] Atualizando gerenciador pip...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip

echo [3/3] Instalando dependencias do projeto (mediapipe, tensorflow, opencv)...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [AVISO] Falha na instalacao das dependencias.
    echo Lembrete: O MediaPipe Model Maker requer Python 3.9, 3.10 ou 3.11.
    echo Se voce estiver usando Python 3.12+, instale o Python 3.11.
    pause
    exit /b 1
)

echo.
echo =============================================================================
echo           AMBIENTE CONFIGURADO COM SUCESSO!
echo =============================================================================
echo Proximos passos:
echo   - Para capturar imagens: execute capturar.bat
echo   - Para treinar o modelo:  execute treinar.bat
echo   - Para testar na webcam:  execute testar.bat
echo =============================================================================
pause
