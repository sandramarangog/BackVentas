from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database

router = APIRouter(prefix="/clientes", tags=["Clientes"])

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🧩 Crear cliente
@router.post("/", response_model=schemas.ClienteOut)
def crear_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.cedula == cliente.cedula).first()
    if db_cliente:
        raise HTTPException(status_code=400, detail="El cliente ya existe")

    nuevo_cliente = models.Cliente(**cliente.dict())
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente


# 🧩 Listar todos los clientes
@router.get("/", response_model=list[schemas.ClienteOut])
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(models.Cliente).all()


# 🧩 Buscar cliente por cédula
@router.get("/{cedula}", response_model=schemas.ClienteOut)
def obtener_cliente(cedula: str, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(models.Cliente.cedula == cedula).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


# 🧩 Actualizar cliente
@router.put("/{cedula}", response_model=schemas.ClienteOut)
def actualizar_cliente(cedula: str, datos: schemas.ClienteCreate, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(models.Cliente.cedula == cedula).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    for key, value in datos.dict().items():
        setattr(cliente, key, value)
    db.commit()
    db.refresh(cliente)
    return cliente


# 🧩 Eliminar cliente
@router.delete("/{cedula}")
def eliminar_cliente(cedula: str, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(models.Cliente.cedula == cedula).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    db.delete(cliente)
    db.commit()
    return {"mensaje": "Cliente eliminado correctamente"}
