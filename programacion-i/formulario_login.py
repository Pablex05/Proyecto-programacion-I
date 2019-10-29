# - *- coding: utf- 8 - *-
from modelos import *
from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField
from wtforms import PasswordField, BooleanField, SubmitField, StringField, validators
from wtforms.validators import ValidationError, Required, Email, EqualTo

#Clase de Login
class Login(FlaskForm):

    #Definición de campo de contraseña
    password = PasswordField('Password', [
        validators.Required(),
    ])

    #Definición de campo de mail
    email = EmailField('E-mail',
    [
        validators.Required(message = "Completar email"),
        validators.Email( message ='Formato de mail incorrecto')
    ])

    #Definición de campo submit
    submit = SubmitField("Enviar")
