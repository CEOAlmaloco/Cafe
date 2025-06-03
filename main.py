from controllers.cafe_controller import CafeController
from views.cafe_view import CafeView

def main():
    controlador = CafeController()
    vista = CafeView()

    while True:
        try:
            vista.limpiar_pantalla()
            opcion = vista.mostrar_menu_principal()

            if opcion == "1":
                vista.limpiar_pantalla()
                tipo_cafe = vista.mostrar_menu_cafes()
                
                if tipo_cafe in ["1", "2", "3", "4"]:
                    tipo_cafe = int(tipo_cafe)
                    tipo = controlador.modelo.obtener_tipo_cafe(tipo_cafe)
                    
                    if tipo:
                        vista.limpiar_pantalla()
                        tamano = vista.mostrar_tamanos(tipo["nombre"], tipo["precios"])
                        
                        if tamano in ["1", "2", "3"]:
                            tamano = int(tamano)
                            if controlador.agregar_cafe(tipo_cafe, tamano):
                                vista.mostrar_mensaje("Café agregado exitosamente")
                            else:
                                vista.mostrar_mensaje("Error al agregar el café")
                        else:
                            vista.mostrar_mensaje("Opción de tamaño inválida")
                    else:
                        vista.mostrar_mensaje("Tipo de café inválido")
                else:
                    vista.mostrar_mensaje("Opción inválida")

            elif opcion == "2":
                if controlador.pedido["total"] == 0:
                    vista.mostrar_mensaje("No ha agregado ningún café a su pedido")
                    continue

                respuesta = vista.mostrar_codigo_descuento()
                if respuesta.upper() in ["SI", "S"]:
                    codigo = input("Ingrese el código de descuento: ")
                    if controlador.aplicar_codigo_descuento(codigo):
                        vista.mostrar_mensaje("Código de descuento aplicado exitosamente")
                    else:
                        vista.mostrar_mensaje("Código de descuento inválido")

            elif opcion == "3":
                if controlador.pedido["total"] == 0:
                    vista.mostrar_mensaje("No ha agregado ningún café a su pedido")
                    continue

                vista.limpiar_pantalla()
                vista.mostrar_boleta(controlador.obtener_pedido())
                vista.mostrar_mensaje("")

                respuesta = vista.confirmar_nuevo_pedido()
                if respuesta.upper() in ["SI", "S"]:
                    controlador.reiniciar_pedido()
                else:
                    break

            elif opcion == "4":
                respuesta = vista.confirmar_salida()
                if respuesta.upper() in ["SI", "S"]:
                    break

            else:
                vista.mostrar_mensaje("Opción inválida")

        except ValueError:
            vista.mostrar_mensaje("Por favor, ingrese un valor válido")
        except KeyboardInterrupt:
            break

    vista.limpiar_pantalla()
    print("¡Gracias por su visita!")

if __name__ == "__main__":
    main() 