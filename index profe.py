from flask import Flask
from flask import render_template #Permite importar templates
from flask_wtf import CSRFProtect #importar para proteccion CSRF
from flask import flash #importar para mostrar mensajes flash
from flask import redirect, url_for #importar para permitir redireccionar y generar url
from formulario_registro import Registro #importar clase de formulario
from formulario_login import Login #importar clase de formulario
import datetime #importar funciones de fecha
from werkzeug.utils import secure_filename #Importa seguridad nombre de archivo
import os.path #importar para funciones de sistema

#Para este ejemplo también instalé WTForms-Compents
# pip install WTForms-Compents


app = Flask(__name__) #Iniciar Flask
csrf = CSRFProtect(app) #Iniciar protección CSRF
app.secret_key = 'esta_es_la_clave_secreta' #clave secreta

#Función que muestra los datos obtenidos del envío de formulario
def mostrar_datos(formulario):
    print(formulario.nombre.data)
    print(formulario.apellido.data)
    print(formulario.fechaNac.data)
    print(formulario.hora.data)
    print(formulario.bio.data)
    print(formulario.usuario.data)
    print(formulario.password.data)
    print(formulario.opciones.data)

#Cargar página principal
@app.route('/')
def index():
    formularioLogin = Login() #Instanciar formulario de Login
    return render_template('index.html',  formularioLogin = formularioLogin)

#Función que procesa el Login
# Solo acepta método POST ya que no debe poder ingresar a la ruta desde la url·
@app.route('/login', methods=["POST"])
def login():
    formularioLogin = Login() #Instanciar formulario de Login
    if formularioLogin.validate_on_submit(): #Si el formulario ha sido enviado y es validado correctamente
        print(formularioLogin.email.data)
        print(formularioLogin.password.data)
        #Verifica que el usuario y pass sean correctos
        if formularioLogin.email.data == "admin@mail.com" and formularioLogin.password.data == "12345":
            flash('Login realizado correctamente','success') #Mostrar mensaje
        else:
            flash('Login incorrecto','danger') #Mostrar mensaje de error
        return redirect(url_for('index')) #Redirecciona a la página principal
    return render_template('index.html',  formularioLogin = formularioLogin)


#Función Insertar
#Si obtiene datos por POST muestra los datos por consola y redirecciona mostrando un mensajes
#Si no obtiene datos muestra el formulario
@app.route('/insertar', methods=["POST","GET"])
def insertar():
    formularioLogin = Login() #Instanciar formulario de Login

    formulario = Registro() #Instanciar formulario de registro
    if formulario.validate_on_submit(): #Si el formulario ha sido enviado y es validado correctamente
        f = formulario.imagen.data #Obtener imagen
        filename = secure_filename(f.filename) #Modifica el nombre del archivo a uno seguro
        f.save(os.path.join('static/img/', filename)) #Guardar imagen en sistema
        flash('Usuario registrado exitosamente','success') #Mostrar mensaje
        mostrar_datos(formulario)  #Redirecciona a la función actualizar
        return redirect(url_for('insertar')) #Redirecciona a la función insertar
    return render_template('registro_form.html', formulario = formulario, formularioLogin = formularioLogin, destino = "insertar")#Muestra el formulario


#Función Actualizar
#Si obtiene datos por POST muestra los datos por consola y redirecciona mostrando un mensajes
#Si no obtiene datos carga valores de prueba al formulario y lo muestra
@app.route('/actualizar', methods=["POST","GET"])
def actualizar():

    formularioLogin = Login() #Instanciar formulario de Login

   #Clase con los valores por defecto que se actualizaran
   #En una aplicación completa estos valores se obtendrian de la db
    class Persona:
        nombre= 'Nombre'
        apellido= 'Apellido'
        email= 'Email@email.com'
        bio= 'Estoe s una bio'
        usuario= 'usuario'
        fechaNac = datetime.datetime.strptime('2019-05-16', "%Y-%m-%d").date()
        hora =  datetime.datetime.strptime('11:25 PM', "%I:%M %p").time()
        imagen = "usuario.png"
        sexo = "f"
        opciones = 3


    #Cargar valores a formulario
    formulario = Registro(obj=Persona)

    #Otro caso de valores por defecto solamente que en forma de diccionario en vez de objeto
     #registro ={
        #'nombre': 'Nombre',
        #'apellido': 'Apellido',
        #'email': 'Email@email.com',
        #'bio': 'Estoe s una bio',
        #'usuario': 'usuario'
    #}
    #formulario = Registro(data=registro)

    #Setea la imagen y la password como opcionales ya que no se permite modificarlas
    Registro.opcional(formulario.imagen)
    Registro.opcional(formulario.password)


    if  formulario.validate_on_submit():#Si el formulario es validado correctamente
        flash('Usuario actualizado exitosamente','success') #Mostrar mensaje
        mostrar_datos(formulario) #Mostrar datos obtenido por consola
        return redirect(url_for('actualizar'))  #Redirecciona a la función actualizar
    return render_template('registro_form.html', formulario = formulario , destino = "actualizar",  formularioLogin = formularioLogin)#Muestra el formulario

if __name__ == '__main__': #Asegura que solo se ejectue el servidor cuando se ejecute el script directamente
    app.run(port = 8000, debug = True)
