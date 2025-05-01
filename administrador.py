# administrador.py
from db import get_database
from autorización_usuarios import get_current_user

db = get_database()
stock_col = db["stock"]
pedidos_col = db["pedidos"]

def ver_reportes():
    if get_current_user() is None or get_current_user()['rol'] != 'administrador':
        print(" Solo los administradores pueden ver los reportes.")
        return

    pedidos = list(pedidos_col.find())

    print("\n Reporte Detallado de Pedidos:\n")

    for idx, pedido in enumerate(pedidos, start=1):
        print(f"Pedido #{idx}")
        print(f"Usuario: {pedido['usuario']}")
        total_venta = 0
        total_costo = 0
        detalle_por_salmón = {}

        for item in pedido['detalle']:
            tipo = item['tipo']
            cantidad = item['cantidad']

            # Obtener info actual del tipo de salmón desde la base de datos
            info_salmón = stock_col.find_one({"tipo": tipo})
            if not info_salmón:
                print(f"  No se encontró información de stock para {tipo}.")
                continue

            precio_venta = info_salmón.get("precio_venta", 0)
            costo = info_salmón.get("costo", 0)

            total_venta += cantidad * precio_venta
            total_costo += cantidad * costo

            # Acumular detalle por tipo de salmón
            if tipo not in detalle_por_salmón:
                detalle_por_salmón[tipo] = 0
            detalle_por_salmón[tipo] += cantidad

        ganancia = total_venta - total_costo

        # Mostrar detalle del pedido
        for tipo, cantidad in detalle_por_salmón.items():
            print(f" - {tipo}: {cantidad} kg vendidos")

        print(f" Total de venta del pedido: ${total_venta:.2f}")
        print(f" Costo bruto total del pedido: ${total_costo:.2f}")
        print(f" Ganancia líquida del pedido: ${ganancia:.2f}\n")

def modificar_stock():
    if get_current_user() is None or get_current_user()['rol'] != 'administrador':
        print(" Solo los administradores pueden modificar el stock.")
        return

    print("\n Modificar Stock de Salmón")
    print("Tipos de salmón disponibles:")
    print("1. Atlántico")
    print("2. Nórdico")
    print("3. Pacífico")

    opciones = {"1": "Atlántico", "2": "Nórdico", "3": "Pacífico"}
    seleccion = input("Seleccione el número del tipo de salmón a modificar (1, 2, 3): ")
    tipo_salmón = opciones.get(seleccion)

    if not tipo_salmón:
        print(" Tipo de salmón inválido.")
        return

    # Mostrar stock actual
    stock_actual = stock_col.find_one({"tipo": tipo_salmón})
    if stock_actual:
        print(f" Stock actual de {tipo_salmón}: {stock_actual['stock_kilos']} kg")
    else:
        print(f" No se encontró stock para el tipo {tipo_salmón}.")
        return

    try:
        nuevo_stock = float(input(f"Ingrese el nuevo stock para {tipo_salmón} (en kilos): "))
        if nuevo_stock < 0:
            print(" El stock no puede ser negativo.")
            return
    except ValueError:
        print(" Entrada inválida. Ingrese un número.")
        return
    
    # Actualizar el stock en la base de datos

    stock_col.update_one({"tipo": tipo_salmón}, {"$inc": {"stock_kilos": nuevo_stock}})
    print(f" El stock de {tipo_salmón} ha sido actualizado a {stock_actual['stock_kilos'] + nuevo_stock} kilos.")