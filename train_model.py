r"""
=============================================================================
 GUIA DE SETUP RÁPIDO NO TERMINAL (WINDOWS / VS CODE)
=============================================================================
Copie e cole os comandos abaixo sequencialmente no terminal do VS Code:

1. Criar o ambiente virtual Python:
   python -m venv venv

2. Ativar o ambiente virtual no Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   (Nota: Se houver restricao de script no PowerShell, execute:
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass)

3. Instalar as dependencias do projeto:
   pip install -r requirements.txt

4. Executar o treinamento:
   python train_model.py
=============================================================================
"""

import os
import sys

# Reduz mensagens de log verbosas do TensorFlow no console
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

try:
    from mediapipe_model_maker import gesture_recognizer
except ImportError:
    # Mensagem explicativa caso o script seja executado sem o ambiente virtual ativo
    print("\n[ERRO]: A biblioteca 'mediapipe-model-maker' nao esta instalada neste ambiente Python.")
    print("Siga os passos de inicializacao:")
    print(r"  1. Ative a venv: .\venv\Scripts\Activate.ps1")
    print("  2. Instale os requisitos: pip install -r requirements.txt")
    print("  3. Execute novamente: python train_model.py\n")
    sys.exit(1)


def main():
    # -------------------------------------------------------------------------
    # 1. DEFINIÇÃO SEGURA DE CAMINHOS RELATIVOS
    # -------------------------------------------------------------------------
    # Define os caminhos baseados na localização deste script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(base_dir, "dataset")
    exported_models_dir = os.path.join(base_dir, "exported_models")

    # Garante que o diretório de saída existe
    os.makedirs(exported_models_dir, exist_ok=True)

    print("=" * 60)
    print(" INICIANDO PIPELINE DE TREINAMENTO - MEDIAPIPE GESTURE RECOGNIZER ")
    print("=" * 60)

    # -------------------------------------------------------------------------
    # 2. VERIFICAÇÃO DE DADOS & REQUISITOS ANATÔMICOS (LABELS DINÂMICAS)
    # -------------------------------------------------------------------------
    # LABELS DINÂMICAS (ZERO PRESETS):
    # - Não há nenhuma label ou classe pré-configurada no código.
    # - O MediaPipe Model Maker extrai automaticamente as labels a partir do
    #   nome de cada subpasta presente no diretório 'dataset/'.
    # - Exemplo de estrutura:
    #     dataset/
    #       ├── none/                   (classe negativa recomendada / mão em repouso)
    #       ├── gesto_personalizado_a/  (qualquer nome de gesto manual desejado)
    #       └── gesto_personalizado_b/
    #
    # AVISO DE RESTRIÇÃO ANATÔMICA OBRIGATÓRIA (MÃOS VISÍVEIS):
    # - O pipeline 'gesture_recognizer' opera exclusivamente sobre pontos anatômicos
    #   de mãos (Hand Landmarks com 21 pontos-chave).
    # - TODAS as imagens do dataset DEVEM conter obrigatoriamente mãos humanas visíveis.
    # - Imagens contendo rostos, expressões faciais, corpo inteiro sem mãos,
    #   ou fundos vazios serão automaticamente ignoradas/descartadas pelo
    #   extrator de landmarks do Google durante o pré-processamento.
    # -------------------------------------------------------------------------
    subdirs = [
        d
        for d in os.listdir(dataset_dir)
        if os.path.isdir(os.path.join(dataset_dir, d))
    ] if os.path.exists(dataset_dir) else []

    # Checa se há classes com imagens
    has_images = any(
        len([
            f for f in os.listdir(os.path.join(dataset_dir, sd))
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ]) > 0
        for sd in subdirs
    )

    if not has_images:
        print("\n[AVISO]: Nenhuma imagem encontrada para treinamento!")
        print(f"Por favor, adicione suas fotos dentro de: {dataset_dir}")
        print("Organize em subpastas por gesto manual (labels dinâmicas), por exemplo:")
        print(f"  {os.path.join(dataset_dir, 'none')}")
        print(f"  {os.path.join(dataset_dir, 'gesto_personalizado_a')}")
        print(f"  {os.path.join(dataset_dir, 'gesto_personalizado_b')}")
        print("\nIMPORTANTE: Todas as imagens devem conter maos humanas visiveis.")
        print("Apos adicionar as imagens, execute este script novamente.")
        return

    # -------------------------------------------------------------------------
    # 3. CARREGAMENTO DO DATASET
    # -------------------------------------------------------------------------
    print(f"\n[1/5] Carregando dataset a partir de: {dataset_dir}")
    data = gesture_recognizer.Dataset.from_folder(
        dirname=dataset_dir,
        hparams=gesture_recognizer.HandDataPreprocessingParams()
    )

    # -------------------------------------------------------------------------
    # 4. DIVISÃO DOS DADOS (TRAIN / VALIDATION / TEST)
    # -------------------------------------------------------------------------
    # Divisão: 80% treino, 10% validação e 10% teste
    print("\n[2/5] Dividindo dados (80% treino, 10% validação, 10% teste)...")
    train_data, rest_data = data.split(0.8)
    validation_data, test_data = rest_data.split(0.5)

    # -------------------------------------------------------------------------
    # 5. CONFIGURAÇÃO DE HIPERPARÂMETROS (HPARAMS)
    # -------------------------------------------------------------------------
    # AJUSTE DE PRECISÃO:
    # - 'epochs': Número de épocas de treinamento.
    #             Valor inicial sensato: 10.
    #             Se o modelo errar muito ou precisar de mais precisão, aumente
    #             para 20, 30 ou 50 épocas (observe se a loss de validação cai).
    # - 'batch_size': Quantidade de amostras processadas por passo (padrão: 2).
    # - 'export_dir': Diretório onde os artefatos de treinamento serão gerados.
    # -------------------------------------------------------------------------
    print("\n[3/5] Configurando hiperparâmetros...")
    hparams = gesture_recognizer.HParams(
        export_dir=exported_models_dir,
        epochs=10,        # <-- Aumente aqui caso queira treinar por mais épocas
        batch_size=2      # <-- Tamanho de lote adequado para datasets moderados
    )
    options = gesture_recognizer.GestureRecognizerOptions(hparams=hparams)

    # -------------------------------------------------------------------------
    # 6. TREINAMENTO DO MODELO
    # -------------------------------------------------------------------------
    print("\n[4/5] Treinando modelo Gesture Recognizer...")
    model = gesture_recognizer.GestureRecognizer.create(
        train_data=train_data,
        validation_data=validation_data,
        options=options
    )

    # -------------------------------------------------------------------------
    # 7. AVALIAÇÃO COM DADOS DE TESTE
    # -------------------------------------------------------------------------
    print("\n[5/5] Avaliando acurácia no conjunto de teste...")
    loss, acc = model.evaluate(test_data, batch_size=2)
    print("-" * 40)
    print(f"  Perda no Teste (Loss):     {loss:.4f}")
    print(f"  Acurácia no Teste (Acc):   {acc * 100:.2f}%")
    print("-" * 40)

    # -------------------------------------------------------------------------
    # 8. EXPORTAÇÃO DO MODELO .TASK PARA O FLUTTER
    # -------------------------------------------------------------------------
    model_output_filename = "gesture_recognizer.task"
    print(f"\nExportando modelo para: {os.path.join(exported_models_dir, model_output_filename)}")
    model.export_model(model_name=model_output_filename)

    print("\n" + "=" * 60)
    print(" TREINAMENTO E EXPORTAÇÃO CONCLUÍDOS COM SUCESSO! ")
    print(f" Modelo salvo em: {os.path.join(exported_models_dir, model_output_filename)}")
    print(" Pronto para integrar no Flutter via MediaPipe Vision Tasks.")
    print("=" * 60)


if __name__ == "__main__":
    main()
