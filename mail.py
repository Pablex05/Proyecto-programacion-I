from app import mail, app
from rutas import *
from flask_mail import Mail, Message
from flask import render_template
from threading import Thread



def enviarMail(to, subject, template, **kwargs):
    msg = Message(subject, sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template('mail/' + template + '.txt', **kwargs)
    msg.html = render_template('mail/' + template + '.html', **kwargs)
    thr = Thread(target=mail_sender, args=[app, msg])
    # Iniciar hilo
    thr.start()


def mailRegistro(app, msg):
    with app.app_context():
        mail.send(msg)