# auth.py

import bcrypt
from db import get_database

db = get_database()
usuarios_col = db["usuarios"]
usuario_actual = None

def login():
    global usuario_actual
    nombre = input(" Nombre de usuario: ").strip()
    password = input(" Contraseña: ").strip()

    usuario = usuarios_col.find_one({"nombre": nombre})

    if usuario and bcrypt.checkpw(password.encode(), usuario["password"]):
        usuario_actual = usuario
        return usuario
    else:
        print(" Nombre de usuario o contraseña incorrectos.")
        return None

def logout():
    global usuario_actual
    if usuario_actual:
        print(f"\n Cerrando sesión de {usuario_actual['nombre']}")
        usuario_actual = None

def get_current_user():
    return usuario_actual
