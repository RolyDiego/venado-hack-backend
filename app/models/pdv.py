from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class PDV(Base):
    __tablename__ = "pdvs"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True)
    nombre = Column(String)
    categoria = Column(String)
    mercado = Column(String)
    supervisor = Column(String)
    reponedor = Column(String)
    latitud = Column(Float)
    longitud = Column(Float)
    tiempo_promedio = Column(Float)
    frecuencia_semanal = Column(Integer)