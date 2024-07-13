from flask import Flask, request, jsonify, session, redirect, url_for
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = 'supersecretkey'  # Necesario para utilizar sesiones
app.config['SESSION_TYPE'] = 'filesystem'
class Bicicleta:
    bicis = []

    def __init__(self):
        self.id = -1
        self.modelo = ""
        self.usuario = ""
        self.precio = -1.0
        self.color = ""
        try:
            self.conn = mysql.connector.connect(host="localhost", user="root", password="root", database="bdBicis")
            self.cursor = self.conn.cursor(dictionary=True)
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
        
    # TRAE TODAS LAS BICIS - CATALOGUE
    def selectAllBicis(self):
        sql = "SELECT b.id, b.modelo, u.nombre AS usuario, b.precio, b.color FROM bdBicis.bicicletas b JOIN bdBicis.usuarios u ON b.usuario = u.id;"
        self.cursor.execute(sql)
        bicis = self.cursor.fetchall()
        return bicis

    # TRAE LAS BICIS DE UN USUARIO - MY_DESIGNS
    def selectBicisByUserId(self, id):
        sql = "SELECT b.id, b.modelo, u.nombre as usuario, b.precio, b.color FROM bdBicis.bicicletas b JOIN bdBicis.usuarios u ON b.usuario = u.id WHERE u.id = %s;"
        self.cursor.execute(sql, (id,))
        return self.cursor.fetchall()

    # MODIFICA UNA BICIS - MY_DESIGNS
    def updateBici(self, m, u, p, c, id):
        sql = "UPDATE bdBicis.bicicletas SET modelo = %s, usuario = %s, precio = %s, color = %s WHERE id = %s;"
        self.cursor.execute(sql, (m, u, p, c, id))
        self.conn.commit()
        return self.cursor.rowcount > 0

    # AGREGA UNA BICICLETA A LA BASE DE DATOS - CREATE_BIKE
# AGREGA UNA BICICLETA A LA BASE DE DATOS - CREATE_BIKE
    def insertBici(self, m, u, p, c):
        sql = "INSERT INTO bdBicis.bicicletas (modelo, usuario, precio, color) VALUES (%s, %s, %s, %s);"
        self.cursor.execute(sql, (m, u, p, c))
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    # BORRA UNA BICICLETA DE LA BASE DE DATOS - MY_DESIGNS
    def deleteBici(self, id):
        self.cursor.execute(f"DELETE FROM bdBicis.bicicletas WHERE id = {id}")
        self.conn.commit()
        return self.cursor.rowcount > 0

class Usuario:
    usuarios = []

    def __init__(self):
        self.id = -1
        self.nombre = ""
        self.psw = ""
        self.conn = mysql.connector.connect(host="127.0.0.1", user="root", password="root", database="bdBicis")
        self.cursor = self.conn.cursor(dictionary=True)

    def logear(self, n, p):
        sql = "SELECT * FROM bdBicis.usuarios WHERE nombre = %s AND pass = %s;"
        self.cursor.execute(sql, (n, p))
        return self.cursor.fetchone()


# -------------------------------- BICICLETAS -------------------------------- #
bicis = Bicicleta()
 # Selecciona todas las bicis - CATALOGUE
@app.route("/bicicletas", methods=["GET"])
def showAllBicis():
    b = bicis.selectAllBicis()
    return jsonify(b)

 # Selecciona todas las bicis - MY_DESIGNS
@app.route("/bicicletas/usuarios/<int:id>", methods=["GET"])
def showBicis(id):
    b = bicis.selectBicisByUserId(id)
    return jsonify(b)

# Inserta una bici creada por un usuario - CREATE_BIKE
@app.route("/bicicletas/agregar", methods=["POST"])
def insertBici():
    modelo = request.form['modelo']
    usuario = request.form['usuario']
    precio = request.form['precio']
    color = request.form['color']

    print(f"Modelo: {modelo}, Usuario: {usuario}, Precio: {precio}, Color: {color}")


    b = bicis.insertBici(modelo, usuario, precio, color)
    if b:
        return jsonify({"mensaje": "Bici agregada"}), 201
    else:
        return jsonify({"mensaje": "Error al agregar la bici"}), 500


 # Eliminar una bici de un usuario en especifico - MY_DESIGNS
@app.route("/bicicletas/eliminar/<int:id>", methods=["DELETE"])
def delete(id):
    b = bicis.deleteBici(id)
    if b:
        return jsonify({"mensaje": "Bici eliminada"}), 200
    else:
        return jsonify({"mensaje": "Error al eliminar la bici"}), 500

 # Modifica una bici de un usuario en especifico - MY_DESIGNS
@app.route("/bicicletas/modificar/<int:id>", methods=["PUT"])
def modificarBici(id):
    data = request.json

    modelo = data.get('modelo')
    usuario = data.get('usuario')
    precio = data.get('precio')
    color = data.get('color')

    if bicis.updateBici(modelo, usuario, precio, color, id):
        return jsonify({"mensaje": "Bici modificada"}), 200
    else:
        return jsonify({"mensaje": "hubo un error al modificar la bici"}), 403


# -------------------------------- USUARIO -------------------------------- #
bicis = Bicicleta()

# Ruta para el login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    usuario = data.get('username')
    contrasena = data.get('password')

    user_instance = Usuario()
    user_data = user_instance.logear(usuario, contrasena)
    
    if user_data:
        session['usuario'] = user_data
        session['user_id'] = user_data['id']

       # print(session['user_id'])
        return jsonify({"mensaje": "Usuario logeado"}), 200
    else:
        return jsonify({"mensaje": "hubo un error al logear usuario"}), 403

# Implementación de las rutas para Bicicletas...

if __name__ == "__main__":
    app.run(debug=True)