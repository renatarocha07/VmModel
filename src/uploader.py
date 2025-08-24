import os
from datetime import datetime
from supabase import create_client
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = "Image_detect"

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL e SUPABASE_KEY devem estar definidos no .env")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_image(file_path, main_class, precisao):
    """
    Envia a imagem para Supabase Storage e insere os dados na tabela alertas_imagem
    """
    file_name = os.path.basename(file_path)

    try:
        # Upload da imagem
        with open(file_path, "rb") as f:
            supabase.storage.from_(BUCKET_NAME).upload(file_name, f)
        print(f"✅ {file_name} enviado para Storage com sucesso!")
    except Exception as e:
        print(f" Falha no upload de {file_name}: {e}")
        return

    # Define alarme_ativado
    alarme_ativado = precisao >= 0.75 if precisao is not None else False

    # Trata imagens sem detecção
    if main_class is None:
        main_class = "None"
        precisao = 0.0

    # Insere dados na tabela
    data = {
        "classe": main_class,
        "alarme_ativado": alarme_ativado,
        "data_hora": datetime.now().isoformat(),
        "precisao": precisao,
        "arquivo": file_name,
        "processado": True
    }

    try:
        supabase.table("alertas_imagem").insert(data).execute()
        print(f"✅ Dados de {file_name} inseridos com sucesso!")
    except Exception as e:
        print(f" Falha ao inserir dados de {file_name}: {e}")
