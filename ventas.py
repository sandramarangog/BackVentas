from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database



router = APIRouter(prefix="/ventas", tags=["Ventas"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.VentaOut)
def crear_venta(venta: schemas.VentaCreate, db: Session = Depends(get_db)):
    existe = db.query(models.Venta).filter(models.Venta.consecutivo == venta.consecutivo).first()
    if existe:
        raise HTTPException(status_code=400, detail="El consecutivo ya existe")

    nueva_venta = models.Venta(
        consecutivo=venta.consecutivo,
        fecha=venta.fecha,
        id_cliente=venta.id_cliente,
        total_venta=venta.total_venta,
    )
    db.add(nueva_venta)
    db.commit()
    db.refresh(nueva_venta)

    for d in venta.detalles:
        detalle = models.VentaDet(
            id_venta=nueva_venta.id_venta,
            id_producto=d.id_producto,
            valor_producto=d.valor_producto,
            iva_calculado=d.iva_calculado,
        )
        db.add(detalle)

    db.commit()
    return nueva_venta


@router.get("/", response_model=list[schemas.VentaOut])
def listar_ventas(db: Session = Depends(get_db)):
    return db.query(models.Venta).all()


@router.get("/{fecha}", response_model=list[schemas.VentaOut])
def ventas_por_fecha(fecha: str, db: Session = Depends(get_db)):
    ventas = db.query(models.Venta).filter(models.Venta.fecha == fecha).all()
    if not ventas:
        raise HTTPException(status_code=404, detail="No hay ventas registradas en esa fecha")
    return ventas


# ultimo consecutivo
# Ruta segura que no choca con /ventas/{fecha}
@router.get("/ultimo/consecutivo")
def ultimo_consecutivo(db: Session = Depends(get_db)):
    ultima_venta = db.query(models.Venta).order_by(models.Venta.id_venta.desc()).first()
    if ultima_venta:
        return {"ultimo_consecutivo": ultima_venta.consecutivo}
    return {"ultimo_consecutivo": "v00"}





