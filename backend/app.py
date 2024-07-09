import flask
import mysql.connector

def showQuery(cs):
    for i in cs:
        print(i)

def login(cs):
    QUERY = "SELECT * FROM usuarios"
    cs.execute(QUERY)
    showQuery(cs)

def showBicis(cs):
    QUERY = "SELECT b.id AS id, m.modelo AS modelo, u.nombre AS usuario, b.precio AS precio, b.color AS color FROM bicicletas b JOIN modelos m ON b.modelo = m.id JOIN usuarios u ON b.usuario = u.id;"
    cs.execute(QUERY)
    showQuery(cs)

def insertBici(cs, bd, values):
    QUERY = "INSERT INTO bicicletas (modelo, usuario, precio, color) VALUES (%s, %s, %s, %s);"
    cs.execute(QUERY,values)
    if cs.rowcount > 0:
        bd.commit()
    showQuery(cs)

def deleteBici(cs,bd, id):
    QUERY = "DELETE FROM bicicletas WHERE id = %s;"
    cs.execute(QUERY,id)
    bd.commit()
    showQuery(cs)


app = Flask(__name__)
mybd = mysql.connector.connect( host="localhost", user="root", password="root", database="bdBicis")

if __name__ == '__name__':
    app.run()

cs = mybd.cursor()


showQuery(cs)
