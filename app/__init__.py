import os
#import pyotp
import smtplib
import sqlite3
import random
from flask import Flask
from flask_login import login_user, logout_user
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Chave mestra para geração de códigos TOTP
chave_mestra = "K4XO47QRE75L4KTTPM775SOY4ESGSMIN"


# Defina o caminho para o arquivo do banco de dados SQLite
db_path = os.path.join(os.path.dirname(__file__), 'Data', 'Banco.db')

# Função para conectar ao banco de dados SQLite
def conectar_banco():
    conn = sqlite3.connect(db_path)
    return conn
# Função para gerar o código OTP
def gerar_codigo_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])


# Função para enviar email com o código OTP
def enviar_email_otp(destinatario, codigo):
    # Configuração do servidor SMTP
    email_enviador = 'seu_email@gmail.com'
    senha = 'sua_senha'
    servidor_smtp = 'smtp.gmail.com'
    porta = 587

    # Mensagem de email
    mensagem = f'Seu código de autenticação é: {codigo}'

    try:
        # Iniciar conexão SMTP
        server = smtplib.SMTP(servidor_smtp, porta)
        server.starttls()
        server.login(email_enviador, senha)

        # Enviar email
        server.sendmail(email_enviador, destinatario, mensagem)

        # Encerrar conexão SMTP
        server.quit()
        return codigo
    except Exception as e:
        print("Erro ao enviar email:", e)
        return None