
# Importamos las librerías necesarias
from fastapi import FastAPI, Depends, HTTPException               # FastAPI y manejo de errores HTTP
from sqlalchemy.orm import Session                                # Para manejar sesiones con la base de datos
#from . import models, schemas, database     
import models, schemas, database                      # Nuestros módulos propios (modelos, esquemas, base de datos)

# Creamos la instancia principal de la aplicación FastAPI
app = FastAPI(title="Sistema de Ventas Locatel")   #Instancia principal de la aplicacionm

# Dependencia que nos permite obtener una sesión de base de datos por cada petición
def get_db():
    db = database.SessionLocal()  # Crea una nueva sesión con la base de datos
    try:
        yield db                  # La "cede" al endpoint que la use
    finally:
        db.close()                # Cierra la conexión después de usarla

# ---------------------------------------------------
# 🧩 1. ENDPOINT PARA CREAR CLIENTE
# ---------------------------------------------------
@app.post("/clientes", response_model=schemas.ClienteOut)  #Funciones previas
def crear_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    """
    Este endpoint crea un nuevo cliente en la base de datos.
    - Recibe un objeto JSON con los datos del cliente (cedula, nombre, etc.)
    - Verifica que no exista ya un cliente con la misma cédula.
    - Inserta el nuevo registro si todo está correcto.
    """
    # Busca si ya existe un cliente con la misma cédula
    db_cliente = db.query(models.Cliente).filter(models.Cliente.cedula == cliente.cedula).first()
    if db_cliente:
        # Si existe, lanza un error HTTP 400 (Bad Request)
        raise HTTPException(status_code=400, detail="El cliente ya existe") #raise es levatnar una excepcion

    # Crea un nuevo objeto Cliente a partir del esquema recibido
    nuevo_cliente = models.Cliente(**cliente.dict()) #** los asteriscos signifcian kwargs son argumentos de llave y valor

    # Lo agrega a la sesión
    db.add(nuevo_cliente)
    # Confirma los cambios (INSERT en la base de datos)
    db.commit()
    # Refresca el objeto con los datos reales (por ejemplo, el ID generado)
    db.refresh(nuevo_cliente)
    # Retorna el nuevo cliente creado
    return nuevo_cliente

# ---------------------------------------------------
# 🧩 2. ENDPOINT PARA LISTAR TODOS LOS CLIENTES
# ---------------------------------------------------
@app.get("/clientes", response_model=list[schemas.ClienteOut])
def listar_clientes(db: Session = Depends(get_db)):
    """
    Devuelve un listado con todos los clientes registrados.
    - No recibe parámetros.
    - Retorna una lista de objetos Cliente.
    """
    # Consulta todos los registros de la tabla clientes
    return db.query(models.Cliente).all()

# ---------------------------------------------------
# 🧩 3. ENDPOINT PARA CONSULTAR CLIENTE POR CÉDULA
# ---------------------------------------------------
@app.get("/clientes/{cedula}", response_model=schemas.ClienteOut)
def obtener_cliente(cedula: str, db: Session = Depends(get_db)):
    """
    Permite buscar un cliente por su número de cédula.
    - Si el cliente no existe, devuelve un error 404.
    """
    # Busca el cliente que tenga la cédula indicada
    cliente = db.query(models.Cliente).filter(models.Cliente.cedula == cedula).first()
    if not cliente:
        # Si no lo encuentra, lanza un error HTTP 404 (Not Found)
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    # Retorna el cliente encontrado
    return cliente

# ---------------------------------------------------
# 🧩 4. ENDPOINT PARA ACTUALIZAR UN CLIENTE EXISTENTE
# ---------------------------------------------------
@app.put("/clientes/{cedula}", response_model=schemas.ClienteOut)
def actualizar_cliente(cedula: str, datos: schemas.ClienteCreate, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un cliente existente.
    - Busca por cédula.
    - Si lo encuentra, actualiza los campos con la nueva información.
    - Si no lo encuentra, lanza un error 404.
    """
    # Busca el cliente por cédula
    cliente = db.query(models.Cliente).filter(models.Cliente.cedula == cedula).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    # Recorre los campos enviados y los reemplaza en el registro existente
    for key, value in datos.dict().items():
        setattr(cliente, key, value)

    # Guarda los cambios
    db.commit()
    db.refresh(cliente)
    return cliente

# ---------------------------------------------------
# 🧩 5. ENDPOINT PARA ELIMINAR UN CLIENTE
# ---------------------------------------------------
@app.delete("/clientes/{cedula}")
def eliminar_cliente(cedula: str, db: Session = Depends(get_db)):
    """
    Elimina un cliente de la base de datos.
    - Busca por cédula.
    - Si existe, lo borra.
    - Si no existe, devuelve un error 404.
    """
    cliente = db.query(models.Cliente).filter(models.Cliente.cedula == cedula).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    # Elimina el registro y guarda los cambios
    db.delete(cliente)
    db.commit()
    return {"mensaje": "Cliente eliminado correctamente"}
