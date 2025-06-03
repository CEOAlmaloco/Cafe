from models.cafe import Cafe

class CafeController:
    def __init__(self):
        self.pedido = {
            "items": [],
            "total": 0,
            "codigoDescuento": None
        }
        
        # Mapeo de tipos de café
        self.tipos_cafe = {
            "Café Americano": {"id": 1, "precios": {"pequeño": 1200, "mediano": 1500, "grande": 1800}},
            "Café con Leche": {"id": 2, "precios": {"pequeño": 1300, "mediano": 1600, "grande": 1900}},
            "Té Negro": {"id": 3, "precios": {"pequeño": 1000, "mediano": 1300, "grande": 1600}},
            "Chocolate Caliente": {"id": 4, "precios": {"pequeño": 1400, "mediano": 1700, "grande": 2000}}
        }
        
        # Códigos de descuento válidos
        self.codigos_descuento = ["NEXUS10", "PREMIUM", "COFFEE2024"]

    def agregar_cafe(self, tipo: str, tamano: str) -> bool:
        try:
            if tipo not in self.tipos_cafe:
                return False
                
            precio = self.tipos_cafe[tipo]["precios"][tamano]
            
            # Buscar si ya existe el mismo producto
            item_existente = next(
                (item for item in self.pedido["items"] 
                 if item["tipo"] == tipo and item["tamano"] == tamano),
                None
            )
            
            if item_existente:
                item_existente["cantidad"] += 1
                item_existente["precioTotal"] = item_existente["precio"] * item_existente["cantidad"]
            else:
                self.pedido["items"].append({
                    "tipo": tipo,
                    "tamano": tamano,
                    "precio": precio,
                    "cantidad": 1,
                    "precioTotal": precio
                })
            
            self.calcular_total()
            return True
            
        except Exception:
            return False

    def aplicar_codigo_descuento(self, codigo: str) -> bool:
        if codigo in self.codigos_descuento:
            self.pedido["codigoDescuento"] = codigo
            self.calcular_total()
            return True
        return False

    def calcular_total(self):
        subtotal = sum(item["precioTotal"] for item in self.pedido["items"])
        if self.pedido["codigoDescuento"]:
            self.pedido["total"] = int(subtotal * 0.9)  # 10% de descuento
        else:
            self.pedido["total"] = subtotal

    def obtener_pedido(self):
        return self.pedido

    def reiniciar_pedido(self):
        self.pedido = {
            "items": [],
            "total": 0,
            "codigoDescuento": None
        } 