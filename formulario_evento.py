from flask_wtf import Form
from wtforms import StringField,PasswordField,SubmitField,validators,TextField
from wtforms.fields.html5 import EmailField,DateField,DateTimeField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms_components import TimeField

class Evento(Form):

    #Función para hacer campo opcional
    def opcional(field):
        field.validators.insert(0, validators.Optional())

    titulo = StringField('Título Evento',[validators.DataRequired()])
    fecha = DateField('Fecha Evento',[validators.DataRequired(message="Ingrese una fecha válida")])
    hora = TimeField('Hora Evento',[validators.DataRequired(message="Ingrese una hora válida")])
    lugar = StringField('Lugar Evento',[validators.DataRequired(message='Ingrese un Lugar de Evento')])
    descripcion = StringField('Descripcion Evento', [validators.DataRequired(message='Ingrese una Descripcion del Evento')])
    imagen = FileField('Imagen Evento',validators=[ validators.DataRequired(), FileAllowed(['jpg', 'png'], 'El archivo debe ser una imagen jpg o png')])
    aceptar_evento = SubmitField('Enviar Evento')


class Comentario(Form):
    comentario = StringField('Escribir un Comentario:',[validators.DataRequired(message="Comentario faltante")])
    submit = SubmitField("Enviar Comentario")