import os
#import pyotp
import smtplib
from flask import Flask
from flask_login import LoginManager
from email.mime.text import MIMEText
from flask_sqlalchemy import SQLAlchemy
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Data/banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



# Defina o caminho para o arquivo do banco de dados SQLite
db_path = 'Data/banco.db'

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

    try:
        # Iniciar conexão SMTP
        server = smtplib.SMTP(servidor_smtp, porta)
        server.starttls()
        server.login(email_enviador, senha)

        # Enviar email
        server.send_message(msg)

        # Encerrar conexão SMTP
        server.quit()
        return True
    except Exception as e:
        print("Erro ao enviar email:", e)
        return False


