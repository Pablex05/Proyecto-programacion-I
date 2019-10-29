# - *- coding: utf- 8 - *-
from funciones import comentarios, eventos, crear_evento, crear_usuario, crear_comentario
from flask import Flask, render_template                                #Permite importar templates
from flask_wtf import CSRFProtect #importar para proteccion CSRF
from flask import flash #importar para mostrar mensajes flash
from formulario_registro import Registro #importar clase de formulario
from formulario_login import Login, validarCuenta #importar clase de formulario
import datetime #importar funciones de fecha
from formulario_evento import Evento_form, Comentario_form
from app import db
from modelos import Evento,Usuario,Comentario
import os.path
from mail import enviarMail, mailRegistro
from app import *
from flask import redirect, url_for, request
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, \
    SubmitField, BooleanField
from wtforms.fields.html5 import EmailField, DateField
from wtforms import validators
from wtforms_components import TimeField, DateRange
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_login import login_required, login_user, logout_user, current_user, LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) #Iniciar Flask
csrf = CSRFProtect(app) #Iniciar protección CSRF
app.secret_key = 'esta_es_la_clave_secreta' #clave secreta
db = SQLAlchemy()
login_manager = LoginManager()

@app.route('/')
def index():
    formularioLogin = Login() #Instanciar formulario de Login
    listaeventos = eventos()
    return render_template('pagina_principal.html', listaeventos = listaeventos, usuario="no_iniciado",formularioLogin = formularioLogin)
@app.route('/usuario/login', methods=["POST"])
def login():
    formularioLogin = Login()
    listaeventos = eventos()
    if formularioLogin.validate_on_submit():
        # Obterner usuario por email
        usuario = Usuario.query.filter_by(email=formularioLogin.email.data).first()
        # Si el usuario existe y se verifica la pass
        if usuario is not None and usuario.verificar_pass(formularioLogin.password.data):
            # Loguear usuario
            login_user(usuario, formularioLogin.remember_me.data)
        else:
            # Mostrar error de autenticación
            flash('Email o pass incorrectas.', 'success')
    return render_template('pagina_principal.html', formularioLogin=formularioLogin, listaeventos = listaeventos, usuario="iniciado")

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('Debe iniciar sesión para continuar.', 'warning')
    return redirect(url_for('login'))

def has_permission(user, evento):
    aux = False
    if user.is_authenticated:
        if user.is_admin() or user.is_owner(evento):
            aux = True
    return aux

@app.route('/usuario/nuevoUsuario', methods=["GET", "POST"])
def usuario_nuevo():
    formulario_usuario = Registro()

    if validarCuenta(formulario_usuario.email.data):
        if formulario_usuario.validate_on_submit():
            flash('Registro realizado correctamente', 'success')
            usuario = Usuario(nombre=formulario_usuario.nombre.data, apellido=formulario_usuario.apellido.data,
                              email=formulario_usuario.email.data, password=formulario_usuario.password.data)
            db.session.add(usuario)
            db.session.commit()
            enviarMail(formulario_usuario.email.data, 'Gracias por registrarte y Bienvenido a Eventin.com! :) ', formulario=formulario_usuario)
            return redirect(url_for('index'))
        else:
            flash('La cuenta ya se encuentra REGISTRADA, por favor Registre una cuenta diferente')
    return render_template('registro_de_nuevo_usuario.html', formulario = formulario_usuario, usuario="iniciado")  # Mostrar template y pasar variables


@app.route('/usuario/eventoPublicado/<id>' , methods=["GET"])
def evento(id):
    formularioLogin = Login()
    evento = db.session.query(Evento).get(id)
    if evento.aprobado == 1 or has_permission(current_user, evento):
        formulario = Comentario_form()
        titulo = "Evento - " + evento.nombre
        lista_comentarios = comentarios(id)
        if formulario.is_submitted():
            if formulario.validate_on_submit():
                flash('Comentario añadido!', 'success')
                formulario.mostrar_datos()

                comentario = Comentario(contenido=formulario.contenido.data, usuarioId=current_user.usuarioId, eventoId=id)
                db.session.add(comentario)
                db.session.commit()

                return redirect(url_for('evento', id=id))
            else:
                flash('Comentario no añadido. Reintente', 'danger')
                return redirect(url_for('evento', id=id, evento=evento, titulo=titulo, formulario=formulario, lista_comentarios=lista_comentarios))
    return render_template('evento_con_comentario.html', evento=evento, nombreusuario="pablo",usuario="iniciado",formularioLogin = formularioLogin) #Mostrar template y pasar variables

@app.route('/usuario/nuevoEvento', methods=["GET","POST"])
def crear_evento():
    formularioLogin = Login()
    formulario = Evento_form()
    if formulario.validate_on_submit():  # Si el formulario es validado correctamente
        flash('evento creado exitosamente', 'success')  # Mostrar mensaje
        f = formulario.imagen.data
        filename = secure_filename(f.filename)
        f.save(os.path.join('static/imagenes', filename))
        evento = Evento(nombre = formulario.titulo.data, fecha = formulario.fecha.data, hora = formulario.hora.data, lugar = formulario.lugar.data,descripcion = formulario.descripcion.data, imagen = "imagen2.png", usuarioId = 201)
        db.session.add(evento)
        db.session.commit()
    return render_template('crear_nuevo_evento.html',nombreusuario="pablo",usuario="iniciado",formulario=formulario, destino="creando_evento", formularioLogin=formularioLogin) # Muestra el formulario

@app.route('/usuario/evento/modificarEvento/<id>', methods=["GET"])
def modificar_evento(id):

    formularioLogin = Login()
    formulario = Evento_form()
    evento = db.session.query(Evento).get(id)
    formulario.titulo.data = evento.nombre
    formulario.fecha.data = evento.fecha
    formulario.hora.data = evento.hora
    formulario.lugar.data = evento.lugar
    formulario.descripcion.data = evento.descripcion
    if formulario.validate_on_submit():  # Si el formulario es validado correctamente
        flash('Evento actualizado exitosamente', 'success')  # Mostrar mensaje
        return redirect(url_for('panel_eventos'))  # Redirecciona a la función actualizar
    return render_template('crear_nuevo_evento.html', nombreusuario="pablo", usuario="iniciado", formulario=formulario, destino="modificar_evento", formularioLogin=formularioLogin)  # Muestra el formulario


@app.route('/usuario/evento/eliminarEvento/<id>', methods=["GET", "POST"])
def eliminar_evento(id):
    evento = db.session.query(Evento).get(id)
    db.session.delete(evento)
    db.session.commit()
    return redirect(url_for('panel_eventos'))

@app.route('/eliminarComentarioById/<id>')
@login_required
def eliminarComentarioById(id):
    comentario = db.session.query(Evento).get(id)

    if current_user.is_admin() or current_user.is_owner(comentario) or current_user.is_owner(comentario.evento):
        db.session.delete(comentario)
        db.session.commit()
        flash('Comentario Eliminado!', 'success')
        return redirect(url_for('evento', id=comentario.eventoId))
    else:
        flash('NO PUEDE BORRAR ESTE COMENTARIO!', 'warning')
        return redirect(url_for('index'))

@app.route('/usuario/evento/SolicitudAprobacion/<id>/<estado>', methods=["GET", "POST"])
def aprobar_evento(id,estado):
    formularioLogin = Login()
    formulario = Evento_form()
    evento = db.session.query(Evento).get(id)
    evento.estado = estado
    db.session.add(evento)
    db.session.commit()
    return redirect(url_for('panel_eventos'))

@app.route('/usuario/panelDeEventos', methods=["GET", "POST"])
def panel_eventos():
    formularioLogin = Login()
    listaeventos = eventos()
    return render_template('panel_eventos_creados.html', listaeventos=listaeventos, nombreusuario="pablo",usuario="iniciado",formularioLogin = formularioLogin)

@app.route('/usuario/evento/colocandoComentario/<id>',methods=["GET"])
def agregar_comentario():
    comentario = Comentario_form
    if comentario.validate_on_submit():
        flash('el comentario se a registrado')
        comentario = Comentario(texto=comentario.texto.data, fecha=comentario.fecha.data, hora=comentario.hora.data, usuarioId=201)
        db.session.add(comentario)
        db.session.commit()
        return redirect(url_for('evento', id=id))
    return redirect(url_for('evento'))
