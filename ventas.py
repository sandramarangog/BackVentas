from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import models, schemas, database

app = FastAPI(title="Módulo de Ventas - Locatel")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------------------------------------------------------
# 🧩 POST /ventas/  → Registrar cabecera y detalle
# --------------------------------------------------------
@app.post("/ventas/", response_model=schemas.VentaOut)
def crear_venta(venta: schemas.VentaCreate, db: Session = Depends(get_db)):
    # Validar que no exista consecutivo duplicado
    existe = db.query(models.Venta).filter(models.Venta.consecutivo == venta.consecutivo).first()
    if existe:
        raise HTTPException(status_code=400, detail="El consecutivo ya existe")

    # Crear cabecera
    nueva_venta = models.Venta(
        consecutivo=venta.consecutivo,
        fecha=venta.fecha,
        id_cliente=venta.id_cliente,
        total_venta=venta.total_venta,
    )
    db.add(nueva_venta)
    db.commit()
    db.refresh(nueva_venta)

    # Crear detalles asociados
    for d in venta.detalles:
        detalle = models.VentaDet(
            id_venta=nueva_venta.id_venta,
            id_producto=d.id_producto,
            valor_producto=d.valor_producto,
            iva_calculado=d.iva_calculado,
        )
        db.add(detalle)

    db.commit()
    db.refresh(nueva_venta)

    return nueva_venta


# --------------------------------------------------------
# 🧩 GET /ventas/ → Listar todas las ventas
# --------------------------------------------------------
@app.get("/ventas/", response_model=list[schemas.VentaOut])
def listar_ventas(db: Session = Depends(get_db)):
    return db.query(models.Venta).all()


# --------------------------------------------------------
# 🧩 GET /ventas/{fecha} → Filtrar ventas por fecha
# --------------------------------------------------------
@app.get("/ventas/{fecha}", response_model=list[schemas.VentaOut])
def ventas_por_fecha(fecha: str, db: Session = Depends(get_db)):
    ventas = db.query(models.Venta).filter(models.Venta.fecha == fecha).all()
    if not ventas:
        raise HTTPException(status_code=404, detail="No hay ventas registradas en esa fecha")
    return ventas
