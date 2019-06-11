from flask import Flask
# -*- coding: utf-8 *-*
app = Flask(__name__)
"""
#ejemplo1
#1- Si la url contiene un nombre entonces mostra por pantalla  Hola Nombre!, si no mostrar Hola Usuario

@app.route('/<nombre>')
@app.route('/')
def ej1 (nombre='estandar'):
    if nombre is 'estandar':
        return "Hola Usuario"
    else:
        return "Hola "+nombre
app.run()
"""
"""
#ejemplo2
#2- Mostrar el mensaje Hola tantas veces como el numero ingresado en la url

@app.route('/ejercicio2/<int:edad>')
@app.route('/')
def ej2 (edad=""):
    cadena = ""
    for x in range(edad):
         cadena+="Hola "
    return cadena
app.run()
"""
#ejemplo 3
#3- A partir de la siguiente lista:
#
#productos = [['Producto A', 1.68],['Producto B', 5.32],['Producto C', 8.3]]
#
#Ingresar un nuevo producto por url que contenga un nombre y un precio en formato float
#
#Agregar el producto al principio de la lista
#
#Mostrar la lista de productos

@app.route('/ejercicio3/<producto>/<float:precio>')

def ej3 (producto, precio):
    productos = [[' Producto A', 1.68],[' Producto B', 5.32],[' Producto C', 8.3]]
    print("ingrese el producto:")
    prod = [producto, precio]
    productos.insert(0,prod)
    cadena = ""
    for x in productos:
        cadena += x[0] + str(x[1])
    return cadena
app.run()






