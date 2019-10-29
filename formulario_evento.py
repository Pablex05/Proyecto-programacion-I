from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, \
    SubmitField, BooleanField
from wtforms.fields.html5 import EmailField, DateField
from wtforms import validators
from wtforms_components import TimeField, DateRange
from flask_wtf.file import FileField, FileRequired, FileAllowed
from datetime import date
import re
from app import db
from modelos import Evento, Comentario, Usuario


class Evento_form(Form):

    #Función para hacer campo opcional
    def opcional(field):
        field.validators.insert(0, validators.Optional())
    def nombre_usuario(form,field):
        if (field.data.find("_")!= -1) or (field.data.find("#")!= -1) :
             raise validators.ValidationError("El nombre de usuario solo puede contener letras, números y .")
    def apellido_usuario(form,field):
        if (field.data.find("_")!= -1) or (field.data.find("#")!= -1) :
             raise validators.ValidationError("El nombre de usuario solo puede contener letras, números y .")

    titulo = StringField('Título Evento',[validators.DataRequired()])
    fecha = DateField('Fecha Evento',[validators.DataRequired(message="Ingrese una fecha válida")])
    hora = TimeField('Hora Evento',[validators.DataRequired(message="Ingrese una hora válida")])
    lugar = StringField('Lugar Evento',[validators.DataRequired(message='Ingrese un Lugar de Evento')])
    descripcion = StringField('Descripcion Evento', [validators.DataRequired(message='Ingrese una Descripcion del Evento')])
    imagen = FileField('Imagen Evento',validators=[ validators.DataRequired(), FileAllowed(['jpg', 'png'], 'El archivo debe ser una imagen jpg o png')])
    aceptar_evento = SubmitField('Enviar Evento')

"""
class Comentario_form(Form):
    comentario = StringField('Escribir un Comentario:',[validators.DataRequired(message="Comentario faltante")])
    submit = SubmitField("Enviar Comentario")
"""
class Comentario_form(Form):
    comentario = TextAreaField('Escriba su comentario',
                              [
                                  validators.DataRequired(message="No puede comentar en blanco."),
                                  validators.length(min=4, max=350, message="Su comentario debe tener entre "
                                                                            "4 y 350 caracteres")
                              ])
    submit = SubmitField("Comentar")

    def mostrar_datos(self):
        print("Comentario: " + str(self.comentario.data))

