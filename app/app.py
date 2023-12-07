#!/usr/bin/python3
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Conexion MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
# database_name tiene que ser el nombre de la base de datos a la cual nos queremos conectar.
app.config['MYSQL_DB'] = 'database_name'

# Crear vinculo entre mi aplicacion y la conexion con MYSQL que vamos a crear
conexion = MySQL(app)

# Before request nos permite relizar acciones antes de la peticion
@app.before_request
def before_request():
    #Cualquier tipo de operacion nescesaria se puede realizar en este bloque.
    print("Antes de la peticion")


# After request nos permite realizar acciones despues de la peticion

@app.after_request
def after_request(response):
#Cualquier tipo de operacion nescesaria se puede realizar en este bloque.
    print("Despues de la peticion")
    return response

#   Si a route le pasamos solamente un / inidicamos a esta que va a ser la ruta raiz
@app.route('/')
# Definiendo index debajo de la ruta raiz lo que se consigue es enlazar el return a la ruta
# En este caso se esta enlazando un archivo html para que sea mostrado en el navegador.
def index():
    return render_template('index.html')

# Se pueden crear urls dinamicas, es decir con parametros cambiantes. Por cada parametro que se le provea
# se creara una url valida.
# Este metodo sirve para la creacion de urls a traves del paso de parametros en el navegador, ahorra el paso de crear
# una url nueva cada vez que se nescesite. 
@app.route('/contacto/<nombre>')
def contacto(nombre):
    data = {
        "titulo": 'Contacto',
        "Nombre": nombre
    }
    return render_template('contacto.html', data=data)

# QUERY STRINGS- Pasarle a una url una serie de parametros que puyeden ser variables.
def query_string():
    print(request)
    print(request.args)
    print(request.args.get('param1'))
    print(request.args.get('param2'))
    return "OK"

# Queries de sql atraves de una url
@app.route('/cursos')
def listar_cursos():
    data = {}
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM state"
        cursor.execute(sql)
        states = cursor.fetchall()
        data['mensaje'] = 'Exito' 
    except Exception as ex:
        data['mensaje'] = 'Error'
    return jsonify(data)


def pagina_no_encontrada(error):
   
   # Se puede cambiar el mensaje de error que tira al encontrar una url no valida y cargar otro archivo
   # html para mostrar un mensaje de error personalizado

   # return render_template('404.html'), 404

   # Redirect permite redireccionar al usuario en caso de que este acceda a una url no valida
   # hacia la url que nosotros especifiquemos en este caso index que viene a ser la ruta raiz de la web
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.add_url_rule('/query_string', view_func=query_string)
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True,port=5000)
