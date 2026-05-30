from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional

class LocationUpdateRequest(BaseModel):
    merchandiser_id: UUID
    latitude: float = Field(..., description="Latitud de la ubicación actual", ge=-90.0, le=90.0)
    longitude: float = Field(..., description="Longitud de la ubicación actual", ge=-180.0, le=180.0)
    accuracy: Optional[float] = Field(None, description="Precisión del GPS en metros")
    speed: Optional[float] = Field(None, description="Velocidad actual en metros/segundo o km/h")
    
class LocationUpdateResponse(BaseModel):
    status: str
    message: str
