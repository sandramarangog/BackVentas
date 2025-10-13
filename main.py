from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from clientes import router as clientes_router
from productos import router as productos_router
from ventas import router as ventas_router

app = FastAPI(title="Sistema de Ventas Locatel")

# Configuración CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia a ["http://localhost:5173"] si usas Vite o React local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar los routers
app.include_router(clientes_router)
app.include_router(productos_router)
app.include_router(ventas_router)
