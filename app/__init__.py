import os
import pyotp
import smtplib
from .utils import *
from flask import Flask, jsonify
from .celery_config import make_celery
from email.mime.text import MIMEText
from .scrapping import *


app = Flask(__name__)


# Configuração do banco de dados do Render
url_render = "postgresql://meu_banco_vvlj_user:4CVqUxj8QyBpMzu4LD3CxDxgUXH1C8r7@dpg-cuaekdtds78s739mhjig-a.oregon-postgres.render.com/meu_banco_vvlj"
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
    
    
