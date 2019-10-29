from app import db
from modelos import Comentario, Evento, Usuario

def comentarios():
    listar_comentarios = db.session.query(Comentario).all()
    return listar_comentarios
def eventos():
    listar_eventos = db.session.query(Evento).all()
    return listar_eventos
def crear_evento(evento):
    db.session.add(evento)
    db.session.commit()
def crear_usuario(usuario):
    db.session.add(usuario)
    db.session.commit()
def crear_comentario(comentario):
    db.session.add(comentario)
    db.session.commit()
