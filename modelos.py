# - *- coding: utf- 8 - *-
from app import app, db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash #Permite generar y verificar pass con hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer #este es para generar los tokens
from flask_login import UserMixin, LoginManager


class Evento(db.Model,UserMixin):
	eventoId = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(80), nullable=False)
	fecha = db.Column(db.Date, nullable = False)
	hora = db.Column(db.Time, nullable=False)
	descripcion = db.Column(db.String(500), nullable = False)
	imagen = db.Column(db.String(40), nullable = True)
	tipo = db.Column(db.String(15), nullable = False)
	lugar = db.Column(db.String(100), nullable = False)
	usuarioId = db.Column(db.Integer, db.ForeignKey('usuario.usuarioId'), nullable = False)
	usuario = db.relationship('Usuario', back_populates="eventos")
	estado = db.Column(db.Integer, nullable = False, default=0)
	comentarios = db.relationship('Comentario', back_populates="evento",cascade="all, delete-orphan")
	def __repr__(self):
		return '<Evento %r %r %r %r ' % (self.nombre, self.fecha, self.tipo, self.descripcion)
class Usuario(UserMixin, db.Model):
	usuarioId = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(20), nullable = False)
	apellido = db.Column(db.String(20), nullable = False)
	email = db.Column(db.String(50),unique=True, index=True)
	password_hash = db.Column(db.String(128))
	admin = db.Column(db.Boolean, nullable = False, default=0)
	comentarios = db.relationship('Comentario', back_populates="usuario")
	eventos = db.relationship('Evento', back_populates="usuario")
	confirmado = db.Column(db.Boolean, default=False)

	@property
	def password(self):
		raise AttributeError('La password no puede leerse')
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
	def get_id(self):
		return self.usuarioId
	def verificar_pass(self, password):
		return check_password_hash(self.password_hash, password)
	def __repr__(self):
		return str(self.nombre) + ' ' + str(self.apellido)
	def is_admin(self):  # Comprueba si el usuario es administrador
		aux = False
		if self.admin == 1:
			aux = True
		return aux
	def is_owner(self, event_or_coment):  # Comprueba si el usuario es dueño, puede usarse con comentarios o eventos.
		aux = False
		if self.usuarioId == event_or_coment.usuarioId:
			aux = True
		return aux

class Comentario(db.Model,UserMixin):
	comentarioId = db.Column(db.Integer, primary_key=True)
	texto = db.Column(db.String(500),nullable = False)
	fecha = db.Column(db.Date, nullable=False, default=db.func.current_timestamp())
	hora = db.Column(db.Time,  nullable=False, default=db.func.current_timestamp())
	usuarioId = db.Column(db.Integer, db.ForeignKey('usuario.usuarioId'), nullable = False)
	eventoId = db.Column(db.Integer, db.ForeignKey('evento.eventoId'), nullable = False)
	evento = db.relationship('Evento', back_populates="comentarios")
	usuario = db.relationship('Usuario', back_populates="comentarios")

@login_manager.user_loader
def load_user(user_id):
	return Usuario.query.get(int(user_id))

