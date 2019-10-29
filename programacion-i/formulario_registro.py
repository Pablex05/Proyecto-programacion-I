# - *- coding: utf- 8 - *-
from app import db
from modelos import Usuario
from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField
from wtforms import PasswordField, BooleanField, SubmitField, StringField, validators
from wtforms.validators import ValidationError, Required, Email, EqualTo


#Clase de Registro
class Registro(FlaskForm):

    #Función de validación de nombre de usuario
    def nombre_usuario(form,field):
        if (field.data.find("_")!= -1) or (field.data.find("#")!= -1) :
             raise validators.ValidationError("El nombre de usuario solo puede contener letras, números y .")
    def apellido_usuario(form,field):
        if (field.data.find("_")!= -1) or (field.data.find("#")!= -1) :
             raise validators.ValidationError("El nombre de usuario solo puede contener letras, números y .")

    #Función para hacer campo opcional
    def opcional(field):
        field.validators.insert(0, validators.Optional())

    #Definición de campo String
    nombre = StringField('Nombre',
    [
        #Definición de validaciones
        validators.DataRequired(message="Completar nombre"),
        validators.length(min=4, max=25, message='La longitud del nombre no es válida'),
        nombre_usuario
    ])
    apellido = StringField('Apellido',
    [
        #Definición de validaciones
        validators.Required(message = "Completar apellido"),
        validators.length(min=4, max=25, message='La longitud del apellido no es válida'),
        nombre_usuario
    ])
    email = EmailField('Correo',
    [
        validators.Required(message = "Completar email"),
        validators.Email( message ='Formato de mail incorrecto')
    ])

    password = PasswordField('Contraseña', [
        validators.Required(),
         #El campo de contraseña debe coincidir con el de confirmuar
        validators.EqualTo('confirmar', message='La contraseña no coincide')
    ])

    confirmar = PasswordField('Repetir contraseña')


    submit = SubmitField("Regristrar")
    #Verificar si el email ya existe en la db
    def validate_email(self, field):
        if Usuario.query.filter_by(email=field.data).first():
            raise ValidationError('El email ya ha sido registrado.')


