import os
from flask import Flask

# Configuração do banco de dados e do Flask
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
# Exemplo alternativo: "postgresql://user:password@host:port/dbname"

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

# Configurar a pasta de upload principal no início
configure_upload_folder(app)

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
