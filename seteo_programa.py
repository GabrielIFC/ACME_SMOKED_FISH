# Este bloque de programa nos permite : 
# - La creación de los usuarios que necesitamos (vendedor y administrador)
# - Ejecuta el stock inicial de los salmones
# - Crea las colecciones en nuestra base de datos (usuarios y stock)

# Al ejecutar este bloque, veremos reflejado en MongoDb la base de datos llamada acme_smoked_fish
# y sus dos colecciones correspondientes.

# Este bloque no permite una reinserción , por lo que de manera única, se puede agregar el stock y los usuarios definidos.

# Después solo el administrador puede modificar el stock a su voluntad, previa contraseña validada.

import bcrypt
from db import get_database

db = get_database()
usuarios_col = db["usuarios"]
stock_col = db["stock"]

def crear_usuarios():
    if usuarios_col.count_documents({}) == 0:
        
        usuarios = [
            {
                "nombre": "Gabriel Fuentes",
                "rol": "vendedor",
                "password": bcrypt.hashpw("1234".encode(), bcrypt.gensalt())
            },
            {
                "nombre": "Ricardo Gutierrez",
                "rol": "administrador",
                "password": bcrypt.hashpw("admin".encode(), bcrypt.gensalt())
            }
        ]
        usuarios_col.insert_many(usuarios)
        print("Usuarios creados.")
    else:
        print("ℹ Los usuarios ya existen.")

def crear_stock():
    if stock_col.count_documents({}) == 0:
        
        salmones = [
            {"tipo": "Atlántico", "precio_venta": 5000, "costo": 3000, "stock_kilos": 100},
            {"tipo": "Nórdico", "precio_venta": 7000, "costo": 4500, "stock_kilos": 100},
            {"tipo": "Pacífico", "precio_venta": 3000, "costo": 1500, "stock_kilos": 100}
        ]
        stock_col.insert_many(salmones)
        print("Stock inicial creado.")
    else:
        print("ℹ El stock ya está configurado.")

if __name__ == "__main__":
    crear_usuarios()
    crear_stock()
