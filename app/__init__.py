import os
import pyotp
import smtplib
from random import randint
from flask_login import LoginManager
from email.mime.text import MIMEText
from flask_sqlalchemy import SQLAlchemy
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)



# Chave mestra para geração de códigos TOTP
chave_mestra = "K4XO47QRE75L4KTTPM775SOY4ESGSMIN"

# Função para enviar email
def enviar_email(destinatario, assunto, mensagem):
    # Configuração do servidor SMTP
    email_enviador = 'seu_email@gmail.com'
    senha = 'sua_senha'
    servidor_smtp = 'smtp.gmail.com'
    porta = 587

    # Criar objeto MIMEText para o conteúdo do email
    msg = MIMEMultipart()
    msg['From'] = email_enviador
    msg['To'] = destinatario
    msg['Subject'] = assunto
    msg.attach(MIMEText(mensagem, 'plain'))

    # Iniciar conexão SMTP
    server = smtplib.SMTP(servidor_smtp, porta)
    server.starttls()
    server.login(email_enviador, senha)

    # Enviar email
    server.send_message(msg)

    # Encerrar conexão SMTP
    server.quit()


# Defina o caminho para o arquivo do banco de dados SQLite
db_path = 'Data/banco.db'

# Verifique se o arquivo do banco de dados existe
if not os.path.exists(db_path):
    # Se não existir, crie-o
    open(db_path, 'w').close()

# Configuração do SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização do SQLAlchemy
login_manager = LoginManager(app)
db = SQLAlchemy(app)