# --------------------------------------------------------
# 📘 MODELS.PY
# Define la estructura de la tabla "clientes" en la base de datos
# --------------------------------------------------------

from sqlalchemy import Column, Integer, String,Float, Boolean
from database import Base  # Importa la clase base desde database.py

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
    

    # --------------------------------------------------------
# 🧩 Modelo de tabla PRODUCTOS (ORM SQLAlchemy)
# --------------------------------------------------------
class Producto(Base):
    __tablename__ = "productos"  # Nombre de la tabla en la base de datos

    id_producto = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    valor_venta = Column(Float, nullable=False)
    iva = Column(Boolean, default=False)
    porcentaje_iva = Column(Float, nullable=True)

    def __repr__(self):
        return f"<Producto(nombre={self.nombre}, valor={self.valor_venta})>"
