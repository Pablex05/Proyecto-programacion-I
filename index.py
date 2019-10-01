# - *- coding: utf- 8 - *-
from funciones import listar_eventos, evento_comentarios
from flask import Flask, render_template                                #Permite importar templates
from flask_wtf import CSRFProtect #importar para proteccion CSRF
from flask import flash #importar para mostrar mensajes flash
from flask import redirect, url_for
from formulario_registro import Registro #importar clase de formulario
from formulario_login import Login #importar clase de formulario
import datetime #importar funciones de fecha
from flask import request
from formulario_evento import Evento, Comentario
import os.path


app = Flask(__name__) #Iniciar Flask
csrf = CSRFProtect(app) #Iniciar protección CSRF
app.secret_key = 'esta_es_la_clave_secreta' #clave secreta

@app.route('/')
def index():
    formularioLogin = Login() #Instanciar formulario de Login
    listaeventos = listar_eventos()
    return render_template('pagina_principal.html', listaeventos = listaeventos, usuario="iniciado",formularioLogin = formularioLogin)
@app.route('/usuario/login', methods=["POST"])
def login():
    formularioLogin = Login() #Instanciar formulario de Login
    listaeventos = listar_eventos()
    if formularioLogin.validate_on_submit(): #Si el formulario ha sido enviado y es validado correctamente
        print(formularioLogin.email.data)
        print(formularioLogin.password.data)
        #Verifica que el usuario y pass sean correctos
        if formularioLogin.email.data == "admin@mail.com" and formularioLogin.password.data == "12345":
            flash('Login realizado correctamente','success') #Mostrar mensaje
            return redirect(url_for('index', formularioLogin=formularioLogin))  # Redirecciona a la página principal
        else:
            flash('Login incorrecto','danger') #Mostrar mensaje de error
            return redirect(url_for('index', formularioLogin = formularioLogin)) #Redirecciona a la página principal

    return render_template('pagina_principal.html', listaeventos=listaeventos, usuario="iniciado", formularioLogin = formularioLogin)

@app.route('/usuario/nuevoUsuario', methods=["GET", "POST"])
def usuario_nuevo():
    formulario = Registro()
    if formulario.validate_on_submit():
        flash('Login realizado correctamente', 'success')

    return render_template('registro_de_nuevo_usuario.html', formulario = formulario, usuario="iniciado")  # Mostrar template y pasar variables


@app.route('/usuario/eventoPublicado/<id>')
def evento(id):
    formularioLogin = Login()
    listaeventos = listar_eventos()
    evento = list(filter(lambda evento: evento['id'] == id, listaeventos))[0]
    listacomentarios = evento_comentarios()
    print(listacomentarios)
    return render_template('evento_con_comentario.html', listacomentarios=listacomentarios, evento=evento, nombreusuario="pablo",usuario="iniciado",formularioLogin = formularioLogin) #Mostrar template y pasar variables

@app.route('/usuario/nuevoEvento', methods=["GET", "POST"])
def crear_evento():
    formularioLogin = Login()
    formulario =Evento()
    if formulario.validate_on_submit():  # Si el formulario es validado correctamente
        flash('Usuario actualizado exitosamente', 'success')  # Mostrar mensaje
        mostrar_datos(formulario)  # Mostrar datos obtenido por consola
        return redirect(url_for('actualizar'))  # Redirecciona a la función actualizar
    return render_template('crear_nuevo_evento.html',nombreusuario="pablo",usuario="iniciado", formulario=formulario, destino="creando_evento", formularioLogin=formularioLogin) # Muestra el formulario

@app.route('/usuario/evento/modificarEvento', methods=["GET"])
def modificar_evento():
    formularioLogin = Login()
    formulario = Evento()
    formulario.titulo.data="hola"
    if formulario.validate_on_submit():  # Si el formulario es validado correctamente
        flash('Usuario actualizado exitosamente', 'success')  # Mostrar mensaje
        mostrar_datos(formulario)  # Mostrar datos obtenido por consola
        return redirect(url_for('modificar_evento'))  # Redirecciona a la función actualizar
    return render_template('crear_nuevo_evento.html', nombreusuario="pablo", usuario="iniciado", formulario=formulario, destino="modificar_evento", formularioLogin=formularioLogin)  # Muestra el formulario


@app.route('/usuario/evento/eliminarEvento', methods=["GET", "POST"])
def eliminar_evento():
    formularioLogin = Login()
    estado=1
    return render_template('panel_eventos_creados.html', listaeventos=listaeventos, estado=estado, nombreusuario="pablo",usuario="iniciado",formularioLogin = formularioLogin)
@app.route('/usuario/panelDeEventos', methods=["GET", "POST"])
def panel_eventos():
    formularioLogin = Login()
    listaeventos = listar_eventos()
    estado = 1
    return render_template('panel_eventos_creados.html', listaeventos=listaeventos, nombreusuario="pablo",usuario="iniciado",formularioLogin = formularioLogin, estado=estado)

@app.route('/usuario/evento/colocandoComentario',methods=["POST"])
def agregar_comentario():
    comentarioNuevo= Comentario.FormularioComentario()
    if comentarioNuevo.validate_on_submit():
        flash('¡Has comentado el evento con exito!')
        mostrar_datos(comentarioNuevo)
        return redirect(url_for('index',id=1))
    return render_template('evento_con_comentario.html',comentarionuevo=comentarioNuevo)


if __name__ == '__main__': #Asegura que solo se ejectue el servidor cuando se ejecute el script directamente
    app.run(port = 8800, debug = True)


