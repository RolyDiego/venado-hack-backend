from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import hashlib
import json
from uuid import UUID

from app.database import get_db
from app.schemas.route_schema import (
    RouteOptimizationRequest, 
    RouteOptimizationFullResponse,
    MarketTasksResponse
)
from app.repositories.customer_repository import CustomerRepository
from app.services.route_optimizer import RouteOptimizerService
from app.models.market_category import OptimizedRoute, MarketCategory, CategoryTask
from app.models.market import Market
from app.models.customer import Customer

router = APIRouter(prefix="/api/routes", tags=["routes"])

@router.post("/optimize", response_model=RouteOptimizationFullResponse)
async def optimize_route(
    request: RouteOptimizationRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Optimize visit route for a merchandiser based on their location and the day of week.
    Implements cache-first strategy to avoid redundant calculations.
    """
    try:
        # 1. Instanciar el repositorio
        repository = CustomerRepository(db)
        
        # 2. Obtener los clientes del día para el merchandiser con sus mercados y categorías
        customers = await repository.get_customers_by_merchandiser_and_day(
            merchandiser_id=UUID(request.merchandiser_id),
            day_of_week=request.day_of_week
        )
        
        if not customers:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontraron clientes asignados para este repositor en el día indicado."
            )
        
        # 2.1 Obtener tareas para cada cliente basado en su categoría de mercado
        customer_ids = [c.id for c in customers]
        customers_with_tasks = await db.execute(
            select(Customer, Market, MarketCategory)
            .join(Market, Customer.market_id == Market.id)
            .outerjoin(MarketCategory, Market.category_id == MarketCategory.id)
            .where(Customer.id.in_(customer_ids))
        )
        customers_with_tasks = customers_with_tasks.all()
        
        # Crear un diccionario de customer_id -> tasks y category info
        customer_data_map = {}
        for customer, market, category in customers_with_tasks:
            if category:
                tasks_result = await db.execute(
                    select(CategoryTask).where(CategoryTask.category_id == category.id)
                )
                tasks = tasks_result.scalars().all()
                customer_data_map[customer.id] = {
                    "tasks": [
                        {
                            "id": task.id,
                            "task_description": task.task_description,
                            "estimated_time_mins": task.estimated_time_mins
                        }
                        for task in tasks
                    ],
                    "category": customer.category,
                    "category_display_name": category.display_name,
                    "category_icon": category.icon_name
                }
            else:
                customer_data_map[customer.id] = {
                    "tasks": [],
                    "category": customer.category,
                    "category_display_name": None,
                    "category_icon": None
                }
        
        # 3. Generar hash identificador para caché
        destination_ids = sorted([str(customer.id) for customer in customers])
        hash_input = f"{request.latitude}_{request.longitude}_{'_'.join(destination_ids)}"
        destination_ids_hash = hashlib.sha256(hash_input.encode()).hexdigest()
        
        # 4. Validación de Caché (Búsqueda en BD)
        cached_route = await db.execute(
            select(OptimizedRoute).where(
                OptimizedRoute.destination_ids_hash == destination_ids_hash
            )
        )
        cached_route = cached_route.scalar_one_or_none()
        
        # HIT: Retornar ruta desde caché
        if cached_route:
            return RouteOptimizationFullResponse(**cached_route.optimized_path_json)
        
        # MISS: Optimizar la ruta con OR-Tools
        result = RouteOptimizerService.optimize_route(
            origin_lat=request.latitude,
            origin_lon=request.longitude,
            customers=customers,
            customer_data_map=customer_data_map
        )
        
        # 5. Almacenar en caché antes de retornar
        new_cached_route = OptimizedRoute(
            origin_lat=request.latitude,
            origin_lng=request.longitude,
            destination_ids_hash=destination_ids_hash,
            optimized_path_json=result.model_dump(mode='json')
        )
        db.add(new_cached_route)
        await db.commit()
        
        return result

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error optimizando la ruta: {str(e)}"
        )


@router.get("/markets/{market_id}/tasks", response_model=MarketTasksResponse)
async def get_market_tasks(
    market_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get tasks assigned to a market based on its category.
    """
    try:
        # 1. Obtener el mercado con su categoría
        market = await db.execute(
            select(Market).where(Market.id == market_id)
        )
        market = market.scalar_one_or_none()
        
        if not market:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mercado no encontrado"
            )
        
        if not market.category_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El mercado no tiene una categoría asignada"
            )
        
        # 2. Obtener la categoría con sus tareas
        category = await db.execute(
            select(MarketCategory).where(MarketCategory.id == market.category_id)
        )
        category = category.scalar_one_or_none()
        
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada"
            )
        
        # 3. Obtener las tareas de la categoría
        tasks = await db.execute(
            select(CategoryTask)
            .where(CategoryTask.category_id == category.id)
            .order_by(CategoryTask.id)
        )
        tasks = tasks.scalars().all()
        
        # 4. Calcular tiempo total estimado
        total_time = sum(task.estimated_time_mins for task in tasks)
        
        return MarketTasksResponse(
            market_id=market.id,
            category_name=category.name,
            category_display_name=category.display_name,
            category_icon=category.icon_name,
            total_tasks=len(tasks),
            total_estimated_time_mins=total_time,
            tasks=[
                {
                    "id": task.id,
                    "task_description": task.task_description,
                    "estimated_time_mins": task.estimated_time_mins
                }
                for task in tasks
            ]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo tareas: {str(e)}"
        )
