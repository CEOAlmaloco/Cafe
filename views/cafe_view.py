from os import system

class CafeView:
    def __init__(self):
        self.user_input = ">>> "

    def limpiar_pantalla(self):
        system('cls')

    def mostrar_menu_principal(self):
        print("   Starbucks - Menú   ")
        print("   Tu hot coffe aquí  ")
        print("")
        print("1. Agregar café       ")
        print("2. Codigo de descuento")
        print("3. Completar pedido   ")
        print("4. Salir del programa ")
        print("")
        print("¿Que desea hacer? (1/2/3/4)")
        return input(self.user_input)

    def mostrar_menu_cafes(self):
        print("  Starbucks - Cafés  ")
        print("  Tu hot coffe aquí  ")
        print("")
        print("1. Café Americano    ")
        print("2. Café con Leche    ")
        print("3. Té Negro          ")
        print("4. Chocolate Caliente")
        print("")
        print("¿Qué tipo de café desea? (1/2/3/4)")
        return input(self.user_input)

    def mostrar_tamanos(self, tipo_cafe, precios):
        print(f"    {tipo_cafe}    ")
        print("")
        print("")
        for tamano, precio in precios.items():
            print(f"{tamano}: ${precio}")
        print("")
        print("¿Qué tamaño desea? (1/2/3)")
        return input(self.user_input)

    def mostrar_codigo_descuento(self):
        print("    Codigo de descuento    ")
        print("")
        print("¿Desea ingresar un codigo de descuento? (Si/No)")
        return input(self.user_input)

    def mostrar_boleta(self, pedido):
        titulo = "BOLETA DE CAFÉ"
        print(titulo.center(50))
        print("")
        
        # Imprimir encabezados
        print("| ID | Tipo Café | Tamaño | Precio |")
        print("-" * 50)
        
        # Imprimir items
        for i in range(len(pedido["tipos"])):
            print(f"| {i+1} | {pedido['tipos'][i]} | {pedido['tamanos'][i]} | ${pedido['precios'][i]} |")
        
        print("-" * 50)
        print(f"Total: ${pedido['total']}")
        if pedido["codigo_descuento"]:
            print(f"Código de descuento aplicado: {pedido['codigo_descuento']}")

    def mostrar_mensaje(self, mensaje):
        print(mensaje)
        input("Presione Enter para continuar...")

    def confirmar_salida(self):
        print("¿Estás seguro? (Si/No)")
        return input(self.user_input).title()

    def confirmar_nuevo_pedido(self):
        print("¿Desea hacer otro pedido? (Si/No)")
        return input(self.user_input).title() 