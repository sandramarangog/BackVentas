# --------------------------------------------------------
# 📘 MODELS.PY
# --------------------------------------------------------

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# --------------------------------------------------------
# 🧩 Modelo CLIENTE
# --------------------------------------------------------
class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True, index=True)
    cedula = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    email = Column(String, nullable=False)

    # Relación con ventas
    ventas = relationship("Venta", back_populates="cliente")

    def __repr__(self):
        return f"<Cliente(nombre={self.nombre}, cedula={self.cedula})>"


# --------------------------------------------------------
# 🧩 Modelo PRODUCTO
# --------------------------------------------------------
class Producto(Base):
    __tablename__ = "producto"

    id_producto = Column(Integer, primary_key=True, index=True, autoincrement=True)
    codigo = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    valor_venta = Column(Float, nullable=False)
    iva = Column(Boolean, default=False)
    porcentaje_iva = Column(Float, default=0.0)

    # Relación con detalle de venta
    detalles = relationship("VentaDet", back_populates="producto")

    def __repr__(self):
        return f"<Producto(nombre={self.nombre}, valor_venta={self.valor_venta}, iva={self.iva})>"


# --------------------------------------------------------
# 🧩 Modelo VENTA (Cabecera)
# --------------------------------------------------------
class Venta(Base):
    __tablename__ = "venta"

    id_venta = Column(Integer, primary_key=True, index=True)
    consecutivo = Column(String, unique=True, nullable=False)
    fecha = Column(String, nullable=False)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False)
    total_venta = Column(Float, default=0)

    # Relaciones
    cliente = relationship("Cliente", back_populates="ventas")
    detalles = relationship("VentaDet", back_populates="venta")

    def __repr__(self):
        return f"<Venta(consecutivo={self.consecutivo}, total_venta={self.total_venta})>"


# --------------------------------------------------------
# 🧩 Modelo DETALLE DE VENTA
# --------------------------------------------------------
class VentaDet(Base):
    __tablename__ = "ventadet"

    id_detalle = Column(Integer, primary_key=True, index=True)
    id_venta = Column(Integer, ForeignKey("venta.id_venta"), nullable=False)
    id_producto = Column(Integer, ForeignKey("producto.id_producto"), nullable=False)
    valor_producto = Column(Float, nullable=False)
    iva_calculado = Column(Float, default=0)

    # Relaciones
    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles")

    def __repr__(self):
        return f"<VentaDet(id_venta={self.id_venta}, id_producto={self.id_producto})>"
