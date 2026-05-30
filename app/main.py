from fastapi import FastAPI
from app.database import Base, engine
from app.routers import merchandiser_router

from app.routers import carga_datos_router
from app.routers import auth_router
from app.routers import dashboard_router
from app.routers import mobile_router
from app.routers import pdv_router

from app.models import supervisor, merchandiser, market, customer, customer_visit_day
from app.routers import customer_router

app = FastAPI(
    title="Venado Hack Backend",
    version="1.0.0",
    description="API para gestión operativa de rutas, PDVs, visitas y dashboard"
)

# Crear tablas en PostgreSQL
Base.metadata.create_all(bind=engine)

# Incluir routers
app.include_router(
    carga_datos_router.router,
    prefix="/carga-datos",
    tags=["Carga de Datos"]
)

app.include_router(
    auth_router.router,
    prefix="/auth",
    tags=["Auth"]
)

app.include_router(
    dashboard_router.router,
    prefix="/dashboard",
    tags=["Dashboard"]
)

app.include_router(
    mobile_router.router,
    prefix="/mobile",
    tags=["Mobile"]
)

app.include_router(
    customer_router.router,
    prefix="/api",
    tags=["Customers"]
)

app.include_router(
    merchandiser_router.router,
    prefix="/api",
    tags=["Merchandisers"]
)

@app.get("/")
async def root():
    return {"message": "Venado Hack Backend API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}