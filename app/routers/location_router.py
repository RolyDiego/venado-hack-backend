from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.schemas.location_schema import LocationUpdateRequest, LocationUpdateResponse
from app.repositories.location_repository import LocationRepository

router = APIRouter(prefix="/api/locations", tags=["locations"])

@router.post("", response_model=LocationUpdateResponse)
async def update_location(
    payload: LocationUpdateRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint para recibir coordenadas GPS de un reponedor.
    Actualiza su ubicación actual y registra un historial.
    """
    try:
        repository = LocationRepository(db)
        await repository.save_location(payload)
        
        return LocationUpdateResponse(
            status="success",
            message="Ubicación actualizada correctamente"
        )
    except IntegrityError as e:
        # En caso de que el merchandiser_id no exista
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El merchandiser_id especificado no existe o es inválido."
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al guardar la ubicación: {str(e)}"
        )
