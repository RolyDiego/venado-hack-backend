import asyncio
import asyncpg

async def init_db():
    print("Conectando a la base de datos...")
    conn = await asyncpg.connect('postgresql://venado_user:venado_password@localhost:5432/venado_hack_db')
    
    print("Leyendo init.sql...")
    with open("app/sql/init.sql", "r") as f:
        sql = f.read()
        
    print("Ejecutando sentencias SQL...")
    await conn.execute(sql)
        
    print("Base de datos inicializada exitosamente.")
    await conn.close()

if __name__ == "__main__":
    asyncio.run(init_db())
