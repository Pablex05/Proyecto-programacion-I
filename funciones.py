from app import db
from modelos import Comentario, Evento, Usuario


def eventos():
    listar_eventos = db.session.query(Evento).all()
    return listar_eventos
def eventos_usuario():
    eventos_usuario = db.session.query(Usuario).all()
    return eventos_usuario
def crear_evento(evento):
    db.session.add(evento)
    db.session.commit()
def crear_usuario(usuario):
    db.session.add(usuario)
    db.session.commit()
def crear_comentario(comentario):
    db.session.add(comentario)
    db.session.commit()
def mostrar_comentarios(id):
    return db.session.query(Comentario).filter(Comentario.eventoId == id).all()
def mostrar_eventos_filtro():
    lista_eventos = db.session.query(Evento).filter(Evento.tipo)
    return lista_eventos
def mostrar_eventos():
    lista_eventos = db.session.query(Evento).filter(Evento.estado == 1)
    return lista_eventos
def listar_comentarios(id):
    listar_comentarios = db.session.query(Comentario).filter(Comentario.eventoId == id).all()
    return listar_comentarios
