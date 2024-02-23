import os
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

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