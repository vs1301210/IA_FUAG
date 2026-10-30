r"""
=============================================================================
 IA_FUAG - Ferramenta de Captura Interativa de Gestos (Dataset Collector)
=============================================================================
Utilitário para coletar fotos de novos gestos diretamente da webcam para o dataset.

Uso no terminal:
  python capture_gestures.py --label meu_gesto --camera 0

Ou simplesmente execute sem parâmetros para modo interativo:
  python capture_gestures.py
=============================================================================
"""

import argparse
import os
import sys
import time

try:
    import cv2
except ImportError:
    print("\n[ERRO]: OpenCV não está instalado.")
    print("Instale com: pip install opencv-python\n")
    sys.exit(1)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Coletor de imagens para dataset de gestos manuais do FUAG.")
    parser.add_argument("--label", type=str, default="", help="Nome da classe/gesto (ex: acelerar, frear, none)")
    parser.add_argument("--camera", type=int, default=0, help="Índice da câmera (padrão: 0)")
    parser.add_argument("--delay", type=float, default=0.25, help="Intervalo em segundos para captura em rajada (padrão: 0.25s)")
    return parser.parse_args()


def main():
    args = parse_arguments()

    label = args.label.strip()
    if not label:
        print("=" * 60)
        print(" IA_FUAG - COLETOR DE DATASET DE GESTOS MANUAIS")
        print("=" * 60)
        print("Dica: Use 'none' para cadastrar a mão neutra/em repouso.")
        label = input("Digite o nome do gesto/classe a ser capturado: ").strip()

    if not label:
        print("[ERRO]: O nome do gesto não pode ser vazio.")
        sys.exit(1)

    # Diretório de destino
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "dataset", label)
    os.makedirs(output_dir, exist_ok=True)

    # Contagem de fotos existentes
    existing_files = [
        f for f in os.listdir(output_dir)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]
    counter = len(existing_files)

    print(f"\n[INFO] Salvando imagens em: {output_dir}")
    print(f"[INFO] Imagens já existentes nesta classe: {counter}")
    print("\nIniciando câmera...")

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        print(f"[ERRO]: Não foi possível acessar a câmera no índice {args.camera}.")
        print("Verifique se nenhuma outra aplicação está usando a câmera.")
        sys.exit(1)

    # Ajusta resolução se suportado
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    burst_mode = False
    last_burst_time = 0

    print("\nControles na janela da câmera:")
    print("  [ESPAÇO] : Capturar 1 foto manual")
    print("  [B]      : Ligar/Desligar modo rajada contínua (captura automática periódica)")
    print("  [Q/ESC]  : Sair e salvar")
    print("-" * 60)

    window_name = f"IA_FUAG - Capturando: {label}"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERRO]: Falha ao capturar quadro da câmera.")
            break

        # Espelhamento para visão natural do usuário
        display_frame = cv2.flip(frame, 1)
        clean_save_frame = display_frame.copy()

        current_time = time.time()

        # Captura automática no modo rajada
        if burst_mode and (current_time - last_burst_time >= args.delay):
            counter += 1
            filename = f"{label}_{counter:04d}_{int(current_time*1000)%100000}.jpg"
            filepath = os.path.join(output_dir, filename)
            cv2.imwrite(filepath, clean_save_frame)
            last_burst_time = current_time

        # Renderização do HUD na tela
        h, w, _ = display_frame.shape

        # Barra superior informativa
        cv2.rectangle(display_frame, (0, 0), (w, 50), (20, 20, 20), -1)
        mode_text = "MODO: RAJADA [B]" if burst_mode else "MODO: MANUAL [ESPACO]"
        mode_color = (0, 255, 0) if burst_mode else (255, 200, 0)
        cv2.putText(
            display_frame,
            f"Gesto: {label}  |  Fotos: {counter}  |  {mode_text}",
            (15, 32),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            mode_color,
            2,
            cv2.LINE_AA,
        )

        # Instruções na barra inferior
        cv2.rectangle(display_frame, (0, h - 35), (w, h), (20, 20, 20), -1)
        cv2.putText(
            display_frame,
            "[ESPACO]: Foto Unica | [B]: Alternar Rajada | [Q/ESC]: Sair | Mantenha a mao visivel!",
            (15, h - 12),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (220, 220, 220),
            1,
            cv2.LINE_AA,
        )

        cv2.imshow(window_name, display_frame)

        key = cv2.waitKey(1) & 0xFF
        if key in (27, ord("q"), ord("Q")):
            break
        elif key == 32:  # Barra de espaço
            counter += 1
            filename = f"{label}_{counter:04d}_{int(time.time()*1000)%100000}.jpg"
            filepath = os.path.join(output_dir, filename)
            cv2.imwrite(filepath, clean_save_frame)
            print(f"[OK] Foto salva: {filename} (Total: {counter})")
        elif key in (ord("b"), ord("B")):
            burst_mode = not burst_mode
            status = "ATIVADO" if burst_mode else "DESATIVADO"
            print(f"[INFO] Modo rajada {status}")
            last_burst_time = current_time

    cap.release()
    cv2.destroyAllWindows()

    print("\n" + "=" * 60)
    print(f" Captura concluída para a classe '{label}'!")
    print(f" Total de imagens salvas: {counter}")
    print(f" Diretório: {output_dir}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
