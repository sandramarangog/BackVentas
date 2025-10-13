from pydantic import BaseModel, EmailStr
from typing import Optional
from typing import List

# --------------------------------------------------------
# 🔹 Modelo base — contiene los campos comunes del cliente
# --------------------------------------------------------
class ClienteBase(BaseModel):
    cedula: str
    nombre: str
    direccion: str
    telefono: str
    email: EmailStr

# --------------------------------------------------------
# 🔹 Modelo de creación — usado cuando se inserta un nuevo cliente
# --------------------------------------------------------
class ClienteCreate(ClienteBase):
    pass  # Por ahora es igual al base, pero podrías personalizarlo después

# --------------------------------------------------------
# 🔹 Modelo de salida — usado cuando FastAPI devuelve datos al frontend
# --------------------------------------------------------
class ClienteOut(ClienteBase):
    id_cliente: int  # Campo adicional, que normalmente agrega la base de datos

    class Config:
        orm_mode = True  # Permite a Pydantic trabajar con objetos ORM (SQLAlchemy)

  # finaliza clientes
  # 
  #
class ProductoBase(BaseModel):
    codigo: str
    nombre: str
    valor_venta: float
    iva: bool
    porcentaje_iva: Optional[float] = 0.0

class ProductoCreate(ProductoBase):
    pass

class ProductoOut(ProductoBase):
    id_producto: int
    class Config:
        orm_mode = True#       



# -----------------------------
# Detalle de Venta (nuevo)
#VentaCreate es lo que envía el frontend al crear una venta.
#VentaOut es lo que retorna el backend.
# -----------------------------

class VentaDetBase(BaseModel):
    id_producto: int
    valor_producto: float
    iva_calculado: float


class VentaDetCreate(VentaDetBase):
    pass


class VentaDetOut(VentaDetBase):
    id_detalle: int
    producto: Optional[ProductoOut] = None  # <-- permite incluir el nombre del producto
    class Config:
        orm_mode = True
        

# --------------------------------------------------------
# 🧩 Schemas para Venta (cabecera)
# --------------------------------------------------------
class VentaBase(BaseModel):
    consecutivo: str
    fecha: str
    id_cliente: int
    total_venta: float


class VentaCreate(VentaBase):
    detalles: List[VentaDetCreate]


class VentaOut(VentaBase):
    id_venta: int
    detalles: List[VentaDetOut]
    cliente: Optional[ClienteOut] = None

    class Config:
        orm_mode = True