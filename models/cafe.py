class Cafe:
    def __init__(self):
        self.tipos_cafe = {
            1: {"nombre": "Café Americano", "precios": {"pequeño": 1200, "mediano": 1500, "grande": 1800}},
            2: {"nombre": "Café con Leche", "precios": {"pequeño": 1300, "mediano": 1600, "grande": 1900}},
            3: {"nombre": "Té Negro", "precios": {"pequeño": 1000, "mediano": 1300, "grande": 1600}},
            4: {"nombre": "Chocolate Caliente", "precios": {"pequeño": 1400, "mediano": 1700, "grande": 2000}}
        }
        self.tamanos = {
            1: "pequeño",
            2: "mediano",
            3: "grande"
        }
        self.codigo_descuento = "CAFELIFE"
        self.descuento = 0.10  # 10% de descuento

    def obtener_tipo_cafe(self, opcion):
        return self.tipos_cafe.get(opcion)

    def obtener_tamano(self, opcion):
        return self.tamanos.get(opcion)

    def calcular_precio(self, tipo_cafe, tamano):
        if tipo_cafe and tamano:
            tipo = self.tipos_cafe[tipo_cafe]
            tamano_nombre = self.tamanos[tamano]
            return tipo["precios"][tamano_nombre]
        return 0

    def validar_codigo_descuento(self, codigo):
        return codigo.upper() == self.codigo_descuento

    def aplicar_descuento(self, total):
        return round(total * (1 - self.descuento)) 