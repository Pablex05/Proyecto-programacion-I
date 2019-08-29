# - *- coding: utf- 8 - *-
from flask_wtf import FlaskForm #Importa funciones de formulario
from wtforms import PasswordField, SubmitField#Importa campos
from wtforms.fields.html5 import EmailField #Importa campos HTML
from wtforms import validators #Importa validaciones

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
