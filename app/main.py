from fastapi import FastAPI
from app.database import Base, engine
from app.routers import merchandiser_router

from app.routers import carga_datos_router
from app.routers import auth_router
from app.routers import dashboard_router
from app.routers import mobile_router
from app.routers import route_router
from app.routers import location_router

app = FastAPI(
    title="Venado Hack Backend",
    version="1.0.0",
    description="API para gestión operativa de rutas, PDVs, visitas y dashboard"
)

# Crear tablas en PostgreSQL de forma asíncrona
@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
# Incluir routers
app.include_router(carga_datos_router.router)
app.include_router(auth_router.router)
app.include_router(dashboard_router.router)
app.include_router(mobile_router.router)
app.include_router(route_router.router)
app.include_router(location_router.router)

@app.get("/")
async def root():
    return {"message": "Venado Hack Backend API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}