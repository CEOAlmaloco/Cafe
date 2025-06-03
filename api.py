from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from models.schemas import CafeBase, CodigoDescuento, RespuestaPedido, Pedido, Menu
from controllers.cafe_controller import CafeController
import os
from dotenv import load_dotenv
import stripe

load_dotenv()

# Configurar Stripe con tu clave secreta
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

app = FastAPI(
    title="NEXUS COFFEE API",
    description="API para el sistema premium de pedidos de café",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Instancia global del controlador
controlador = CafeController()

# Ruta raíz para servir el frontend
@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

@app.get("/menu", response_model=Menu)
async def obtener_menu():
    """Obtiene el menú completo de cafés y precios"""
    return {
        "tipos": [
            {
                "id": 1,
                "nombre": "Café Americano",
                "precios": {"pequeño": 1200, "mediano": 1500, "grande": 1800}
            },
            {
                "id": 2,
                "nombre": "Café con Leche",
                "precios": {"pequeño": 1300, "mediano": 1600, "grande": 1900}
            },
            {
                "id": 3,
                "nombre": "Té Negro",
                "precios": {"pequeño": 1000, "mediano": 1300, "grande": 1600}
            },
            {
                "id": 4,
                "nombre": "Chocolate Caliente",
                "precios": {"pequeño": 1400, "mediano": 1700, "grande": 2000}
            }
        ],
        "tamanos": [
            {"id": 1, "nombre": "pequeño"},
            {"id": 2, "nombre": "mediano"},
            {"id": 3, "nombre": "grande"}
        ]
    }

@app.post("/pedido/agregar", response_model=RespuestaPedido)
async def agregar_cafe(cafe: CafeBase):
    """Agrega un café al pedido actual"""
    if controlador.agregar_cafe(cafe.tipo, cafe.tamano):
        return RespuestaPedido(
            mensaje="Café agregado exitosamente",
            pedido=controlador.obtener_pedido()
        )
    raise HTTPException(status_code=400, detail="Error al agregar el café")

@app.post("/pedido/descuento", response_model=RespuestaPedido)
async def aplicar_descuento(codigo: CodigoDescuento):
    """Aplica un código de descuento al pedido actual"""
    if not controlador.pedido["items"]:
        raise HTTPException(status_code=400, detail="No hay items en el pedido")
    
    if controlador.aplicar_codigo_descuento(codigo.codigo):
        return RespuestaPedido(
            mensaje="Código de descuento aplicado exitosamente",
            pedido=controlador.obtener_pedido()
        )
    raise HTTPException(status_code=400, detail="Código de descuento inválido")

@app.get("/pedido", response_model=Pedido)
async def obtener_pedido():
    """Obtiene el pedido actual"""
    if not controlador.pedido["items"]:
        raise HTTPException(status_code=400, detail="No hay items en el pedido")
    return controlador.obtener_pedido()

@app.post("/pedido/reiniciar")
async def reiniciar_pedido():
    """Reinicia el pedido actual"""
    controlador.reiniciar_pedido()
    return {"mensaje": "Pedido reiniciado exitosamente"}

@app.post("/create-checkout-session/")
async def create_checkout_session(pedido: Pedido):
    line_items = []
    for item in pedido.items:
        # Stripe espera precios en la unidad más pequeña de la moneda (ej: centavos)
        # Asegúrate de que item.precio sea el precio por unidad en la unidad base
        # y conviértelo a centavos (o la unidad base de tu moneda)
        price_in_cents = int(item.precio * 100) # Ajusta si tu moneda no es USD y no usa centavos

        line_items.append({
            'price_data': {
                'currency': 'usd', # Cambia a tu moneda (ej: 'clp' para pesos chilenos)
                'product_data': {
                    'name': f"{item.tipo} ({item.tamano})",
                },
                'unit_amount': price_in_cents,
            },
            'quantity': item.cantidad,
        })

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            success_url='http://localhost:8000/static/success.html', # Crea una página de éxito
            cancel_url='http://localhost:8000/', # Redirige de vuelta si cancela
        )
        return {"url": checkout_session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 