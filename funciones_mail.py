import smtplib
from flask import render_template
from flask_mail import Message, Mail
from app import app, mail

def enviarMail(to, subject, template, **kwargs):
    msg = Message( subject, sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    cod_error=0
    try:
        mail.send(msg)
    except smtplib.SMTPSenderRefused as e:
        cod_error = 4
    except smtplib.SMTPAuthenticationError as e:
        cod_error = 3
    except smtplib.SMTPServerDisconnected as e:
        cod_error = 2
    except smtplib.SMTPException as e:
        cod_error = 1
    return cod_error


#Función que envía mensaje de registro
def enviarMailRegistro(usuario,token):
    return enviarMail(usuario.email,'Confirmación registro','mail/registro',usuario = usuario, token = token)
def enviarMailAprobado(usuario):
    return enviarMail(usuario.email,'Confirmación registro','mail/registro',usuario = usuario)
