from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database


router = APIRouter(prefix="/productos", tags=["Productos"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.ProductoOut)
def crear_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    db_producto = db.query(models.Producto).filter(models.Producto.nombre == producto.nombre).first()
    if db_producto:
        raise HTTPException(status_code=400, detail="El producto ya existe")

    nuevo_producto = models.Producto(**producto.dict())
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto


@router.get("/", response_model=list[schemas.ProductoOut])
def listar_productos(db: Session = Depends(get_db)):
    return db.query(models.Producto).all()


@router.get("/ultimo", response_model=dict)
def obtener_ultimo_producto(db: Session = Depends(get_db)):
    """
    Devuelve el último código de producto registrado.
    Si no hay productos, retorna un código inicial (por ejemplo: 'P001').
    """
    ultimo = db.query(models.Producto).order_by(models.Producto.id_producto.desc()).first()

    if not ultimo:
        return {"ultimo_codigo": "P001"}  # si no hay registros

    return {"ultimo_codigo": ultimo.codigo}
