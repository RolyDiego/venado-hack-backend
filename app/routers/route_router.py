from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.schemas.route_schema import RouteOptimizationRequest, RouteOptimizationFullResponse
from app.repositories.customer_repository import CustomerRepository
from app.services.route_optimizer import RouteOptimizerService

router = APIRouter(prefix="/api/routes", tags=["routes"])

@router.post("/optimize", response_model=RouteOptimizationFullResponse)
async def optimize_route(
    request: RouteOptimizationRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Optimize visit route for a merchandiser based on their location and the day of week.
    """
    try:
        # 1. Instanciar el repositorio
        repository = CustomerRepository(db)
        
        # 2. Obtener los clientes del día para el merchandiser
        customers = await repository.get_customers_by_merchandiser_and_day(
            merchandiser_id=request.merchandiser_id,
            day_of_week=request.day_of_week
        )
        
        if not customers:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontraron clientes asignados para este repositor en el día indicado."
            )
            
        # 3. Optimizar la ruta con OR-Tools
        result = RouteOptimizerService.optimize_route(
            origin_lat=request.latitude,
            origin_lon=request.longitude,
            customers=customers
        )
        
        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error optimizando la ruta: {str(e)}"
        )
