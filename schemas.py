from pydantic import BaseModel, EmailStr
from typing import Optional

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
    maneja_iva: bool
    porcentaje_iva: Optional[float] = 0.0

class ProductoCreate(ProductoBase):
    pass

class ProductoOut(ProductoBase):
    id: int

    class Config:
        orm_mode = True#       
