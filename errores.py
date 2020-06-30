from flask import render_template, request, jsonify	#importamos flask
from app import app
from formulario_login import *
@app.errorhandler(404) # Manejar error de página no encontrada
def page_not_found(e):
    formularioLogin = Login()
    print(e)
    # Si la solicitud acepta json y no HTML
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        # Responder con JSON
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    # Sino responder con template HTML
    return render_template('errores/404.html', formularioLogin = formularioLogin), 404

@app.errorhandler(500) # Manejar error de error interno
def internal_server_error(e):
    formularioLogin = Login()
    print(e)
    # Si la solicitud acepta json y no HTML
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        # Responder con JSON
        response = jsonify({'error': 'internal server error'})
        response.status_code = 500
        return response
    # Sino responder con template HTML
    return render_template('errores/500.html', formularioLogin = formularioLogin), 500
