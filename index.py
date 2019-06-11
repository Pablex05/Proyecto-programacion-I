from funciones import listar_eventos, evento_comentarios

# - *- coding: utf- 8 - *-

from flask import Flask

from flask import render_template #Permite importar templates

app = Flask(__name__) #Iniciar Flask


@app.route('/')
def index():
    listaeventos = listar_eventos()
    return render_template('eventos.html', listaeventos = listaeventos, usuario="iniciado")

@app.route('/nuevo_usuario')
def usuario_nuevo():

    return render_template('registro_de_nuevo_usuario.html') #Mostrar template y pasar variables

@app.route('/evento_publicado/<id>')
def evento(id):

    listaeventos = listar_eventos()

    evento = list(filter(lambda evento: evento['id'] == id, listaeventos))[0]
    listacomentarios = evento_comentarios()
    print(listacomentarios)
    return render_template('evento_con_comentario.html', listacomentarios=listacomentarios, evento=evento, nombreusuario="pablo",usuario="no_iniciado") #Mostrar template y pasar variables

@app.route('/nuevoevento')
def crear_evento():

    return render_template('crear_nuevo_evento.html' ) #Mostrar template y pasar variables

@app.route('/modificarevento')
def modificar_evento():

    return render_template('modificar_evento_creado')



if __name__ == '__main__': #Asegura que solo se ejectue el servidor cuando se ejecute el script directamente
    app.run(port = 8000, debug = True)


