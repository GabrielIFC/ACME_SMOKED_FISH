# administrador.py
from db import get_database
from autorización_usuarios import get_current_user

db = get_database()
stock_col = db["stock"]
pedidos_col = db["pedidos"]

def ver_reportes():
    if get_current_user() is None or get_current_user()['rol'] != 'administrador':
        print("❌ Solo los administradores pueden ver los reportes.")
        return

    # Obtener los pedidos y calcular las ganancias
    pedidos = list(pedidos_col.find())
    ganancias = {"Atlántico": 0, "Nórdico": 0, "Pacífico": 0}
    total_general = 0

    for pedido in pedidos:
        for item in pedido['detalle']:
            tipo = item['tipo']
            cantidad = item['cantidad']
            precio = item['precio']
            ganancias[tipo] += cantidad * precio
            total_general += cantidad * precio

    # Mostrar ganancias por tipo de salmón
    print("\n📊 Reporte de Ganancias:")
    for tipo, ganancia in ganancias.items():
        print(f"{tipo}: ${ganancia:.2f}")

    print(f"\n🔹 Total General de Ganancias: ${total_general:.2f}")


def modificar_stock():
    if get_current_user() is None or get_current_user()['rol'] != 'administrador':
        print("❌ Solo los administradores pueden modificar el stock.")
        return

    print("\n📦 Modificar Stock de Salmón")
    print("Tipos de salmón disponibles:")
    print("1. Atlántico")
    print("2. Nórdico")
    print("3. Pacífico")

    salmones = ["Atlántico", "Nórdico", "Pacífico"]
    tipo_salmón = input("Seleccione el tipo de salmón a modificar (Atlántico, Nórdico, Pacífico): ").capitalize()

    if tipo_salmón not in salmones:
        print(" Tipo de salmón inválido.")
        return

    nuevo_stock = float(input(f"Ingrese el nuevo stock para {tipo_salmón} (en kilos): "))
    if nuevo_stock < 0:
        print(" El stock no puede ser negativo.")
        return

    # Actualizar el stock en la base de datos

    stock_col.update_one({"tipo": tipo_salmón}, {"$inc": {"stock_kilos": nuevo_stock}})
    print(f" El stock de {tipo_salmón} ha sido actualizado a {nuevo_stock} kilos.")

