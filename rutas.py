# - *- coding: utf- 8 - *-
from flask_login import login_user, logout_user, login_required, current_user
from wtforms import ValidationError

from funciones import *
from flask import Flask, render_template, app  # Permite importar templates
from flask_wtf import CSRFProtect #importar para proteccion CSRF
from flask import flash #importar para mostrar mensajes flash
from flask import redirect, url_for
from formulario_registro import Registro #importar clase de formulario
from formulario_login import Login #importar clase de formulario
import datetime #importar funciones de fecha
from flask import request
from formulario_evento import *
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
    filtro = Filtro_form()
    listaeventos = eventos()
    lista = db.session.query(Evento).filter(Evento.estado == 1)
    if filtro.is_submitted():
        if filtro.fecha.data is not None:
            lista = lista.filter(Evento.fecha == filtro.fecha.data)
        print(filtro.tipo.data)
        if filtro.tipo.data != 'empty':
            lista = lista.filter(Evento.tipo == filtro.tipo.data)
        if filtro.titulo.data != "":
            lista = lista.filter(Evento.nombre.ilike('%' + filtro.titulo.data + '%'))
        print(lista)

    return render_template('pagina_principal.html',listaeventos = lista, formularioLogin = formularioLogin, nombreUsuario = current_user, filtro =filtro)
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
    return redirect(url_for('index', formularioLogin = formularioLogin))

@app.route('/usuario/nuevoUsuario', methods=["GET","POST"])
def usuario_nuevo():
    formularioLogin = Login()
    formulario_usuario = Registro()
    if formulario_usuario.validate_on_submit():
        if validarExistente(formulario_usuario.email.data):
            flash('Cuenta creada con exito!', 'success')
            usuario = Usuario(nombre=formulario_usuario.nombre.data, apellido=formulario_usuario.apellido.data, email=formulario_usuario.email.data, password=formulario_usuario.password.data)
            db.session.add(usuario)
            db.session.commit()
            flash('Se ha enviado un mail.', 'success')
            enviarMail(formulario_usuario.email.data, 'Bienvenido a EVENTIN!', 'registro', formulario=formulario_usuario)
            login_user(usuario, True)
            return redirect(url_for('index'))
        else:
            flash('Existe una cuenta registrada con el email ingresado', 'danger')
    return render_template('registro_de_nuevo_usuario.html', formulario=formulario_usuario,formularioLogin=formularioLogin,nombreUsuario = current_user)  # Mostrar template y pasar variables


@app.route('/usuario/eventoPublicado/<id>' , methods=["POST","GET"])
def evento(id):
    formularioLogin = Login()
    formulario = Evento_form()
    formulario_com = Comentario_form()
    evento = db.session.query(Evento).get(id)
    comentarios = db.session.query(Comentario).filter(Comentario.eventoId == id).all()
    print(comentarios)
    print(id)
    if formulario.is_submitted():
        if formulario_com.validate_on_submit():
            flash('Comentario fue agregado Exitosamente!', 'success')
            comentario = Comentario(texto=formulario_com.comentario.data, usuarioId=current_user.usuarioId, eventoId=id)
            db.session.add(comentario)
            db.session.commit()
            return redirect(url_for('evento', id=id, formularioLogin=formularioLogin, formulario_com=formulario_com))
        else:
            flash('comentar el evento no fue exitoso', 'danger')
    return render_template('evento_con_comentario.html', evento=evento, formulario=formulario,comentarios=comentarios, id=id, formularioLogin=formularioLogin,formulario_com=formulario_com)

@app.route('/usuario/evento/nuevoEvento', methods=["GET","POST"])
@login_required
def crear_evento():
    formularioLogin = Login()
    formulario = Evento_form()
    if formulario.validate_on_submit():  # Si el formulario es validado correctamente
        flash('evento creado exitosamente, pero tiene que algun administrador apruebe el evento', 'success')  # Mostrar mensaje
        f = formulario.imagen.data
        filename = secure_filename(f.filename)
        f.save(os.path.join('static/imagenes', filename))
        evento = Evento(nombre = formulario.titulo.data, fecha = formulario.fecha.data, hora = formulario.hora.data, lugar = formulario.lugar.data,tipo = formulario.tipo.data, descripcion = formulario.descripcion.data, imagen = filename, usuarioId = current_user.usuarioId)
        db.session.add(evento)
        db.session.commit()
    return render_template('crear_nuevo_evento.html',formulario=formulario, destino="creando_evento", formularioLogin=formularioLogin,nombreUsuario = current_user) # Muestra el formulario

@app.route('/usuario/evento/modificarEvento/<int:id>', methods=["GET","POST"])
@login_required
def modificar_evento(id):
    formularioLogin = Login()
    formulario = Evento_form()
    evento = db.session.query(Evento).get(id)
    if has_permission(current_user, evento):
        class EventoClase:
            titulo = evento.nombre
            fecha = evento.fecha
            hora = evento.hora
            lugar = evento.lugar
            imagen = evento.imagen
            descripcion = evento.descripcion
            tipo = evento.tipo
        formulario = Evento_form(obj=EventoClase)
        if formulario.validate_on_submit():
            flash('Se a modificado el evento exitosamente, pero no se visualizara hasta que un administrador lo apruebe', 'success')
            evento.nombre = formulario.titulo.data
            evento.fecha = formulario.fecha.data
            evento.hora = formulario.hora.data
            evento.lugar = formulario.lugar.data
            evento.descripcion = formulario.descripcion.data
            evento.tipo = formulario.tipo.data
            evento.estado = 0
            db.session.add(evento)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('crear_nuevo_evento.html', nombreusuario=evento.usuario,  formulario=formulario, destino="modificar_evento", formularioLogin=formularioLogin,nombreUsuario = current_user,evento=evento)  # Muestra el formulario

@app.route('/usuario/evento/eliminarEvento/<id>', methods=["GET", "POST"])
@login_required
def eliminar_evento(id):
    evento = db.session.query(Evento).get(id)
    db.session.delete(evento)
    db.session.commit()
    flash('Evento a sido eliminado exitosamente', 'success')  # Mostrar mensaje
    return redirect(url_for('index'))

@app.route('/usuario/evento/aprobacionDeEstado/<id>/<estado>', methods=["GET", "POST"])
@login_required
def aprobar_evento(id,estado):

    if current_user.is_admin():
        evento = db.session.query(Evento).get(id)
        evento.estado = estado
        db.session.add(evento)
        db.session.commit()
        if estado == 1:
            enviarMail(evento.usuario.email, 'Evento a sido aprobado', 'aprobado', evento=evento)
        if estado == 0:
            enviarMail(evento.usuario.email, 'Evento a sido desaprobado', 'desaprobado', evento=evento)
        return redirect(url_for('panel_eventos_admin'))
    else:
        flash('Usted no es un administrador para entrar a este servicio', 'danger')
        return redirect(url_for('index',nombreUsuario = current_user))



@app.route('/usuario/panelDeEventos/', methods=["GET", "POST"])
@login_required
def panel_eventos():
    formularioLogin = Login()
    listaeventos = eventos()
    usuarioId = current_user.usuarioId  #esto es para filtrar el usuario para que solo me muestre sus eventos
    return render_template('panel_eventos_creados.html', listaeventos=listaeventos,formularioLogin = formularioLogin,usuarioId = usuarioId )


@app.route('/usuario/panelDeEventosAdmin', methods=["GET", "POST"])
@login_required
def panel_eventos_admin():
    formularioLogin = Login()
    listaeventos = eventos()
    if current_user.is_admin():
        return render_template('panel_eventos_creados_admin.html', listaeventos=listaeventos, nombreUsuario=current_user,formularioLogin = formularioLogin)
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
    return render_template('evento_con_comentario.html',comentarionuevo=comentarioNuevo,nombreUsuario = current_user)


@app.route('/eliminarComentario/<int:id>')
@login_required
def eliminarComentario(id):
    comentario = db.session.query(Comentario).get(id)
    if current_user.is_admin() or current_user.is_owner(comentario):
        db.session.delete(comentario)
        db.session.commit()
        flash('Comentario a sido eliminado!', 'success')
        return redirect(url_for('evento', id=comentario.eventoId))
    else:
        flash('Usted no es un administrador para entrar a este servicio', 'danger')
        return redirect(url_for('evento'))


def validarExistente(email):
    aux = False
    if db.session.query(Usuario).filter(Usuario.email.ilike(email)).count() == 0:
        aux = True
    return aux