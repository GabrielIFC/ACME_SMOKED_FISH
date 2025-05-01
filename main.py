# La ejecución de este bloque nos permite iniciar nuestro menú principal y hacer login
# para poder interactuar con el programa.


from autorización_usuarios import login, logout, get_current_user
from vendedor import vender_salmón
from administrador import ver_reportes, modificar_stock

def menu_principal():
    user = get_current_user()
    if user is None:
        print(" Debes iniciar sesión para acceder al sistema.")
        return

    print(f"\nBienvenido, {user['nombre']}!")
    if user['rol'] == 'vendedor':
        menu_vendedor()
    elif user['rol'] == 'administrador':
        menu_administrador()

def menu_vendedor():
    while True:
        print("\nMenú Vendedor")
        print("1. Realizar venta de salmón")
        print("2. Cerrar sesión")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            vender_salmón()
        elif opcion == '2':
            logout()
            print(" Cerrando sesión.")
            break
        else:
            print(" Opción no válida.")

def menu_administrador():
    while True:
        print("\nMenú Administrador")
        print("1. Ver reportes de ganancias")
        print("2. Modificar stock de salmón")
        print("3. Vender salmón")
        print("4. Cerrar sesión")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            ver_reportes()
        elif opcion == '2':
            modificar_stock()
        elif opcion == '3':
            vender_salmón()
        elif opcion == '4':
            logout()
            print(" Cerrando sesión.")
            break
        else:
            print(" Opción no válida.")

if __name__ == "__main__":
    while True:
        print("\n--- Menú Principal ---")
        print("1. Iniciar sesión")
        print("2. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            login()
            menu_principal()
        elif opcion == '2':
            print(" Saliendo del sistema.")
            break
        else:
            print(" Opción no válida.")
