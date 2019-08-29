# - *- coding: utf- 8 - *-
from flask_wtf import FlaskForm #Importa funciones de formulario
from wtforms import StringField, TextField , HiddenField, PasswordField, TextAreaField, SelectField, RadioField,SubmitField #Importa campos
from wtforms.fields.html5 import EmailField,DateField #Importa campos HTML
from wtforms import validators #Importa validaciones
from wtforms_components import TimeField
from flask_wtf.file import FileField, FileRequired, FileAllowed #Importa funciones, validaciones y campos de archivo

#Clase de Registro
class Registro(FlaskForm):

    #Función de validación de nombre de usuario
    def nombre_usuario(form,field):
        if (field.data.find("_")!= -1) or (field.data.find("#")!= -1) :
             raise validators.ValidationError("El nombre de usuario solo puede contener letras, números y .")

    #Función para hacer campo opcional
    def opcional(field):
        field.validators.insert(0, validators.Optional())

    #Definición de campo String
    nombre = StringField('Nombre Usuario',
    [
        #Definición de validaciones
        validators.Required(message = "Completar nombre de usuario de usuario"),
        validators.length(min=4, max=25, message='La longitud del nombre de usuario no es válida'),
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

