from flask import Flask, jsonify, request
from flask_cors import CORS
import serial
import threading
import time

app = Flask(__name__)
CORS(app)

contador = 0
historial = []

arduino = serial.Serial('COM5', 9600)
time.sleep(2)

def leer_serial():
    global contador, historial
    while True:
        try:
            dato = arduino.readline().decode('utf-8').strip()
            if dato == "ADD":
                contador += 1
                historial.append(f"Producto agregado - Total: {contador}")
        except:
            pass

threading.Thread(target=leer_serial, daemon=True).start()

# 📊 obtener datos
@app.route('/data')
def data():
    return jsonify({
        "total": contador,
        "historial": historial[-10:]  # últimos 10
    })

# ➕ sumar manual
@app.route('/add', methods=['POST'])
def add():
    global contador, historial
    contador += 1
    historial.append(f"Agregado manual - Total: {contador}")
    return jsonify({"ok": True})

# ➖ restar manual
@app.route('/remove', methods=['POST'])
def remove():
    global contador, historial
    if contador > 0:
        contador -= 1
        historial.append(f"Removido manual - Total: {contador}")
    return jsonify({"ok": True})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)