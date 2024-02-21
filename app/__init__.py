from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for, request


app = Flask(__name__)
#app.config['SQLAlCHEMY_DATABASE_URI'] = ''

#login_manager = LoginManager(app)
#db = SQLAlchemy(app)
