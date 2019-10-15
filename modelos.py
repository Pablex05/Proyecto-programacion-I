# - *- coding: utf- 8 - *-
from app import db

class Evento(db.Model):
	eventoId = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(80), nullable=False)
	fecha = db.Column(db.DateTime, nullable = False)
	hora = db.Column(db.DateTime, nullable=False)
	descripcion = db.Column(db.String(500), nullable = False)
	imagen = db.Column(db.String(40), nullable = False)
	tipo = db.Column(db.String(15), nullable = False)
	usuarioId = db.Column(db.Integer, db.ForeignKey('usuario.usuarioId'), nullable = False)
	usuario = db.relationship('Usuario', back_populates="eventos")
	comentarios = db.relationship('Comentario', back_populates="evento")
	def __repr__(self):
		return '<Evento %r %r %r %r ' % (self.nombre, self.fecha, self.tipo, self.descripcion)
class Usuario(db.Model):
	usuarioId = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(20), nullable = False)
	apellido = db.Column(db.String(20), nullable = False)
	email = db.Column(db.String(50), nullable = False)
	password = db.Column(db.String(40), nullable = False)
	admin = db.Column(db.Boolean, nullable = False)
	comentarios = db.relationship('Comentario', back_populates="usuario")
	eventos = db.relationship('Evento', back_populates="usuario")
	def __repr__(self):
		return '<Usuario %r %r>' % (self.nombre, self.apellido)
class Comentario(db.Model):
	comentarioId = db.Column(db.Integer, primary_key=True)
	texto = db.Column(db.String(500),nullable = False)
	fechahora = db.Column(db.DateTime, nullable = False)
	usuarioId = db.Column(db.Integer, db.ForeignKey('usuario.usuarioId'), nullable = False)
	eventoId = db.Column(db.Integer, db.ForeignKey('evento.eventoId'), nullable = False)
	evento = db.relationship('Evento', back_populates="comentarios")
	usuario = db.relationship('Usuario', back_populates="comentarios")
	def __repr__(self):
		return '<Comentario %r %r>' % (self.texto, self.fechahora)
#db.drop_all()
#db.create_all()
