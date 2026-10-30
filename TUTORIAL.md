# 📖 Tutorial Prático: Criando Novos Movimentos de IA para o FUAG

Bem-vindo ao tutorial definitivo de criação de entradas gestuais para o **FUAG (Ferramenta Universal de Acessibilidade em Games)**!

Neste tutorial prático "mão na massa", vamos construir juntos um conjunto de **3 novos controles gestuais** para um jogo de corrida ou simulador gamer:
1. `acelerar`: Palma aberta ou punho estendido para frente (acelera o carro).
2. `frear`: Mão aberta levantada com a palma voltada para a câmera (freia / ré).
3. `nitro`: Polegar levantado em sinal de positivo 👍 (dispara nitro ou turbo).
4. `none`: Mão em repouso natural, relaxada (não aciona nada).

Ao final deste guia, você terá exportado um arquivo `.task` pronto e saberá exatamente como plugá-lo no FUAG para controlar seus jogos na Steam, emuladores ou Game Pass.

---

## 📋 Sumário

1. [Fase 1: Preparando o Ambiente Python](#fase-1-preparando-o-ambiente-python)
2. [Fase 2: Planejamento Ergonômico dos Gestos](#fase-2-planejamento-ergonômico-dos-gestos)
3. [Fase 3: Coletando o Dataset com a Ferramenta de Captura](#fase-3-coletando-o-dataset-com-a-ferramenta-de-captura)
4. [Fase 4: Treinando o Modelo com o MediaPipe](#fase-4-treinando-o-modelo-com-o-mediapipe)
5. [Fase 5: Testando e Validando na Webcam](#fase-5-testando-e-validando-na-webcam)
6. [Fase 6: Integrando o Novo Gesto ao FUAG](#fase-6-integrando-o-novo-gesto-ao-fuag)
7. [Fase 7: Solução de Problemas Frequentes](#fase-7-solução-de-problemas-frequentes)

---

## 🛠️ Fase 1: Preparando o Ambiente Python

### 1.1 Verificando a Versão do Python

Abra o terminal do PowerShell e certifique-se de estar utilizando **Python 3.9, 3.10 ou 3.11**:

```powershell
python --version
```

> **Atenção:** Se sua versão for Python 3.12 ou 3.13, o MediaPipe Model Maker não encontrará pacotes pré-compilados do TensorFlow. Baixe e instale o [Python 3.11](https://www.python.org/downloads/release/python-3110/) caso necessário.

### 1.2 Configurando o Ambiente Virtual

Execute o script automático ou os comandos no terminal:

```powershell
# Opção 1: Usar o script facilitador
.\setup.bat

# Opção 2: Linha de comando manual
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🧠 Fase 2: Planejamento Ergonômico dos Gestos

Antes de ligar a câmera, planeje os gestos com foco em acessibilidade e ergonomia:

| Nome da Pasta / Label | Descrição Anatômica | Comando no Jogo | Dica Ergonômica |
| :--- | :--- | :--- | :--- |
| `none` | Mão relaxada, repousando na mesa ou colo | Nenhuma ação (Solta gatilhos) | Essencial para descansar a musculatura |
| `acelerar` | Palma voltada para a mesa ou punho cerrado | Gatilho `RT` (Gás) | Movimento firme e estável |
| `frear` | Mão aberta em sinal de "Pare" (palma para a câmera) | Gatilho `LT` (Freio) | Fácil de alternar rapidamente |
| `nitro` | Polegar voltado para cima (👍) | Botão `A` / `Cross` | Distinto dos outros gestos para evitar disparo acidental |

---

## 📸 Fase 3: Coletando o Dataset com a Ferramenta de Captura

O projeto já inclui o utilitário `capture_gestures.py` com HUD na tela para facilitar sua vida.

### 3.1 Coletando a Classe de Repouso (`none`)

A classe `none` é a mais importante do dataset! Ela ensina a IA a **não reagir** quando você estiver apenas repousando a mão.

Execute:
```powershell
python capture_gestures.py --label none
```

1. Coloque sua mão no enquadramento em posição relaxada.
2. Pressione a tecla **`B`** para ligar o **Modo Rajada** (captura contínua automática).
3. Mova suavemente a mão, gire ligeiramente o punho, afaste e aproxime da câmera.
4. Ao atingir entre **40 e 60 fotos**, pressione `B` para pausar ou `Q` para sair.

### 3.2 Coletando o Gesto `acelerar`

```powershell
python capture_gestures.py --label acelerar
```
1. Faça o gesto escolhido para aceleração.
2. Capture entre **40 e 60 fotos** com pequenas variações de ângulo.
3. Pressione `Q` para salvar.

### 3.3 Coletando o Gesto `frear`

```powershell
python capture_gestures.py --label frear
```
1. Faça a pose de freio.
2. Capture entre **40 e 60 fotos**.
3. Pressione `Q` para salvar.

### 3.4 Coletando o Gesto `nitro`

```powershell
python capture_gestures.py --label nitro
```
1. Faça o gesto do polegar levantado.
2. Capture entre **40 e 60 fotos**.
3. Pressione `Q` para salvar.

### 3.5 Verificando a Estrutura de Pastas

Após a captura, sua pasta `dataset/` estará organizada da seguinte forma:

```text
dataset/
├── none/          (ex: 50 fotos)
├── acelerar/      (ex: 50 fotos)
├── frear/         (ex: 50 fotos)
└── nitro/         (ex: 50 fotos)
```

---

## ⚡ Fase 4: Treinando o Modelo com o MediaPipe

Com as imagens salvas, o treinamento é 100% automático.

Execute:
```powershell
python train_model.py
# Ou execute treinar.bat
```

### O que acontece durante a execução:

1. **Validação Anatômica:** O extrator do Google detecta os 21 pontos da mão em cada foto. Imagens borradas ou sem mãos são descartadas automaticamente.
2. **Separação do Dataset:** Os dados são divididos em 80% treino, 10% validação e 10% teste cego.
3. **Treinamento por Transfer Learning:** A rede neural é refinada por 10 épocas.
4. **Relatório de Acurácia:** O terminal exibirá a taxa de acerto no conjunto de teste:
   ```text
   ----------------------------------------
     Perda no Teste (Loss):     0.0412
     Acurácia no Teste (Acc):   98.50%
   ----------------------------------------
   ```
5. **Exportação:** O arquivo compilado final é gerado em:
   `exported_models/gesture_recognizer.task`

> **Dica de Calibração:** Se a acurácia ficar abaixo de 90%, abra o arquivo `train_model.py` e altere o parâmetro `epochs=10` na linha 135 para `epochs=20` ou `epochs=30`.

---

## 🧪 Fase 5: Testando e Validando na Webcam

Antes de abrir o jogo, certifique-se de que a IA responde com rapidez e estabilidade.

Execute o script de teste:
```powershell
python test_model.py
# Ou execute testar.bat
```

- A janela da webcam abrirá.
- Faça o gesto de `acelerar`: o banner superior deve indicar **GESTO: ACELERAR** em verde com confiança superior a 80%.
- Faça o gesto de `nitro`: o banner mudará para **GESTO: NITRO**.
- Relaxe a mão: o banner mudará para **NEUTRO / NONE**.
- Pressione `Q` para fechar.

---

## 🎮 Fase 6: Integrando o Novo Gesto ao FUAG

Agora que seu modelo `gesture_recognizer.task` está pronto, vamos conectá-lo ao **FUAG**.

### 6.1 Copiando o Arquivo para o FUAG

Copie o arquivo:
```text
C:\...\IA_FUAG\exported_models\gesture_recognizer.task
```
Para a raiz do seu projeto FUAG:
```text
C:\...\FUAG\gesture_recognizer.task
```

### 6.2 Integrando no `pc_local_controller.py` do FUAG

No arquivo principal do FUAG (`pc_local_controller.py`), configure o leitor do MediaPipe e o driver **ViGEmBus** (`vgamepad`) para traduzir os gestos em comandos de controle do Xbox 360 ou PS4:

```python
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import vgamepad as vg

# 1. Cria a instância do controle virtual de Xbox 360
gamepad = vg.VX360Gamepad()

# 2. Configura o modelo compilado do IA_FUAG
base_options = python.BaseOptions(model_asset_path="gesture_recognizer.task")
options = vision.GestureRecognizerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.IMAGE,
    num_hands=1
)
recognizer = vision.GestureRecognizer.create_from_options(options)

# 3. Abre a webcam local (zero latência)
cap = cv2.VideoCapture(0)

# Variável de estado para evitar comandos redundantes
ultimo_gesto = "none"

print("[FUAG] Controle Gestual Ativado! Abra seu jogo favorito.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    result = recognizer.recognize(mp_image)

    gesto_atual = "none"
    if result.gestures and len(result.gestures[0]) > 0:
        top_gesture = result.gestures[0][0]
        # Aplica filtro de confiança mínima de 70%
        if top_gesture.score >= 0.70:
            gesto_atual = top_gesture.category_name

    # 4. MAPEAMENTO DE ENTRADAS PARA O JOGO
    if gesto_atual != ultimo_gesto:
        if gesto_atual == "acelerar":
            print(">> [FUAG] ACELERANDO (RT)")
            gamepad.left_trigger_float(0.0)
            gamepad.right_trigger_float(1.0) # Gatilho RT no máximo
            gamepad.update()

        elif gesto_atual == "frear":
            print(">> [FUAG] FREANDO (LT)")
            gamepad.right_trigger_float(0.0)
            gamepad.left_trigger_float(1.0)  # Gatilho LT no máximo
            gamepad.update()

        elif gesto_atual == "nitro":
            print(">> [FUAG] NITRO ATIVADO (Botão A)")
            gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
            gamepad.update()

        elif gesto_atual == "none":
            print(">> [FUAG] NEUTRO / REPOUSO")
            gamepad.right_trigger_float(0.0)
            gamepad.left_trigger_float(0.0)
            gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
            gamepad.update()

        ultimo_gesto = gesto_atual

    # HUD Visual no PC
    cv2.putText(frame, f"Comando: {gesto_atual.upper()}", (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
    cv2.imshow("FUAG - Controle Ativo", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
```

---

## ❓ Fase 7: Solução de Problemas Frequentes

### 1. `[ERRO]: A biblioteca 'mediapipe-model-maker' nao esta instalada`
- **Causa:** O script foi executado fora do ambiente virtual `venv`.
- **Solução:** Ative a venv antes de rodar:
  ```powershell
  .\venv\Scripts\Activate.ps1
  python train_model.py
  ```

### 2. O modelo erra ou confunde dois gestos
- **Causa:** Gestos muito parecidos geometricamente ou poucas fotos no dataset.
- **Solução:**
  - Adicione mais 20 fotos para cada um dos gestos confusos.
  - Varie a distância da mão em relação à câmera.
  - No `train_model.py`, mude `epochs=10` para `epochs=20`.

### 3. As ações disparam sozinhas no jogo sem eu fazer o gesto
- **Causa:** Falta de imagens na classe `none`.
- **Solução:** Tire pelo menos 50 fotos na pasta `dataset/none/` contendo sua mão em diferentes posições neutras e relaxadas. No código de integração do FUAG, aumente a exigência de confiança para `score >= 0.75`.

---

🎉 **Parabéns!** Você aprendeu todo o fluxo para expandir a biblioteca de movimentos de IA do **FUAG**! Agora qualquer novo movimento imaginado pode se transformar em controle gamer real.
