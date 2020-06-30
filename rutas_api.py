from flask import request
from app import csrf, app, db
from flask import jsonify
from funciones import *
from funciones_mail import enviarMail
"""
curl -i -X [metodo get,put,post,delete] -H [llamamos la direccion de json] [url]
	-H [llamamos la direccion de json] - H [url]
cuando usamos content y accept es para recibir y enviar el json
#curl -I: genera un encabezado 

curl -X : reemplaza el metodo por el cual nosotros lo especificamos, que por defecto es GET, para funcionar, debe estar registrado un usuario
"""
# Ver Evento por Id
# curl -i -H "Content-Type:application/json" -H "Accept: application/json" http://localhost:8000/api/evento/136
@app.route('/api/evento/<id>', methods=['GET'])
def apiGetEventoById(id):
    evento = db.session.query(Evento).get(id)
    return jsonify(evento.to_json())

# Listar eventos
# curl -H "Accept:application/json" http://localhost:8000/api/evento/
@app.route('/')
@app.route('/api/evento/', methods=['GET'])
def apiListarEventos():
    lista_eventos = eventos()
    return jsonify({'eventos': [evento.to_json() for evento in lista_eventos]})

# Actualizar evento
# curl -i -X PUT -H "Content-Type:application/json" -H "Accept:application/json" http://localhost:8000/api/evento/136 -d '{"nombre":"CEEEEEEB", "tipo":"fiesta"}'
"""cuando usamos content y accept es para recibir y enviar el json"""
@app.route('/api/evento/<id>', methods=['PUT'])
@csrf.exempt
def apiActualizarEvento(id):
    evento = db.session.query(Evento).get(id) #trae la consulta el evento de un determinado id
    evento.nombre = request.json.get('nombre', evento.nombre) #en el comando si no esta "nombre" entonces lo toma como evento.nombre
    evento.fecha = request.json.get('fecha', evento.fecha)
    evento.hora = request.json.get('hora', evento.hora)
    evento.tipo = request.json.get('tipo', evento.tipo)
    evento.lugar = request.json.get('lugar', evento.lugar)
    evento.descripcion = request.json.get('descripcion', evento.descripcion)
    evento.estado = 0
    crear_evento_F(evento)
    return jsonify(evento.to_json()), 201

# Aprobar evento
# curl -i -X PUT -H "Content-Type:application/json" -H
# "Accept:application/json" http://localhost:8000/api/evento/47/aprobar
@app.route('/api/evento/<id>/<estado>', methods=['PUT'])
@csrf.exempt #es la excepcion de la "clave secreta"
def apiSetearEvento(id,estado):

    evento = db.session.query(Evento).get(id)
    evento.estado = estado
    actualizar_BD(evento)
    if estado == 1:
        enviarMail(evento.usuario.email, 'Evento a sido aprobado', 'aprobado', evento=evento)
    if estado == 0:
        enviarMail(evento.usuario.email, 'Evento a sido desaprobado', 'desaprobado', evento=evento)
    return jsonify(evento.to_json()), 201

# Eliminar evento
# curl -i -X DELETE -H "Accept: application/json" http://localhost:8000/api/evento/134
@app.route('/api/evento/<id>', methods=['DELETE'])
@csrf.exempt
def eliminarEvento(id):
    evento = db.session.query(Evento).get(id)
    eliminar_BD(evento)
    return '', 204	#el 204 es el tipo de http de borrado exitoso

# Ver Comentario por Id
# curl -i -H "Content-Type:application/json" -H "Accept: application/json" http://localhost:8000/api/comentario/136
@app.route('/api/comentario/<id>', methods=['GET'])
def apiGetComentarioById(id):
    comentario = db.session.query(Comentario).get(id)
    return jsonify(comentario.to_json())

# Listar comentarios por evento
# curl -i -H "Content-Type:application/json" -H "Accept: application/json" http://localhost:8000/api/comentarios/15
@app.route('/api/comentarios/<evento>', methods=['GET'])
def apiGetComentariosByEvento(evento):
    lista_comentarios = listar_comentarios(evento)
    return jsonify({'Comentarios': [comentario.to_json() for comentario in lista_comentarios]})

# Eliminar comentario
# curl -i -X DELETE -H "Accept: application/json" http://localhost:8000/api/comentario/134
@app.route('/api/comentario/<id>', methods=['DELETE'])
@csrf.exempt
def apiEliminarComentarioById(id):
    comentario = db.session.query(Comentario).get(id)
    eliminar_BD(comentario)
    return '', 204
