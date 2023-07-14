from datetime import date
import json
from flask import Flask,request
from flask_cors import CORS
app = Flask(__name__)

CORS(app)

class Pago:
    def __init__(self,Numero,Fecha,Valor):
        self.Numero = Numero
        self.Fecha = Fecha
        self.Valor = Valor

class Cuenta:
    def __init__(self,numero,nombre,saldo,contactos):
        self.nombre = nombre
        self.numero = numero
        self.saldo = saldo
        self.contactos = contactos
        self.pagos_enviados = []
        self.pagos_recibidos = []
    def get_contactos(self):
        return self.contactos

class BD:
    def __init__(self):
        self.cuentas = []
    def agregar_cuenta(self,nueva_cuenta):
        self.cuentas.append(nueva_cuenta)
    def get_cuentas(self):
        return self.cuentas
    def get_cuenta(self,numero):
        for i in self.cuentas:
            if i.numero == numero:
                return i
        return "error"
    def get_cuenta_contactos(self,numero):
        finded = False
        for i in self.cuentas:
            if i.numero == numero:
                contactos = i.get_contactos()
                finded = True
        if finded == False:
            return {
                    "status":"error"
            }
        for i in contactos:
            for j in self.cuentas:
                if j.numero == i:
                    response[i] = j.nombre 
        return {
            "status":"successfull",
            "response":json.dumps(response)
        }

    def pagar_cuenta(self,emisor,receptor,valor):
        user_emisor = self.get_cuenta(emisor)
        if user_emisor == "error":
            return {
                    "status":"error"
                }
        contactos_emisor = user_emisor.get_contactos()
        permission = False
        for i in contactos_emisor:
            if receptor == i:
                permission = True
        if permission:
            user_receptor = self.get_cuenta(receptor)
            if user_receptor == "error":
                return {
                    "status":"error"
                }
            elif user_emisor.saldo >= valor:
                Fecha = str(date.today())
                user_emisor.saldo -= valor
                user_receptor.saldo +=valor
                pago_enviado = Pago(receptor,Fecha,valor)
                pago_recibido = Pago(emisor,Fecha,valor)
                user_emisor.pagos_enviados.append(pago_enviado)
                user_receptor.pagos_recibidos.append(pago_recibido)
                response = {"Fecha":Fecha}
                return json.dumps(response)
        else:
            return {
                    "status":"error"
                }
    def get_historial(self,numero):
        user = self.get_cuenta(numero)
        if user == "error":
            return {
                "status": "error"
            }
        response = {}
        response["Saldo"] = user.saldo
        operaciones = []
        for i in user.pagos_recibidos:
            nombre = ""
            for j in self.cuentas:
                if j.numero == i.Numero:
                    nombre = j.nombre
            result = "Pago recibido de "+ str(i.Valor) + " de " + nombre
            operaciones.append(result)
        for i in user.pagos_enviados:
            nombre = ""
            for j in self.cuentas:
                if j.numero == i.Numero:
                    nombre = j.nombre
            result = "Pago realizado de "+ str(i.Valor) + " a " + nombre
            operaciones.append(result)
        response["Operaciones"] = operaciones
        return {
            "status":"successfull",
            "response":json.dumps(response)
        }
database = BD()
database.agregar_cuenta(Cuenta("21345","Arnaldo",200,["123","456"]))
database.agregar_cuenta(Cuenta("123","Luisa",400,["456"]))
database.agregar_cuenta(Cuenta("456","Andrea",300,["21345"]))

"""
print(database.get_cuenta_contactos("21345"))
print("-------------------------------")
print(database.pagar_cuenta("21345","123",100))
print(database.pagar_cuenta("123","456",50))
print("-------------------------------")
print(database.get_historial("123"))
"""

@app.route("/billetera/contactos", methods=["GET"])
def get_cuenta_contactos():
    args = request.args.to_dict()
    return database.get_cuenta_contactos(args["minumero"])

@app.route("/billetera/pagar",methods=["GET"])
def pagar_cuenta():
    args = request.args.to_dict()
    return database.pagar_cuenta(args["minumero"],args["numerodestino"],int(args["valor"]))

@app.route("/billetera/historial",methods=["GET"])
def get_historial():
    args = request.args.to_dict()
    return database.get_historial(args["minumero"])

def test_get_cuenta(numero):
    return database.get_cuenta_contactos(numero)

def test_pagar_cuenta(numero,numerodestino,valor):
    return database.pagar_cuenta(numero,numerodestino,valor)

def test_get_historial(numero):
    return database.get_historial(numero)

if __name__ == "__main__":
    app.run(debug=True)
