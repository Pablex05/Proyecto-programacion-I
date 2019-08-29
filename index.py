# - *- coding: utf- 8 - *-
from funciones import listar_eventos, evento_comentarios
from flask import Flask, render_template                                #Permite importar templates
from flask_wtf import CSRFProtect #importar para proteccion CSRF
from flask import flash #importar para mostrar mensajes flash
from flask import redirect, url_for
from formulario_registro import Registro #importar clase de formulario
from formulario_login import Login #importar clase de formulario
import datetime #importar funciones de fecha
from werkzeug.utils import secure_filename #Importa seguridad nombre de archivo
import os.path #importar para funciones de sistema

app = Flask(__name__) #Iniciar Flask
csrf = CSRFProtect(app) #Iniciar protección CSRF
app.secret_key = 'esta_es_la_clave_secreta' #clave secreta

@app.route('/')
def index():
    formularioLogin = Login() #Instanciar formulario de Login
    listaeventos = listar_eventos()
    return render_template('pagina_principal.html', listaeventos = listaeventos, usuario="iniciado",formularioLogin = formularioLogin)
@app.route('/login', methods=["POST"])
def login():
    formularioLogin = Login() #Instanciar formulario de Login
    if formularioLogin.validate_on_submit(): #Si el formulario ha sido enviado y es validado correctamente
        print(formularioLogin.email.data)
        print(formularioLogin.password.data)
        #Verifica que el usuario y pass sean correctos
        if formularioLogin.email.data == "admin@mail.com" and formularioLogin.password.data == "12345":
            flash('Login realizado correctamente','success') #Mostrar mensaje
        else:
            flash('Login incorrecto','danger') #Mostrar mensaje de error
        return redirect(url_for('index')) #Redirecciona a la página principal
    listaeventos = listar_eventos()
    return render_template('pagina_principal.html', listaeventos=listaeventos, usuario="iniciado", formularioLogin = formularioLogin)

@app.route('/nuevo_usuario', methods=["GET", "POST"])
def usuario_nuevo():
    formulario = Registro()
    if formulario.validate_on_submit():
        flash('Login realizado correctamente', 'success')

    return render_template('registro_de_nuevo_usuario.html', formulario = formulario, usuario="iniciado")  # Mostrar template y pasar variables


@app.route('/evento_publicado/<id>')
def evento(id):
    formularioLogin = Login()
    listaeventos = listar_eventos()
    evento = list(filter(lambda evento: evento['id'] == id, listaeventos))[0]
    listacomentarios = evento_comentarios()
    print(listacomentarios)
    return render_template('evento_con_comentario.html', listacomentarios=listacomentarios, evento=evento, nombreusuario="pablo",usuario="iniciado",formularioLogin = formularioLogin) #Mostrar template y pasar variables

@app.route('/nuevo_evento', methods=["GET", "POST"])
def crear_evento():
    formularioLogin = Login()
    class Persona:
        nombre_usuario = 'nombre usuario'
        email = 'Email@email.com'
        fechaNac = datetime.datetime.strptime('2019-05-16', "%Y-%m-%d").date()
        hora = datetime.datetime.strptime('11:25 PM', "%I:%M %p").time()

    formulario = Registro(obj=Persona)
    Registro.opcional(formulario.password)
    if formulario.validate_on_submit():  # Si el formulario es validado correctamente
        flash('Usuario actualizado exitosamente', 'success')  # Mostrar mensaje
        mostrar_datos(formulario)  # Mostrar datos obtenido por consola
        return redirect(url_for('actualizar'))  # Redirecciona a la función actualizar
    return render_template('crear_nuevo_evento.html',nombreusuario="pablo",usuario="iniciado", formulario=formulario, destino="actualizar", formularioLogin=formularioLogin) # Muestra el formulario

@app.route('/panel_configuracion', methods=["GET", "POST"])
def panel_eventos():
    formularioLogin = Login()
    listaeventos = listar_eventos()
    return render_template('panel_eventos_creados.html', listaeventos=listaeventos, nombreusuario="pablo",usuario="iniciado",formularioLogin = formularioLogin)



if __name__ == '__main__': #Asegura que solo se ejectue el servidor cuando se ejecute el script directamente
    app.run(port = 8000, debug = True)


