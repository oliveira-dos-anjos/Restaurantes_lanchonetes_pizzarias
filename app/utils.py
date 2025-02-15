import os
import psycopg2
from .extensions import db  # Importe o db de extensions.py


def conectar_banco():
    # Pegue as variáveis de ambiente configuradas no Render (como credenciais do banco de dados)
    db_url = "postgresql://meu_banco_92dn_user:smC07EuSDkTeQFzALUAh1pkn3ncImAez@dpg-cultktbtq21c73b3fje0-a.oregon-postgres.render.com/meu_banco_92dn"

    if db_url is None:
        raise Exception("DATABASE_URL não configurado.")

    # Conectar ao banco de dados usando a URL de conexão
    try:
        conn = psycopg2.connect(db_url)
        print("Conexão bem-sucedida ao banco de dados!")
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
    

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

# Função para salvar arquivos enviados
def save_uploaded_file(app, image_data, filename, subfolder=None):
    """
    Salva um arquivo enviado pelo usuário na pasta configurada.
    """
    # Configurar a pasta de upload específica, se necessário
    upload_folder = configure_upload_folder(app, subfolder)
    
    # Construir o caminho completo para salvar o arquivo
    save_path = os.path.join(upload_folder, filename)
    
    # Salvar o arquivo no caminho especificado
    image_data.save(save_path)
    
    return save_path