import os
import pyotp
import smtplib
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from email.mime.text import MIMEText
from .celery_config import make_celery  # Importe a função make_celery do celery.py
from .extensions import db

def create_app():
    # Caminho absoluto para as pastas templates e static
    base_dir = os.path.abspath(os.path.dirname(__file__))  # Diretório atual (app/)
    templates_path = os.path.join(base_dir, '..', 'templates')  # Volta uma pasta e entra em templates/
    static_path = os.path.join(base_dir, '..', 'static')  # Volta uma pasta e entra em static/

    # Criar a instância do Flask com os caminhos personalizados
    app = Flask(__name__, template_folder=templates_path, static_folder=static_path)

    app.config['SQLALCHEMY_DATABASE_URI'] = ('postgresql://hora_de_comer_user:Je7JHMeWD6GC8TVCHOKUlEhd3FDEXLOO@dpg-d0u52fm3jp1c73feg3e0-a.oregon-postgres.render.com/hora_de_comer' )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configuração do Celery
    app.config.update(
        CELERY_BROKER_URL='redis://localhost:6379/0', 
        CELERY_RESULT_BACKEND='redis://localhost:6379/0'
    )

    # Inicializar SQLAlchemy
    db.init_app(app)

    # Inicializar Celery
    celery = make_celery(app)

    # Criar as tabelas, se necessário
    with app.app_context():
        db.create_all()

    # Rota para iniciar o scraping em segundo plano
    @app.route('/start_scraping')
    def start_scraping():
        async_scraping.delay('sp/campinas')
        return jsonify({'message': 'Scraping started in background.'}), 200

    # Tarefa assíncrona para scraping
    @celery.task
    def async_scraping(location):
        # Implementação da tarefa de scraping
        # Exemplo: scraping(location)
        pass

    return app


# Função para gerar o código OTP
def gerar_codigo_otp():
    chave_mestra = "K4XO47QRE75L4KTTPM775SOY4ESGSMIN"
    totp = pyotp.TOTP(chave_mestra)
    codigo = totp.now()
    return codigo

# Função para enviar o código OTP por e-mail
def enviar_email_otp(destinatario, codigo):
    # Configuração do servidor SMTP
    email_enviador = 'raffasadol@gmail.com'
    senha = 'szhumutctbvxdjux'
    servidor_smtp = 'smtp.gmail.com'
    porta = 587

    # Mensagem de e-mail
    mensagem = MIMEText(f'Seu código de autenticação é: {codigo}')
    mensagem['From'] = email_enviador
    mensagem['To'] = destinatario
    mensagem['Subject'] = 'Use o código de autenticação para redefinir sua senha'

    try:
        # Iniciar conexão SMTP
        server = smtplib.SMTP(servidor_smtp, porta)
        server.starttls()
        server.login(email_enviador, senha)

        # Enviar e-mail
        server.sendmail(email_enviador, destinatario, mensagem.as_string())

        # Encerrar conexão SMTP
        server.quit()
        return codigo
    except Exception as e:
        print("Erro ao enviar e-mail:", e)
        return None


