import os, time, smtplib
from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField
from wtforms.fields.html5 import EmailField
from wtforms import validators
from flask import flash #importar para mostrar mensajes flash
from flask_mail import Mail, Message #Importar para enviar Mail
from flask_wtf import CSRFProtect #importar para proteccion CSRF
from threading import Thread #Importar hilos
from app import mail, app
def confMsg(to, subject, template, **kwargs):
    #Configurar asunto, emisor y destinatarios
    msg = Message( subject, sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    #Seleccionar template para mensaje de texto plano
    msg.body = render_template(template + '.txt', **kwargs)
    #Seleccionar template para mensaje HTML
    msg.html = render_template(template + '.html', **kwargs)
    return msg

#Función que genera el hilo que enviará el mail
def enviarMailThread(to, subject, template, **kwargs):
    #Crear configuración
    msg = confMsg(to, subject, template, **kwargs)
    #Crear hilo
    thr = Thread(target=enviarMailAsync, args=[app, msg])
    #Iniciar hilo
    thr.start()

def enviarMailAsync(app, msg):
    #Espera 5 segundo, utilizada en el ejercicio para comprobar la diferencia entre sync y async
    time.sleep(5)
    #Se utiliza el contexto de la aplicación para tener acceso a la configuración
    with app.app_context():
        try:
            #Enviar mail
            mail.send(msg)
            print("Mail enviado correctamente")

        #Mostrar errores por consola
        except smtplib.SMTPAuthenticationError as e:
            print("Error de autenticación: "+str(e))
        except smtplib.SMTPServerDisconnected as e:
            print("Servidor desconectado: "+str(e))
        except smtplib.SMTPSenderRefused as e:
            print("Se requiere autenticación: "+str(e))
        except smtplib.SMTPException as e:
            print("Error: "+str(e))


#Clase con la configuración del formulario
class FormularioMail(FlaskForm):
    mail = EmailField('Correo',
        [
            validators.Required(message = "Completar email"),
            validators.Email( message ='Formato de mail incorrecto')

        ]
    )
    async = RadioField('Asincrónico', choices=[('1','Si'),('0','No')])
    submit = SubmitField('Enviar')
