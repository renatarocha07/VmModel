import socket
import os
import cv2
from detect import detect_objects
from uploader import upload_image

# Configurações do servidor TCP
HOST = "193.123.119.192"   # Escuta em todas interfaces
PORT = 1883
INPUT_DIR = r"C:\projeto_yolo\data\images_inputt"
OUTPUT_DIR = r"C:\projeto_yolo\data\images_outputt"

# Garante pastas
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def handle_connection(conn, addr, image_id):
    print(f" Conexão recebida de {addr}")

    input_file = os.path.join(INPUT_DIR, f"received_{image_id}.jpg")
    output_file = os.path.join(OUTPUT_DIR, f"received_{image_id}.jpg")

    try:
        # --- Reconstrução da imagem ---
        with open(input_file, "wb") as f:
            total_bytes = 0
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                f.write(data)
                total_bytes += len(data)

        print(f" Imagem salva em {input_file} ({total_bytes} bytes)")

        # --- Processamento YOLO ---
        img = cv2.imread(input_file)
        if img is None:
            print(f" Imagem ilegível: {input_file}")
            return

        try:
            main_class, precisao = detect_objects(input_file, output_file)
            print(f" Detecção concluída: classe={main_class}, confiança={precisao:.2f}")
        except Exception as e:
            print(f" Erro na detecção: {e}")
            return

        # --- Upload para Supabase ---
        try:
            upload_image(output_file, main_class, precisao)
        except Exception as e:
            print(f" Erro ao enviar para Supabase: {e}")

    except Exception as e:
        print(f" Erro durante o recebimento da imagem: {e}")


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f" Servidor ativo em {HOST}:{PORT}, aguardando imagens...")

        image_counter = 0
        while True:
            conn, addr = s.accept()
            with conn:
                handle_connection(conn, addr, image_counter)
                image_counter += 1


if __name__ == "__main__":
    start_server()
