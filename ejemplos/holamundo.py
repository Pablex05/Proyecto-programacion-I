from flask import Flask
# -*- coding: utf-8 *-*
app = Flask(__name__)

@app.route('/')
def index():
    return "hola mundo"
"""@app.route('/saludar/<nombre>')
def saludar (nombre):
    return "hola" +nombre
@app.route('/saludar2/<nombre>/<int:edad>') #funcion individual de la funcion 
def saludar2(nombre,edad):
    return "mi nombre es " + nombre + "y tengo " + str(edad) + " anios"
"""
@app.route('/saludar/<nombre>/<int:edad>')   #funcion convinando el nombre y la edad      
@app.route('/saludar/<nombre>')
def saludar(nombre,edad=""):
    return "mi nombre es " + nombre + "y tengo " + str(edad) + " anios"




app.run()
