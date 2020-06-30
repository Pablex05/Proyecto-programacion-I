from flask import Flask
from flask_wtf import CSRFProtect	#es de la clave secreta
from flask_sqlalchemy import SQLAlchemy  #importar para base de datos
import os
from dotenv import load_dotenv #importa el archivo .env que contiene claves y configuraciones que otros no deberian tener acceso, pero si es vital para el sistema(entonces se lo coloca externamente)
from flask_mail import Mail, Message  # Importar para enviar Mail
from flask_login import LoginManager, current_user #importar para login

app = Flask(__name__)

load_dotenv(override=True)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + os.getenv('DB_USERNAME') + ':' + os.getenv('DB_PASS') + '@localhost/proyectoPaginaWeb'
db = SQLAlchemy(app)	#app = Flask(__name__)
app.config['MAIL_HOSTNAME'] = 'localhost'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SENDER'] = 'Eventin.com <Eventin@noreply.com>'
app.secret_key = 'esta_es_la_clave_secreta' #clave secreta

mail = Mail(app)
login_manager = LoginManager(app)
csrf = CSRFProtect(app)
app.secret_key = os.getenv('SECRET_KEY')

if __name__ == '__main__': # esto es para que inicie
    from rutas import *		#importamos las librerias que tienen los archivos rutas, api y errores
    from rutas_api import *
    from errores import *
    app.run(port=8000, debug=False)

