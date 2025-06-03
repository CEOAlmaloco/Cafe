from pydantic import BaseModel
from typing import List, Dict, Optional

class CafeBase(BaseModel):
    tipo: str
    tamano: str
    cantidad: int = 1

class ItemPedido(BaseModel):
    tipo: str
    tamano: str
    precio: int
    cantidad: int
    precioTotal: int

class Pedido(BaseModel):
    items: List[ItemPedido]
    total: int
    codigoDescuento: Optional[str] = None

class CodigoDescuento(BaseModel):
    codigo: str

class RespuestaPedido(BaseModel):
    mensaje: str
    pedido: Pedido

class Menu(BaseModel):
    tipos: List[Dict]
    tamanos: List[Dict] 