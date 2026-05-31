-- 1. Nueva Tabla: Categorías de Mercado
CREATE TABLE IF NOT EXISTS market_categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) NOT NULL UNIQUE,
    display_name VARCHAR(100) NOT NULL,
    icon_name VARCHAR(50) NOT NULL
);

-- 2. Nueva Tabla: Tareas Específicas por Categoría
DROP TABLE IF EXISTS category_tasks CASCADE;
CREATE TABLE category_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category_id UUID NOT NULL REFERENCES market_categories(id) ON DELETE CASCADE,
    task_description VARCHAR(255) NOT NULL,
    estimated_time_mins INT NOT NULL
);

-- 3. Nueva Tabla: Caché de Rutas Optimizadas
CREATE TABLE IF NOT EXISTS optimized_routes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    origin_lat NUMERIC(12,8) NOT NULL,
    origin_lng NUMERIC(12,8) NOT NULL,
    destination_ids_hash VARCHAR(64) NOT NULL,
    optimized_path_json JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_optimized_routes_hash ON optimized_routes(destination_ids_hash);

-- 4. Modificación de la Tabla 'markets' Existente
ALTER TABLE markets ADD COLUMN IF NOT EXISTS category_id UUID REFERENCES market_categories(id);

-- =========================================================================
-- SEED DATA: Inicialización de Categorías, Íconos y Tareas
-- =========================================================================

-- Inserción de Categorías con mapeo visual requerido
INSERT INTO market_categories (id, name, display_name, icon_name) VALUES
('a0000000-0000-0000-0000-000000000001', 'Mayorista', 'Mayorista', 'corporate_fare'),
('a0000000-0000-0000-0000-000000000002', 'Detallista normal', 'Detallista', 'storefront'),
('a0000000-0000-0000-0000-000000000003', 'Detallista Pareto', 'Detallista Pareto', 'storefront_star')
ON CONFLICT (id) DO NOTHING;

-- Inserción de Tareas por Categoría
-- Categoría: Mayorista (Tiempo estimado: 45 a 55 min)
INSERT INTO category_tasks (category_id, task_description, estimated_time_mins) VALUES
('a0000000-0000-0000-0000-000000000001', 'Verificar stock general', 8),
('a0000000-0000-0000-0000-000000000001', 'Revisar disponibilidad por línea de producto', 8),
('a0000000-0000-0000-0000-000000000001', 'Reposición o acomodo de producto', 18),
('a0000000-0000-0000-0000-000000000001', 'Revisar exhibición o ubicación del producto', 8),
('a0000000-0000-0000-0000-000000000001', 'Verificar material POP', 5),
('a0000000-0000-0000-0000-000000000001', 'Registrar observaciones', 5);

-- Categoría: Detallista normal (Tiempo estimado: 20 a 30 min)
INSERT INTO category_tasks (category_id, task_description, estimated_time_mins) VALUES
('a0000000-0000-0000-0000-000000000002', 'Verificar disponibilidad de producto', 5),
('a0000000-0000-0000-0000-000000000002', 'Reposición básica', 10),
('a0000000-0000-0000-0000-000000000002', 'Orden y limpieza rápida', 5),
('a0000000-0000-0000-0000-000000000002', 'Revisar material POP básico', 3),
('a0000000-0000-0000-0000-000000000002', 'Registrar observación rápida', 2);

-- Categoría: Detallista Pareto (Tiempo estimado: 50 a 60 min)
INSERT INTO category_tasks (category_id, task_description, estimated_time_mins) VALUES
('a0000000-0000-0000-0000-000000000003', 'Verificar stock disponible', 8),
('a0000000-0000-0000-0000-000000000003', 'Revisar quiebres de stock', 7),
('a0000000-0000-0000-0000-000000000003', 'Reposición de productos', 15),
('a0000000-0000-0000-0000-000000000003', 'Orden y limpieza del espacio', 8),
('a0000000-0000-0000-0000-000000000003', 'Revisión de exhibición principal', 8),
('a0000000-0000-0000-0000-000000000003', 'Verificar material POP', 5),
('a0000000-0000-0000-0000-000000000003', 'Registrar observaciones del PDV', 5);
