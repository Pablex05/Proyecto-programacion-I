from app import mail, app
from flask_mail import Mail, Message
from flask import render_template
from threading import Thread

#to = emisor
#subject = receptor
#templeate = la pagina web
def enviarMail(to, subject, template, **kwargs): #kwargs deja pasar o no mas  "lista" parametros
    msg = Message(subject, sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template('mail/' + template + '.txt', **kwargs) #hay gestores de correos que solo admiten texto plano y por eso enviamos estos dos tipos
    msg.html = render_template('mail/' + template + '.html', **kwargs)
    thr = Thread(target=mail_sender, args=[app, msg]) #aca abrimos un hilo que llamamos la funcion mail_sender y pasamos los argumentos app y msg
    thr.start() # Iniciar hilo


def mail_sender(app, msg):
    with app.app_context():
        mail.send(msg) #send es la que envia el mail
