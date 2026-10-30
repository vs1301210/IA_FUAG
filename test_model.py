r"""
=============================================================================
 IA_FUAG - Testador de Modelo em Tempo Real (Live Gesture Tester)
=============================================================================
Permite testar o arquivo compilado 'gesture_recognizer.task' diretamente
pela webcam antes de integrá-lo no FUAG.

Uso no terminal:
  python test_model.py
=============================================================================
"""

import os
import sys
import time

try:
    import cv2
    import mediapipe as mp
    from mediapipe.tasks import python
    from mediapipe.tasks.python import vision
except ImportError:
    print("\n[ERRO]: Dependências não encontradas. Certifique-se de ativar a venv:")
    print(r"  .\venv\Scripts\Activate.ps1")
    print("  pip install -r requirements.txt\n")
    sys.exit(1)


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "exported_models", "gesture_recognizer.task")

    if not os.path.exists(model_path):
        print("=" * 60)
        print("[ERRO]: Modelo não encontrado!")
        print(f"Caminho esperado: {model_path}")
        print("Execute o script de treinamento primeiro: python train_model.py")
        print("=" * 60)
        return

    print("=" * 60)
    print(" IA_FUAG - TESTADOR EM TEMPO REAL DE GESTOS")
    print("=" * 60)
    print(f"Carregando modelo: {model_path}")

    # Configura o reconhecedor do MediaPipe
    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.GestureRecognizerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.LIVE_STREAM,
        num_hands=2,
        min_hand_detection_confidence=0.5,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5,
        result_callback=print_result_callback,
    )

    global latest_result
    latest_result = None

    def result_callback(result: vision.GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
        global latest_result
        latest_result = result

    options.result_callback = result_callback

    recognizer = vision.GestureRecognizer.create_from_options(options)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERRO]: Falha ao acessar a câmera.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    print("\nIniciando câmera. Pressione [Q] ou [ESC] para sair.\n")
    window_name = "IA_FUAG - Testador de Gestos (Live)"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        timestamp_ms = int((time.time() - start_time) * 1000)
        recognizer.recognize_async(mp_image, timestamp_ms)

        h, w, _ = frame.shape

        # Renderiza os resultados recebidos
        detected_text = "Nenhum gesto detectado"
        confidence_text = ""
        box_color = (60, 60, 60)

        if latest_result and latest_result.gestures:
            top_gesture = latest_result.gestures[0][0]
            label = top_gesture.category_name
            score = top_gesture.score

            if label and label != "None":
                detected_text = f"Gesto: {label.upper()}"
                confidence_text = f"Confianca: {score * 100:.1f}%"
                box_color = (0, 160, 0)
            else:
                detected_text = "Gesto: NEUTRO / NONE"
                confidence_text = f"Confianca: {score * 100:.1f}%"
                box_color = (120, 120, 0)

        # Barra HUD
        cv2.rectangle(frame, (0, 0), (w, 60), box_color, -1)
        cv2.putText(
            frame,
            detected_text,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

        if confidence_text:
            cv2.putText(
                frame,
                confidence_text,
                (w - 300, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )

        cv2.rectangle(frame, (0, h - 30), (w, h), (20, 20, 20), -1)
        cv2.putText(
            frame,
            "Pressione [Q] ou [ESC] para sair",
            (15, h - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (200, 200, 200),
            1,
            cv2.LINE_AA,
        )

        cv2.imshow(window_name, frame)

        key = cv2.waitKey(1) & 0xFF
        if key in (27, ord("q"), ord("Q")):
            break

    cap.release()
    cv2.destroyAllWindows()
    recognizer.close()
    print("[INFO] Teste finalizado com sucesso.")


def print_result_callback(result, output_image, timestamp_ms):
    pass


if __name__ == "__main__":
    main()
