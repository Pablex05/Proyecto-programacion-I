from app import db #estamos pasando la inicializacion de SQLAlchemy
from modelos import Comentario, Evento, Usuario

def eventos():
    listar_eventos = db.session.query(Evento).all()	#lo que estamos haciendo es que "listar_eventos" nos muestre todos los "eventos" de la base de datos
    return listar_eventos

def eventos_usuario():
    eventos_usuario = db.session.query(Usuario).all() #lo que estamos haciendo es que "eventos_usuario" nos muestre  todos los "eventos" del usuario que esta en la base de datos
    return eventos_usuario

def actualizar_BD(datos):
    db.session.add(datos)	#lo que estamos haciendo es agregar un evento/usuario/comentario a la base de datos
    db.session.commit()		#lo que estamos haciendo es dar la orden de subir el evento a la base de datos

def eliminar_BD(datos):
    db.session.delete(datos)    #lo que estamos haciendo es eliminar un evento/usuario/comentario a la base de datos
    db.session.commit()         #lo que estamos haciendo es dar la orden de atualizar a la base de datos

def mostrar_comentarios(id):
    return db.session.query(Comentario).filter(Comentario.eventoId == id).all()  #lo que estamos haciendo es listar todos los comentarios de un determinado evento que esta en la base de datos

def mostrar_eventos_filtro():
    lista_eventos = db.session.query(Evento).filter(Evento.tipo)	#lo que estamos haciendo es mostrar todos los eventos de un determinado por la eleccion que hagamos del filtro
    return lista_eventos

def mostrar_eventos():
    lista_eventos = db.session.query(Evento).filter(Evento.estado == 1)  #lo que estamos haciendo es mostrar todos los eventos que estan aprobados por el administrador
    return lista_eventos

def listar_comentarios(id):
    listar_comentarios = db.session.query(Comentario).filter(Comentario.eventoId == id).all()	#lo que estamos haciendo es mostrar todos los comentarios de un evento
    return listar_comentarios
