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
    __tablename__ = "cliente"

    id_cliente = Column(Integer, primary_key=True, index=True)
    cedula = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    email = Column(String, nullable=False)

    # 🔹 Relación con ventas
    ventas = relationship("Venta", back_populates="cliente")


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
# 🧩 Modelo de tabla VENTA
# --------------------------------------------------------
class Venta(Base):
    __tablename__ = "venta"

    id_venta = Column(Integer, primary_key=True, index=True, autoincrement=True)
    consecutivo = Column(String, unique=True, nullable=False)
    fecha = Column(String, nullable=False)
    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente"), nullable=False)  # 🔹 ForeignKey agregado
    total_venta = Column(Float, default=0)

    # Relación con los detalles
    detalles = relationship("VentaDet", back_populates="venta", cascade="all, delete-orphan")

    # 🔹 Relación con cliente
    cliente = relationship("Cliente", back_populates="ventas")


# --------------------------------------------------------
# 🧩 Modelo de tabla VENTADET
# --------------------------------------------------------
class VentaDet(Base):
    __tablename__ = "ventadet"

    id_detalle = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_venta = Column(Integer, ForeignKey("venta.id_venta"), nullable=False)
    id_producto = Column(Integer, ForeignKey("producto.id_producto"), nullable=False)  # ✅ Agregado
    valor_producto = Column(Float, nullable=False)
    iva_calculado = Column(Float, default=0)

    # Relación con la cabecera
    venta = relationship("Venta", back_populates="detalles")

    # 🔹 Relación con el producto
    producto = relationship("Producto", back_populates="detalles")  # ✅ Agregado
