# servidor_web.py

from flask import Flask, request, render_template_string
import sqlite3
import hashlib
import os

# Inicialización de Flask
app = Flask(__name__)

# Ruta de base de datos
DB_PATH = 'usuarios.db'

# Lista de usuarios válidos (nombres del grupo)
usuarios_validos = ["Kevin", "Juan", "Gerald"]

# Crear DB y tabla si no existen
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            nombre TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Guardar un usuario en la base de datos
def guardar_usuario(nombre, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO usuarios (nombre, password_hash) VALUES (?, ?)', (nombre, password_hash))
    conn.commit()
    conn.close()

# Validar usuario contra la base
def validar_usuario(nombre, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE nombre = ? AND password_hash = ?', (nombre, password_hash))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

# Plantilla HTML para el formulario
html_form = '''
<!doctype html>
<title>Login Examen</title>
<h2>Ingreso de usuario</h2>
<form method=post>
  Nombre: <input type=text name=nombre required><br>
  Contraseña: <input type=password name=clave required><br>
  <input type=submit value=Ingresar>
</form>
<p>{{ mensaje }}</p>
'''

# Ruta principal
@app.route('/', methods=['GET', 'POST'])
def login():
    mensaje = ''
    if request.method == 'POST':
        nombre = request.form['nombre']
        clave = request.form['clave']
        if validar_usuario(nombre, clave):
            mensaje = f'✅ Bienvenido, {nombre}!'
        else:
            mensaje = '❌ Usuario o contraseña incorrectos.'
    return render_template_string(html_form, mensaje=mensaje)

if __name__ == '__main__':
    init_db()
    # Solo una vez: agregar usuarios válidos con claves a elección
    for nombre in usuarios_validos:
        guardar_usuario(nombre, f"{nombre.lower()}123")  # ejemplo de clave
    print("Servidor web ejecutándose en http://localhost:5800")
    app.run(host='0.0.0.0', port=5800)
