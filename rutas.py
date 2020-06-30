# - *- coding: utf- 8 - *-
from flask_login import login_user, logout_user, login_required, current_user  # current user contiene el usuario completo
from wtforms import ValidationError
from funciones import *
from flask import Flask, render_template, app  # Permite importar templates
from flask_wtf import CSRFProtect  # importar para proteccion CSRF
from flask import flash  # importar para mostrar mensajes flash
from flask import redirect, url_for
from formulario_registro import Registro  # importar clase de formulario
from formulario_login import Login  # importar clase de formulario
import datetime  # importar funciones de fecha
from flask import request
from formulario_evento import *
from app import db, app, login_manager
from funciones_mail import *
from modelos import Evento, Usuario, Comentario
from werkzeug.utils import secure_filename  # Importa seguridad nombre de archivo
import os.path

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('Debe iniciar sesión para continuar.', 'warning')
    return redirect(url_for('index'))

def has_permission(user, evento):
    aux = False
    if user.is_authenticated:
        if user.is_admin() or user.is_owner(evento):
            aux = True
    return aux

# La diferencia entre los métodos get y post radica en la forma de enviar los datos a la página cuando se pulsa el botón “Enviar”.
@app.route('/', methods=["POST","GET"])  # Mientras que el método GET envía los datos usando la URL, el método POST los envía de forma que no podemos verlos
def index():
    formularioLogin = Login()  # Instanciar formulario de Login
    filtro = Filtro_form()
    lista = db.session.query(Evento).filter(Evento.estado == 1)
    if filtro.is_submitted():  # esto es donde si usamos el filtro
        if filtro.fecha.data is not None:
            lista = lista.filter(Evento.fecha == filtro.fecha.data)  # filtro por fecha
        print(filtro.tipo.data)
        if filtro.tipo.data != 'empty':
            lista = lista.filter(Evento.tipo == filtro.tipo.data)  # filtro por tipo de evento
        if filtro.titulo.data != "":
            lista = lista.filter(Evento.nombre.ilike('%' + filtro.titulo.data + '%'))  # filtro por titulo
        print(lista)
    return render_template('pagina_principal.html', listaeventos=lista, formularioLogin=formularioLogin,
                           nombreUsuario=current_user, filtro=filtro)


@app.route('/usuario/login', methods=["POST"])
def login():
    formularioLogin = Login()
    if formularioLogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formularioLogin.email.data).first()
        # Si el usuario existe y se verifica la pass
        if usuario is not None and usuario.verificar_pass(formularioLogin.password.data):
            # Loguear usuario
            login_user(usuario, formularioLogin.remember_me.data)
        else:
            # Mostrar error de autenticación
            flash('Email o pass incorrectas.', 'success')
    return redirect(url_for('index', formularioLogin=formularioLogin))


@app.route('/logout')
# Limitar el acceso a los usuarios registrados
@login_required
def logout():
    logout_user()
    # Insntanciar formulario de Login
    formularioLogin = Login()
    return redirect(url_for('index', formularioLogin=formularioLogin))

@app.route('/usuario/crear-usuario', methods=["GET", "POST"])
def usuario_nuevo():  # es la funcion para crear un usuario nuevo
    formularioLogin = Login()
    formulario_usuario = Registro()
    if formulario_usuario.validate_on_submit():  # aca comprueba si el usuario envio un formulario
        if validarExistente(formulario_usuario.email.data):  # aca comprueba si el usuario ingresado no existe
            if formulario_usuario.nombre.data.isalpha() == True:  #verifica si el nombre es alfabetico
                if formulario_usuario.apellido.data.isalpha() == True: #verifica si el apellido es alfabetico
                    usuario = Usuario(nombre=formulario_usuario.nombre.data, apellido=formulario_usuario.apellido.data,
                                  email=formulario_usuario.email.data, password=formulario_usuario.password.data)
                    actualizar_BD(usuario) #envia los datos de usuario a la funcion para que se agregue en la base de datos
                    flash('Cuenta creada con exito!', 'success')
                    enviarMail(formulario_usuario.email.data, 'Bienvenido a EVENTIN!', 'registro', formulario=formulario_usuario)
                    login_user(usuario, True)
                    return redirect(url_for('index'))
                else:
                    flash('Apellido mal introducido, debe ser solamente ALFABETICO', 'danger')
            else:
                flash('Nombre mal introducido, debe ser solamente ALFABETICO','danger')
        else:  # si existe el usuario
            flash('Existe una cuenta registrada con el email ingresado',
                  'danger')  # va a indicar que esa cuenta ya existe
    return render_template('registro_de_nuevo_usuario.html', formulario=formulario_usuario,
                           formularioLogin=formularioLogin,
                           nombreUsuario=current_user)  # Mostrar template y pasar variables
# cqlqoestsuqautjl
@app.route('/evento/<id>', methods=["POST", "GET"])
def evento(id):
    formularioLogin = Login()
    formulario = Evento_form()
    formulario_com = Comentario_form()
    evento = db.session.query(Evento).get(id)
    comentarios = listar_comentarios(id)
    if formulario.is_submitted():  # aca comprueba si el formulario es valido correctamente
        if formulario_com.validate_on_submit():  # aca comprueba el comentario que se agrego en el evento por el usuario
            comentario = Comentario(texto=formulario_com.comentario.data, usuarioId=current_user.usuarioId, eventoId=id)
            actualizar_BD(comentario)
            flash('Comentario Enviado!', 'success')
            return redirect(url_for('evento', id=id, formularioLogin=formularioLogin, formulario_com=formulario_com))
        else:
            flash('comentar el evento no fue exitoso', 'danger')
    return render_template('evento_con_comentario.html', evento=evento, formulario=formulario, comentarios=comentarios,
                           id=id, formularioLogin=formularioLogin, formulario_com=formulario_com)

@app.route('/evento/crear-evento', methods=["GET", "POST"])
@login_required
def crear_evento():
    formularioLogin = Login()
    formulario = Evento_form()
    if formulario.validate_on_submit():  # Si el formulario es validado correctamente
        flash('evento creado exitosamente, pero tiene que algun administrador apruebe el evento',
              'success')  # Mostrar mensaje
        f = formulario.imagen.data
        filename = secure_filename(f.filename)
        f.save(os.path.join('static/imagenes', filename))
        evento = Evento(nombre=formulario.titulo.data, fecha=formulario.fecha.data, hora=formulario.hora.data,
                        lugar=formulario.lugar.data, tipo=formulario.tipo.data, descripcion=formulario.descripcion.data,
                        imagen=filename, usuarioId=current_user.usuarioId)
        actualizar_BD(evento)
    return render_template('crear_nuevo_evento.html', formulario=formulario, destino="creando_evento",
                           formularioLogin=formularioLogin, nombreUsuario=current_user)  # Muestra el formulario


@app.route('/evento/modificar-evento/<int:id>', methods=["GET", "POST"])
@login_required
def modificar_evento(id):
    formularioLogin = Login()
    formulario = Evento_form()
    evento = db.session.query(Evento).get(id)
    if has_permission(current_user, evento):  # aca comprueba que el usuario sea dueño del evento
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
            flash(
                'Se a modificado el evento exitosamente, pero no se visualizara hasta que un administrador lo apruebe',
                'success')
            evento.nombre = formulario.titulo.data
            evento.fecha = formulario.fecha.data
            evento.hora = formulario.hora.data
            evento.lugar = formulario.lugar.data
            evento.descripcion = formulario.descripcion.data
            evento.tipo = formulario.tipo.data
            evento.estado = 0
            actualizar_BD(evento)
            return redirect(url_for('index'))
    return render_template('crear_nuevo_evento.html', nombreusuario=evento.usuario, formulario=formulario,
                           destino="modificar_evento", formularioLogin=formularioLogin, nombreUsuario=current_user,
                           evento=evento)  # Muestra el formulario


@app.route('/evento/eliminar/<id>', methods=["GET", "POST"])
@login_required
def eliminar_evento(id):
    evento = db.session.query(Evento).get(id)
    eliminar_BD(evento)
    flash('Evento a sido eliminado exitosamente',
          'success')  # Muestra el mensaje de que se elimino exitosamente el evento
    return redirect(url_for('index'))


@app.route('/evento/aprobacion-de-estado/<id>/<estado>', methods=["GET", "POST"])
@login_required
def aprobar_evento(id, estado):
    if current_user.is_admin():  # comprueba si el usuario es admin
        evento = db.session.query(Evento).get(id)
        evento.estado = estado
        actualizar_BD(evento)
        if estado == 1:
            enviarMail(evento.usuario.email, 'Evento a sido aprobado', 'aprobado', evento=evento)
        if estado == 0:
            enviarMail(evento.usuario.email, 'Evento a sido desaprobado', 'desaprobado', evento=evento)
        return redirect(url_for('panel_eventos_admin'))
    else:  # si no es admin va a mostrar este error
        flash('Usted no es un administrador para entrar a este servicio', 'danger')
        return redirect(url_for('index', nombreUsuario=current_user))


@app.route('/panel-eventos/', methods=["GET", "POST"])
@login_required
def panel_eventos():
    formularioLogin = Login()
    listaeventos = eventos()
    usuarioId = current_user.usuarioId  # esto es para filtrar el usuario para que solo me muestre sus eventos
    return render_template('panel_eventos_creados.html', listaeventos=listaeventos, formularioLogin=formularioLogin,
                           usuarioId=usuarioId)


@app.route('/panel-eventos-admin', methods=["GET", "POST"])
@login_required
def panel_eventos_admin():
    formularioLogin = Login()
    listaeventos = eventos()
    if current_user.is_admin():
        return render_template('panel_eventos_creados_admin.html', listaeventos=listaeventos,
                               nombreUsuario=current_user,
                               formularioLogin=formularioLogin)  # aca muestra todos los eventos
    else:
        flash('Usted no es un administrador para entrar a este servicio', 'danger')
        return redirect(url_for('index'))


@app.route('/evento/comentario/agregar', methods=["POST"])
@login_required
def agregar_comentario():
    comentarioNuevo = Comentario_form()
    if comentarioNuevo.validate_on_submit():  # comprueba que sea valido el comentario
        flash('¡Has comentado el evento con exito!')
        return redirect(url_for('index', id=1))
    return render_template('evento_con_comentario.html', comentarionuevo=comentarioNuevo, nombreUsuario=current_user)


@app.route('/evento/comentario/eliminar/<int:id>')
@login_required
def eliminarComentario(id):
    comentario = db.session.query(Comentario).get(id)
    if current_user.is_admin() or current_user.is_owner(
            comentario):  # comprueba que sea un admin o que sea el dueño del comentario
        eliminar_BD(comentario)
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
