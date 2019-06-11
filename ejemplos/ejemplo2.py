
from flask import Flask
from flask import render_template #permite mostrar templates

# -*- coding: utf-8 *-*
app = Flask(__name__)

@app.route('/')
def index():
    lista=["elemento A", "elemento B", "elemento C"]
    titulo="Titulo pagina"
    return render_template('registro_de_nuevo_usuario.html',titulo=titulo, texto="esto es un texto", lista=lista)

app.run()
