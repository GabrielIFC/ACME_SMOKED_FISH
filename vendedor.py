from db import get_database
from autorización_usuarios import get_current_user

# Conexión a la base de datos
db = get_database()
pedidos_col = db["pedidos"]
stock_col = db["stock"]

def vender_salmón():
    if get_current_user() is None or get_current_user()['rol'] not in ['vendedor', 'administrador']:
     print(" Solo los vendedores o administradores pueden realizar ventas.")
     return

    print("\n Venta de Salmón")
    print("Tipos de salmón disponibles:")
    print("1. Atlántico - $5000 por kilo")
    print("2. Nórdico - $7000 por kilo")
    print("3. Pacífico - $3000 por kilo")

    salmones = {
        "Atlántico": 5000,
        "Nórdico": 7000,
        "Pacífico": 3000
    }

    opciones = {"1": "Atlántico", "2": "Nórdico", "3": "Pacífico"}

    pedido = []
    tipos_vendidos = set()

    while len(pedido) < 3:
        opcion = input("\nSeleccione el tipo de salmón:\n1. Atlántico\n2. Nórdico\n3. Pacífico\nIngrese número (o 'salir' para terminar): ")
        if opcion.lower() == 'salir':
            break
        tipo = opciones.get(opcion)
        if not tipo:
            print(" Opción inválida.")
            continue
        if tipo in tipos_vendidos:
            print(f" Ya has vendido el tipo de salmón {tipo} en esta venta. Por favor, elige otro tipo.")
            continue

        try:
            cantidad = float(input(f"Ingrese la cantidad de {tipo} (en kilos): "))
            if cantidad <= 0:
                print(" La cantidad debe ser mayor a cero.")
                continue
        except ValueError:
            print(" Entrada inválida. Ingrese un número.")
            continue

        # Verificar stock disponible
        stock = stock_col.find_one({"tipo": tipo})
        if not stock or stock["stock_kilos"] < cantidad:
            disponible = stock["stock_kilos"] if stock else 0
            print(f" No hay suficiente stock de {tipo}. Disponible: {disponible} kg.")
            continue

        # Descontar del stock
        stock_col.update_one(
            {"tipo": tipo},
            {"$inc": {"stock_kilos": -cantidad}}
        )

        pedido.append({"tipo": tipo, "cantidad": cantidad, "precio": salmones[tipo]})
        tipos_vendidos.add(tipo)

    if not pedido:
        print(" No se realizó ninguna venta.")
        return

    total = sum([item['cantidad'] * item['precio'] for item in pedido])
    nuevo_pedido = {
        "usuario": get_current_user()['nombre'],
        "detalle": pedido,
        "total": total
    }
    pedidos_col.insert_one(nuevo_pedido)

    print(f"\n Venta registrada con éxito. Total: ${total}")

    # Mostrar stock actualizado
    print("\n Stock actualizado:")
    for doc in stock_col.find():
        print(f"{doc['tipo']}: {doc['stock_kilos']} kg disponibles")
