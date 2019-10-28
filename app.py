from flask import Flask
from flask_sqlalchemy import SQLAlchemy #Incluye sqlAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#Configuración de conexion de base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Pablex_123456789@localhost/proyectoPaginaWeb'
#Instancia que representa la base de datos
db = SQLAlchemy(app)

#Instalar SQLAlchemy con:
#pip install Flask-SQLAlchemy
#Instalar controlador para MySQL
# pip install Flask-pymysql

if __name__ == '__main__': #Asegura que solo se ejectue el servidor cuando se ejecute el script directamente
    from rutas import *
    app.run(port = 8000, debug = True)
