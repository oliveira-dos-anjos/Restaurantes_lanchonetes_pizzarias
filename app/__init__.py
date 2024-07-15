import os
import pyotp
import smtplib
from flask import Flask, jsonify
from .celery_config import make_celery
from email.mime.text import MIMEText
from .scrapping import *


app = Flask(__name__)


# Configuração do banco de dados do Render
url_render = "postgresql://locais_na_regiao_user:Kt7jO2Gp0AItHphEktRs4Xs16cXB8W9F@dpg-cq09p8aju9rs73aqcqvg-a.oregon-postgres.render.com/locais_na_regiao"
app.config['SQLALCHEMY_DATABASE_URI'] = url_render

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0', 
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'
)

celery = make_celery(app)

@celery.task
def async_scraping(location):
    # Implementação da tarefa de scraping
    # Exemplo: scraping(location)
    pass

@app.route('/start_scraping')
def start_scraping():
    async_scraping.delay('sp/campinas')
    return jsonify({'message': 'Scraping started in background.'}), 200

# Função para gerar o código OTP
def gerar_codigo_otp():

    chave_mestra = "K4XO47QRE75L4KTTPM775SOY4ESGSMIN"
    
    totp = pyotp.TOTP(chave_mestra)
    codigo = totp.now()
    return codigo

#Funçao para enviar o codigo otp para o email cadastrado
def enviar_email_otp(destinatario, codigo):
    # Configuração do servidor SMTP
    email_enviador = 'raffasadol@gmail.com'
    senha = 'szhumutctbvxdjux'
    servidor_smtp = 'smtp.gmail.com'
    porta = 587

    # Mensagem de email
    mensagem = MIMEText(f'Seu código de autenticação é: {codigo}')
    mensagem['From'] = email_enviador
    mensagem['To'] = destinatario
    mensagem['Subject'] = 'Use o código de autenticação para redefinir sua senha'

    try:
        # Iniciar conexão SMTP
        server = smtplib.SMTP(servidor_smtp, porta)
        server.starttls()
        server.login(email_enviador, senha)

        # Enviar email
        server.sendmail(email_enviador, destinatario, mensagem.as_string())

        # Encerrar conexão SMTP
        server.quit()
        return codigo
    except Exception as e:
        print("Erro ao enviar email:", e)
        return None
    
    
# Função de configuração da pasta de upload
def configure_upload_folder(app):
    UPLOAD_FOLDER = os.path.join(app.root_path, 'static/imagens_lojas')
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)  # Criar o diretório se não existir
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER