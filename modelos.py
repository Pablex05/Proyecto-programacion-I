# - *- coding: utf- 8 - *-
from flask_login import UserMixin  #UserMixin almacena la id del usuario en la sesion ademas tambien maneja el acceso dependiendo el tipo de usuario
from werkzeug.security import generate_password_hash, check_password_hash #esto es para encriptar las pass
from app import db, app, login_manager
from flask import url_for
from datetime import date, datetime
from werkzeug.security import generate_password_hash, check_password_hash   # Permite generar y verificar pass con hash      # TOKENS
from flask_login import UserMixin, LoginManager

class Evento(db.Model):
	eventoId = db.Column(db.Integer, primary_key=True) #aca estamos diciendo que el "eventoId" es la clave primaria(es con lo que se va a relacionar con el resto de las tablas)
	nombre = db.Column(db.String(80), nullable=False)
	fecha = db.Column(db.Date, nullable=False)
	hora = db.Column(db.Time, nullable=False)
	descripcion = db.Column(db.String(500), nullable=False)
	imagen = db.Column(db.String(350), nullable=False)
	tipo = db.Column(db.String(15), nullable=True)
	lugar = db.Column(db.String(100), nullable=False)
	usuarioId = db.Column(db.Integer, db.ForeignKey('usuario.usuarioId'), nullable=False) #aca usuarioId es una clave foranea y es con que se va a relacionar con la id de un usuario
	usuario = db.relationship('Usuario', back_populates="eventos")	#aca es que el evento esta relacionada con un usuario en particular
	estado = db.Column(db.Integer, nullable=False, default=0)	#aca es que cuando se crea un evento, el mismo esta en un estado "0" y que el admin tiene que aprobarlo
	comentarios = db.relationship('Comentario', back_populates="evento", cascade="all, delete-orphan")# delete-orphan hace que se borre cuando el evento se elimine

	# Convertir objeto en JSON
	def to_json(self):
		evento_json = {
			'eventoId': url_for('apiGetEventoById', id=self.eventoId, _external=True),
			'titulo': self.nombre,
			'fecha': self.fecha,
			'lugar': self.lugar,
			'imagen': self.imagen,
			'descripcion': self.descripcion,
			'tipo': self.tipo,
		}
		return evento_json

	@staticmethod
	# Convertir JSON a objeto
	def from_json(evento_json):
		titulo = evento_json.get('titulo')
		fecha = evento_json.get('fecha')
		lugar = evento_json.get('lugar')
		imagen = evento_json.get('imagen')
		descripcion = evento_json.get('descripcion')
		tipo = evento_json.get('tipo')
		return evento(evento=evento, titulo=titulo, fecha=fecha, lugar=lugar,imagen=imagen, descripcion=descripcion, tipo=tipo, estado=estado)

	def __repr__(self):
		return '<Evento %r %r %r %r %r %r' % (self.nombre, self.fecha, self.tipo,self.hora, self.descripcion, self.lugar)

class Usuario(UserMixin, db.Model): #UserMixin almacena la id del usuario en la sesion y lo utiliza para hacer el login y logout, ademas tambien maneja el acceso dependiendo el tipo de usuario( currente_user, usuario anonimo, user_admin)
	usuarioId = db.Column(db.Integer, primary_key=True)	#aca estamos diciendo que el "ususarioId" es la clave primaria(es con lo que se va a relacionar con el resto de las tablas)
	nombre = db.Column(db.String(20), nullable = False)
	apellido = db.Column(db.String(20), nullable = False)
	email = db.Column(db.String(50), nullable = False)
	password_hash = db.Column(db.String(128), nullable = False) 	#aca estan las claves encriptadas de los usuario
	admin = db.Column(db.Integer, nullable=False, default=0) 	#aca indica si un usuario es administrador o un usuario comun
	comentarios = db.relationship('Comentario', back_populates="usuario")	#aca estamos diciendo que uno o varios comentarios estan relacionados con un usuario
	eventos = db.relationship('Evento', back_populates="usuario")		#aca estamos diciendo que uno o varios eventos estan relacionados con un usuario

	#  No permitir leer la pass de un usuario
	@property #esto actuaria como un getter (seria como lo  muestra)
	def password(self):
		raise AttributeError('La password no puede leerse') #aca es donde pasamos la pass

	#  Al setear la pass generar un hash
	@password.setter #esto actuaria como un setter (seria como lo setea)
	def password(self, password):
		self.password_hash = generate_password_hash(password) #aca es donde la encriptamos

	def __repr__(self):
		return str(self.nombre) + ' ' + str(self.apellido) #verificar el nombre y el apellido, si no estan lo va a remplazar con "<usuario 1>

	def get_id(self):
		return self.usuarioId

	def verificar_pass(self, password):
		return check_password_hash(self.password_hash, password) #  Al verififcar pass comparar hash del valor ingresado con el de la db

	def is_admin(self):  # Comprueba si el usuario es administrador
		aux = False
		if self.admin == 1:
			aux = True
		return aux

	def is_owner(self, event_or_coment):  # Comprueba si el usuario si es dueño del evento o el comentario
		aux = False
		if self.usuarioId == event_or_coment.usuarioId:
			aux = True
		return aux

	# Convertir objeto en JSON
	def to_json(self):
		usuario_json = {
			'usuarioId': url_for('apiGetUsuarioById', id=self.usuarioId, _external=True),
			'usuario': self.usuario,
			'nombre': self.nombre,
			'apellido': self.apellido,
			'email': self.email,
		}
		return usuario_json

	@staticmethod
	# Convertir JSON a objeto
	def from_json(usuario_json):
		usuario = usuario_json.get('usuario')
		nombre = usuario_json.get('nombre')
		apellido = usuario_json.get('apellido')
		email = usuario_json.get('email')
		return usuario(usuario=usuario, nombre=nombre, apellido=apellido, email=email)

class Comentario(db.Model):
	comentarioId = db.Column(db.Integer, primary_key=True)	#aca estamos diciendo que el "comentarioId" es la clave primaria(es con lo que se va a relacionar con el resto de las tablas)
	texto = db.Column(db.String(500),nullable = False)
	fechaHora = db.Column(db.DateTime, nullable = False, default=db.func.current_timestamp()) #cuando se crea el comentario, se registra la fecha y la hora automaticamente
	usuarioId = db.Column(db.Integer, db.ForeignKey('usuario.usuarioId'), nullable = False) #aca cuando se crea el comentario se registra la id del usuario
	eventoId = db.Column(db.Integer, db.ForeignKey('evento.eventoId'), nullable = False)	#aca se registra en que evento se le hizo el comentario
	evento = db.relationship('Evento', back_populates="comentarios")		#aca estamos diciendo que los comentarios estan relacionados a un evento
	usuario = db.relationship('Usuario', back_populates="comentarios")		#aca estamos diciendo que los comentarios estan relacionados a un usuario 

	# Convertir objeto en JSON
	def to_json(self):
		comentario_json = {
			'comentarioId': url_for('apiGetComentarioById', id=self.comentarioId, _external=True),
			'usuario': self.usuario.nombre + ' ' + self.usuario.apellido,
			'texto': self.texto,
			'evento': url_for('apiGetEventoById', id=self.eventoId, _external=True)
		}
		return comentario_json

	@staticmethod
	# Convertir JSON a objeto
	def from_json(comentario_json):
		usuario = comentario_json.get('usuario')
		evento = comentario_json.get('evento')
		texto = comentario_json.get('texto')
		return comentario(evento=evento, usuario=usuario, texto=texto)

	def __repr__(self):
		return '<Comentario %r %r %r>' % (self.texto, self.fechaHora, self.usuario)

@login_manager.user_loader #cuando se inicia sesion, cuando tenemos una id de usuario, le estamos diciendo a partir de la id como va a obtener el resto de los datos
def load_user(user_id):
	return Usuario.query.get(int(user_id))


