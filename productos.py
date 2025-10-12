# Importamos las librerías necesarias
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database

from fastapi.middleware.cors import CORSMiddleware

# ---------------------------------------------------
# 🌟 Instancia principal de la aplicación FastAPI
# ---------------------------------------------------
app = FastAPI(title="Sistema de Ventas Locatel")

# Configuración del CORS para permitir llamadas desde el frontend (React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # puedes restringir a ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia para obtener sesión de base de datos
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------------------------------
# 🧩 1. ENDPOINT PARA CREAR PRODUCTOS
# ---------------------------------------------------
@app.post("/productos/", response_model=schemas.ProductoOut)
def crear_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo producto en la base de datos.
    - Valida que no exista un producto con el mismo código.
    - Inserta el nuevo producto si todo es correcto.
    """
    db_producto = db.query(models.Producto).filter(models.Producto.codigo == producto.codigo).first()
    if db_producto:
        raise HTTPException(status_code=400, detail="El producto ya existe")

    nuevo_producto = models.Producto(**producto.dict())
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto

# ---------------------------------------------------
# 🧩 2. ENDPOINT PARA LISTAR TODOS LOS PRODUCTOS
# ---------------------------------------------------
@app.get("/productos/", response_model=list[schemas.ProductoOut])
def listar_productos(db: Session = Depends(get_db)):
    """
    Retorna una lista de todos los productos registrados.
    """
    return db.query(models.Producto).all()

# ---------------------------------------------------
# 🧩 3. ENDPOINT PARA CONSULTAR UN PRODUCTO POR CÓDIGO
# ---------------------------------------------------
@app.get("/productos/{codigo}", response_model=schemas.ProductoOut)
def obtener_producto(codigo: str, db: Session = Depends(get_db)):
    """
    Permite buscar un producto por su código.
    - Si no existe, retorna error 404.
    """
    producto = db.query(models.Producto).filter(models.Producto.codigo == codigo).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto
