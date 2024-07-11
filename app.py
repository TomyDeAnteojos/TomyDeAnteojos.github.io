from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from werkzeug.utils import secure_filename
import os
import time

app = Flask(__name__)
CORS(app)

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
        self.cursor.execute(sql, id)
        return self.cursor.fetchone()

    # MODIFICA UNA BICIS - MY_DESIGNS
    def updateBici(self, m, u, p, c, id):
        sql = "UPDATE bdBicis.bicicletas SET modelo = %s, usuario = %s, precio = %s, color = %s WHERE id = %s;"
        self.cursor.execute(sql, (m, u, p, c, id))
        self.conn.commit()
        return self.cursor.rowcount > 0

    # AGREGA UNA BICICLETA A LA BASE DE DATOS - CREATE_BIKE
    def insertBici(self, m, u, p, c):
        sql = "INSERT INTO bdBicis.bicicletas (modelo, usuario, precio, color) VALUES (%s, %s, %s, %s);"
        self.cursor.execute(sql, (m, u, p, c))
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def showBike(self):
        return self.id, self.modelo, self.usuario, self.precio, self.color

class Usuario:
    usuarios = []

    def __init__(self):
        self.id = -1
        self.nombre = ""
        self.psw = ""
        self.conn = mysql.connector.connect(host="127.0.0.1", user="root", password="root", database="bdBicis")
        self.cursor = self.conn.cursor(dictionary=True)

    def logear(self, n, p):
        sql = "SELECT * FROM bdBicis.usuarios WHERE nombre LIKE %s AND pass LIKE %s;"
        self.cursor.execute(sql, (n, p))
        return self.cursor.fetchone()
    
bicis = Bicicleta()

@app.route("/sites/catalogue", methods=["GET"])
def showAllBicis():
    b = bicis.selectAllBicis()
    return jsonify(b)

@app.route("/sites/my_designs/<int:id>", methods=["GET"])
def showBicis(id):
    b = bicis.selectBicisByUserId(id)
    return jsonify(b)

@app.route("/sites/create_bike/", methods=["POST"])
def insertBici():
    descripcion = request.form['descripcion']
    cantidad = request.form['cantidad']
    precio = request.form['precio']
    imagen = request.files['imagen']
    proveedor = request.form['proveedor'] 

if __name__ == "__main__":
    app.run(debug=True)
