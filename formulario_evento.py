from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, validators, TextField, SelectField, TextAreaField
from wtforms.fields.html5 import EmailField,DateField,DateTimeField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms_components import TimeField

class Evento_form(Form):
    lista_opciones = [			
        ('Fiesta Privada', 'Fiesta Privada'),		#esto son los distintos tipos de eventos del menu de opciones
        ('Fiesta pública', 'Fiesta pública'),
        ('Recital', 'Recital'),
        ('Deporte', 'Deporte'),
        ('Teatro', 'Teatro'),
        ('Conferencia', 'Conferencia'),
        ('Muestra', 'Muestra'),
        ('Fiesta', 'Fiesta'),
        ('Fastival', 'Fastival'),
        ('Otro', 'Otro'),
    ]
    titulo = StringField('Título Evento',[validators.DataRequired()])					#aca estamos validando cada campo del evento
    fecha = DateField('Fecha Evento',[validators.DataRequired(message="Ingrese una fecha válida")])
    hora = TimeField('Hora Evento',[validators.DataRequired(message="Ingrese una hora válida")])
    lugar = StringField('Lugar Evento',[validators.DataRequired(message='Ingrese un Lugar de Evento')])
    tipo = SelectField('Tipo', choices=lista_opciones)
    descripcion = StringField('Descripcion Evento', [validators.DataRequired(message='Ingrese una Descripcion del Evento')])
    imagen = FileField('Imagen Evento',validators=[ validators.DataRequired(), FileAllowed(['jpg', 'png'], 'El archivo debe ser una imagen jpg o png')])
    aceptar_evento = SubmitField('Enviar Evento')	#aca tenemos el submit del boton para crear el evento

class Comentario_form(Form):
    comentario = TextAreaField('Comentario', [validators.Required(message="Ingrese un comentario"),validators.Length(min=5)])	#aca estamos validando si el campo tiene o no un comentario
    submitComentario = SubmitField("Enviar")

class Filtro_form(Form):
    tipo = [					#aca tenemos el listado de cada tipo de evento que usaremos para el filtro
        ('empty', 'Todas'),
        ('Fiesta Privada','Fiesta Privada'),
        ('Fiesta pública','Fiesta pública'),
        ('Recital','Recital'),
        ('Deporte','Deporte'),
        ('Teatro','Teatro'),
        ('Conferencia','Conferencia'),
        ('Muestra','Muestra'),
        ('Fiesta','Fiesta'),
        ('Fastival','Fastival'),
        ('Otro','Otro'),
    ]
    titulo = StringField('Titulo', render_kw={"placeholder": "Titulo completo"}) # render_kw provee de un diccionario
    fecha = DateField('Fecha')
    tipo = SelectField('Tipo', [], choices=tipo) #(nombre, argumentos, tipo de funcion)
    filtro = SubmitField("Buscar")


