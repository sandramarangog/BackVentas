# --------------------------------------------------------
# 📘 MODELS.PY
# Define la estructura de la tabla "clientes" en la base de datos
# --------------------------------------------------------

#from sqlalchemy import Column, Integer, String,Float, Boolean
#from database import Base  # Importa la clase base desde database.py
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
# --------------------------------------------------------
# 🧩 Modelo de tabla CLIENTES (ORM SQLAlchemy)
# --------------------------------------------------------
class Cliente(Base):
    __tablename__ = "clientes"  # Nombre de la tabla en la base de datos

    # Columnas de la tabla
    id_cliente = Column(Integer, primary_key=True, index=True)       # ID autoincremental
    cedula = Column(String, unique=True, index=True, nullable=False)  # Cédula única
    nombre = Column(String, nullable=False)                   # Nombre del cliente
    direccion = Column(String, nullable=False)                # Dirección
    telefono = Column(String, nullable=False)                 # Teléfono
    email = Column(String, nullable=False)                    # Correo electrónico

    def __repr__(self):
        """
        Representación legible del objeto Cliente.
        Ayuda al depurar y ver los datos en consola.
        """
        return f"<Cliente(nombre={self.nombre}, cedula={self.cedula})>"
    
    venta = relationship("Venta", back_populates="cliente")
    

    # --------------------------------------------------------
# 🧩 Modelo de tabla PRODUCTOS (ORM SQLAlchemy)
# --------------------------------------------------------

class Producto(Base):
    __tablename__ = "producto"

    id_producto = Column(Integer, primary_key=True, index=True, autoincrement=True)
    codigo = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    valor_venta = Column(Float, nullable=False)
    iva = Column(Boolean, default=False)
    porcentaje_iva = Column(Float, default=0.0)

    def __repr__(self):
        return f"<Producto(nombre={self.nombre}, valor_venta={self.valor_venta}, iva={self.iva})>"
    
    detalles = relationship("DetalleVenta", back_populates="producto")

        # --------------------------------------------------------
# 🧩 Modelo de tabla CABECERA DE VENTAS (ORM SQLAlchemy)
# --------------------------------------------------------
class Venta(Base):
    __tablename__ = "venta"
    id_venta = Column(Integer, primary_key=True, index=True)
    consecutivo = Column(String, unique=True, nullable=False)
    fecha = Column(String, nullable=False)
    id_cliente = Column(Integer, nullable=False)
    total_venta = Column(Float, default=0)

class VentaDet(Base):
    __tablename__ = "ventadet"
    id_detalle = Column(Integer, primary_key=True, index=True)
    id_venta = Column(Integer, nullable=False)
    id_producto = Column(Integer, nullable=False)
    valor_producto = Column(Float, nullable=False)
    iva_calculado = Column(Float, default=0)