import os
import psycopg2
from PIL import Image
from .extensions import db 


"""def conectar_banco():
    # Pegue as variáveis de ambiente configuradas no Render (como credenciais do banco de dados)
    db_url = "postgresql://meu_banco_4eqw_user:xRafujf8y9H0EESnPi73N6XIQUe0pyM6@dpg-cv2djsogph6c73bf7rog-a.oregon-postgres.render.com/meu_banco_4eqw"

    if db_url is None:
        raise Exception("DATABASE_URL não configurado.")

    # Conectar ao banco de dados usando a URL de conexão
    try:
        conn = psycopg2.connect(db_url)
        print("Conexão bem-sucedida ao banco de dados!")
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None"""

def conectar_banco():
    db_url = "postgresql://meu_banco_4eqw_user:xRafujf8y9H0EESnPi73N6XIQUe0pyM6@dpg-cv2djsogph6c73bf7rog-a.oregon-postgres.render.com/meu_banco_4eqw"
    
    try:
        conn = psycopg2.connect(db_url)
        print("✅ Conexão bem-sucedida ao banco de dados!")
        return conn
    except psycopg2.OperationalError as e:
        print(f"❌ Falha na conexão (OperationalError): {e}")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
    return None  # Explícito
    

# Função para configurar a pasta de upload
def configure_upload_folder(app, subfolder=None):
    """
    Configura a pasta de upload para o aplicativo.
    """
    upload_folder = 'Data'
    
    if subfolder:
        upload_folder = os.path.join(upload_folder, subfolder)
    
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    # Atualizar a configuração do aplicativo
    app.config['UPLOAD_FOLDER'] = upload_folder
    return upload_folder



def resize_and_crop(image, target_size=(800, 800)):

    image = image.convert("RGB")  # Converte para evitar erros de PNGs com transparência
    width, height = image.size

    # Redimensiona para 800px de largura mantendo a proporção
    new_width = 800
    new_height = int((new_width / width) * height)
    image = image.resize((new_width, new_height), Image.LANCZOS)

    # Recorta o centro para 800x800
    left = 0
    top = max(0, (new_height - 800) // 2)
    right = 800
    bottom = top + 800

    return image.crop((left, top, right, bottom))
