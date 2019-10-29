# - *- coding: utf- 8 - *-
from app import app, db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash #Permite generar y verificar pass con hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer #este es para generar los tokens
from flask_login import UserMixin, LoginManager
from rutas import *
class Evento(db.Model):
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

	# No permitir leer la pass de un usuario
	@property
	def password(self):
		raise AttributeError('La password no puede leerse')

	# Al setear la pass generar un hash
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def get_id(self):
		return (self.usuarioId)

	# Al verififcar pass comparar hash del valor ingresado con el de la db
	def verificar_pass(self, password):
		return check_password_hash(self.password_hash, password)

	# Generar token de confirmación
	def generar_token_confirmacion(self, expiracion=300):
		# Crear una JSON Web Signatures a partir de la SECRET_KEY
		# Colocar un tiempo de expiración de 3600 segundos
		s = Serializer(app.config['SECRET_KEY'], expiracion)
		# Convertir JWS en un Token string
		return s.dumps({'confirm': self.usuarioId}).decode('utf-8')

	# Al recibir el código de confirmación comparar con el generado
	def confirmar(self, token):
		# Crear una JSON Web Signatures a partir de la SECRET_KEY
		s = Serializer(app.config['SECRET_KEY'])
		try:
			# Intentar cargar a partir del token brindado por el usuario
			data = s.loads(token.encode('utf-8'))
		except:
			return False
		# Si el dato coincide con el id del usuario
		if data.get('confirm') != self.usuarioId:
			return False
		# Setear el campo de confirmación del usuario a verdadero
		self.confirmado = True
		db.session.add(self)
		db.session.commit()
		return True

	def __repr__(self):
		return '<Usuario %r>' % self.email

class Comentario(db.Model):
	comentarioId = db.Column(db.Integer, primary_key=True)
	texto = db.Column(db.String(500),nullable = False)
	fecha = db.Column(db.Date, nullable = False)
	hora = db.Column(db.Time, nullable=False)
	usuarioId = db.Column(db.Integer, db.ForeignKey('usuario.usuarioId'), nullable = False)
	eventoId = db.Column(db.Integer, db.ForeignKey('evento.eventoId'), nullable = False)
	evento = db.relationship('Evento', back_populates="comentarios")
	usuario = db.relationship('Usuario', back_populates="comentarios")
	def __repr__(self):
		return '<Comentario %r %r>' % (self.texto, self.fechahora)

@login_manager.user_loader
def load_user(user_id):
	return Usuario.query.get(int(user_id))