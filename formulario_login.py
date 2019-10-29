# - *- coding: utf- 8 - *-

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
from modelos import *


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
    submit = SubmitField("Iniciar")


