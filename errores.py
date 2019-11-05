from flask import render_template, request, jsonify
from app import app
# Manejar error de página no encontrada
@app.errorhandler(404)
def page_not_found(e):
    print(e)
    # Si la solicitud acepta json y no HTML
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        # Responder con JSON
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    # Sino responder con template HTML
    return render_template('errores/404.html'), 404
# Manejar error de error interno
@app.errorhandler(500)
def internal_server_error(e):
    print(e)
    # Si la solicitud acepta json y no HTML
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        # Responder con JSON
        response = jsonify({'error': 'internal server error'})
        response.status_code = 500
        return response
    # Sino responder con template HTML
    return render_template('errores/500.html'), 500