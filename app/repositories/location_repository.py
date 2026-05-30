from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from app.models.location import MerchandiserLocation, MerchandiserLocationHistory
from app.schemas.location_schema import LocationUpdateRequest

class LocationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_location(self, data: LocationUpdateRequest):
        # 1. Upsert (Actualizar o Insertar) en la tabla de ubicacion actual
        stmt = insert(MerchandiserLocation).values(
            merchandiser_id=data.merchandiser_id,
            latitude=data.latitude,
            longitude=data.longitude,
            accuracy=data.accuracy,
            speed=data.speed
        )
        
        # En PostgreSQL usamos ON CONFLICT para hacer el upsert
        upsert_stmt = stmt.on_conflict_do_update(
            index_elements=['merchandiser_id'],
            set_=dict(
                latitude=stmt.excluded.latitude,
                longitude=stmt.excluded.longitude,
                accuracy=stmt.excluded.accuracy,
                speed=stmt.excluded.speed,
                updated_at=stmt.excluded.updated_at
            )
        )
        
        await self.session.execute(upsert_stmt)
        
        # 2. Insertar en el historial
        history_record = MerchandiserLocationHistory(
            merchandiser_id=data.merchandiser_id,
            latitude=data.latitude,
            longitude=data.longitude,
            accuracy=data.accuracy,
            speed=data.speed
        )
        self.session.add(history_record)
        
        # Guardar cambios
        await self.session.commit()
