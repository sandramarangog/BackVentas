from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Registrar venta completa
@app.post("/ventas/", response_model=schemas.VentaOut)
def crear_venta(venta: schemas.VentaCreate, db: Session = Depends(get_db)):
    # Cabecera
    nueva_venta = models.Venta(
        consecutivo=venta.consecutivo,
        fecha=venta.fecha,
        id_cliente=venta.id_cliente,
        total_venta=venta.total_venta
    )
    db.add(nueva_venta)
    db.commit()
    db.refresh(nueva_venta)

    # Detalles
    for det in venta.detalles:
        nuevo_det = models.VentaDet(
            id_venta=nueva_venta.id_venta,
            id_producto=det.id_producto,
            valor_producto=det.valor_producto,
            iva_calculado=det.iva_calculado
        )
        db.add(nuevo_det)
    db.commit()

    return nueva_venta

# Listar ventas
@app.get("/ventas/", response_model=list[schemas.VentaOut])
def listar_ventas(db: Session = Depends(get_db)):
    return db.query(models.Venta).all()
