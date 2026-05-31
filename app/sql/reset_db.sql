-- Script para eliminar toda la base de datos y recrearla desde cero
-- ADVERTENCIA: Este script eliminará TODOS los datos

-- Eliminar tablas en orden inverso para respetar foreign keys
DROP TABLE IF EXISTS merchandiser_locations CASCADE;
DROP TABLE IF EXISTS customer_visit_days CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS optimized_routes CASCADE;
DROP TABLE IF EXISTS category_tasks CASCADE;
DROP TABLE IF EXISTS market_categories CASCADE;
DROP TABLE IF EXISTS markets CASCADE;
DROP TABLE IF EXISTS merchandisers CASCADE;
DROP TABLE IF EXISTS supervisors CASCADE;

-- Confirmación
SELECT 'Base de datos eliminada exitosamente. Ejecuta init.sql y migration_categories_cache.sql para recrearla.' AS message;
