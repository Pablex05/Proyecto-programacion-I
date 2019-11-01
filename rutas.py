# - *- coding: utf- 8 - *-
from flask_login import login_user, logout_user, login_required, current_user
from wtforms import ValidationError

from funciones import comentarios, eventos, crear_evento, crear_usuario, crear_comentario
from flask import Flask, render_template, app  # Permite importar templates
from flask_wtf import CSRFProtect #importar para proteccion CSRF
from flask import flash #importar para mostrar mensajes flash
from flask import redirect, url_for
from formulario_registro import Registro #importar clase de formulario
from formulario_login import Login #importar clase de formulario
import datetime #importar funciones de fecha
from flask import request
from formulario_evento import Evento_form, Comentario_form
from app import db, app, login_manager
from funciones_mail import *
from modelos import Evento,Usuario,Comentario
from werkzeug.utils import secure_filename #Importa seguridad nombre de archivo
import os.path


@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('Debe iniciar sesión para continuar.', 'warning')
    return redirect(url_for('ingresar'))


def has_permission(user, evento):
    aux = False
    if user.is_authenticated:
        if user.is_admin() or user.is_owner(evento):
            aux = True
    return aux

@app.route('/',  methods=["POST", "GET"])
def index():
    formularioLogin = Login() #Instanciar formulario de Login
    listaeventos = eventos()
    return render_template('pagina_principal.html', listaeventos = listaeventos, formularioLogin = formularioLogin)
@app.route('/usuario/login', methods=["POST"])
def login():
    formularioLogin = Login()
    if formularioLogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formularioLogin.email.data).first()
        #Si el usuario existe y se verifica la pass
        if usuario is not None and usuario.verificar_pass(formularioLogin.password.data):
        #Loguear usuario
            login_user(usuario, formularioLogin.remember_me.data)
        else:
            #Mostrar error de autenticación
            flash('Email o pass incorrectas.','success')
    return redirect(url_for('index', formularioLogin = formularioLogin))

@app.route('/logout')
#Limitar el acceso a los usuarios registrados
@login_required
def logout():
    logout_user()
    #Insntanciar formulario de Login
    formularioLogin = Login()
    return render_template('pagina_principal.html', formularioLogin=formularioLogin)
"""
@app.route('/confirmar/<token>')
#Limitar el acceso a los usuarios registrados
@login_required
def confirmar(token):
    if current_user.confirmado:
        return redirect(url_for('index'))
    if current_user.confirmar(token):
        flash('La cuenta ha sido confirmada','success')
    else:
        flash('La cuenta no pudo ser confirmada.','danger')
        return redirect(url_for('index'))
    return redirect(url_for('usuario'))
"""
@app.route('/usuario/nuevoUsuario', methods=["GET","POST"])
def usuario_nuevo():
    form = FormularioMail()
    formularioLogin = Login()
    formulario_usuario = Registro()
    x = 0
    if formulario_usuario.validate_on_submit() and validarExistente(formulario_usuario.email.data):
        flash('Registro realizado correctamente', 'success')
        if form.validate_on_submit():
            mail = form.mail.data
            flash('Se ha enviado un mail de confirmación.', 'success')
            enviarMailThread(mail)
        usuario = Usuario(nombre=formulario_usuario.nombre.data, apellido=formulario_usuario.apellido.data, email=formulario_usuario.email.data, password=formulario_usuario.password.data)
        db.session.add(usuario)
        db.session.commit()
        login_user(usuario, True)
        return redirect(url_for('index', form=form))
    else:
         flash('Este usuario ya se a registrado', 'danger')
    return render_template('registro_de_nuevo_usuario.html', formulario=formulario_usuario,formularioLogin=formularioLogin)  # Mostrar template y pasar variables


@app.route('/usuario/eventoPublicado/<id>' , methods=["GET"])
def evento(id):
    formularioLogin = Login()
    evento = db.session.query(Evento).get(id)
    return render_template('evento_con_comentario.html', evento=evento, nombreusuario="pablo",usuario="iniciado",formularioLogin = formularioLogin) #Mostrar template y pasar variables

@app.route('/usuario/nuevoEvento', methods=["GET","POST"])
@login_required
def crear_evento():
    formularioLogin = Login()
    formulario = Evento_form()
    if formulario.validate_on_submit():  # Si el formulario es validado correctamente
        flash('evento creado exitosamente, pero tiene que algun administrador apruebe el evento', 'success')  # Mostrar mensaje
        f = formulario.imagen.data
        filename = secure_filename(f.filename)
        f.save(os.path.join('static/imagenes', filename))
        evento = Evento(nombre = formulario.titulo.data, fecha = formulario.fecha.data, hora = formulario.hora.data, lugar = formulario.lugar.data,descripcion = formulario.descripcion.data, imagen = filename, usuarioId = 1)
        db.session.add(evento)
        db.session.commit()
    return render_template('crear_nuevo_evento.html',nombreusuario="pablo",formulario=formulario, destino="creando_evento", formularioLogin=formularioLogin) # Muestra el formulario

@app.route('/usuario/evento/modificarEvento/<id>', methods=["GET","POST"])
@login_required
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
    return render_template('crear_nuevo_evento.html', nombreusuario="pablo",  formulario=formulario, destino="modificar_evento", formularioLogin=formularioLogin)  # Muestra el formulario


@app.route('/usuario/evento/eliminarEvento/<id>', methods=["GET", "POST"])
@login_required
def eliminar_evento(id):
    evento = db.session.query(Evento).get(id)
    db.session.delete(evento)
    db.session.commit()
    return redirect(url_for('panel_eventos'))

@app.route('/usuario/evento/SolicitudAprobacion/<id>/<estado>', methods=["GET", "POST"])
@login_required
def aprobar_evento(id,estado):
    formularioLogin = Login()
    formulario = Evento_form()
    if current_user.is_admin():
        evento = db.session.query(Evento).get(id)
        evento.estado = estado
        db.session.add(evento)
        db.session.commit()
        return redirect(url_for('panel_eventos'))
    else:
        flash('Usted no es un administrador para entrar a este servicio', 'danger')
        return redirect(url_for('index'))



@app.route('/usuario/panelDeEventos', methods=["GET", "POST"])
@login_required
def panel_eventos():
    formularioLogin = Login()
    listaeventos = eventos()
    if current_user.is_admin():
        return render_template('panel_eventos_creados.html', listaeventos=listaeventos, nombreusuario="pablo",formularioLogin = formularioLogin)
    else:
        flash('Usted no es un administrador para entrar a este servicio', 'danger')
        return redirect(url_for('index'))

@app.route('/usuario/evento/colocandoComentario',methods=["POST"])
@login_required
def agregar_comentario():
    comentarioNuevo = Comentario_form()
    if comentarioNuevo.validate_on_submit():
        flash('¡Has comentado el evento con exito!')
        return redirect(url_for('index',id=1))
    return render_template('evento_con_comentario.html',comentarionuevo=comentarioNuevo)

def validarExistente(email):
    aux = False
    if db.session.query(Usuario).filter(Usuario.email.ilike(email)).count() == 0:
        aux = True
    return aux