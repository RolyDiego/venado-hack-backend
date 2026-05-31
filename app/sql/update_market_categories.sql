-- Script para asignar categorías a los mercados basándose en la categoría de sus clientes
BEGIN;

-- Actualizar mercados con clientes MAYORISTA
UPDATE markets m
SET category_id = 'a0000000-0000-0000-0000-000000000001'
WHERE EXISTS (
    SELECT 1 FROM customers c 
    WHERE c.market_id = m.id AND c.category = 'MAYORISTA'
);

-- Actualizar mercados con clientes MINORISTA
UPDATE markets m
SET category_id = 'a0000000-0000-0000-0000-000000000002'
WHERE EXISTS (
    SELECT 1 FROM customers c 
    WHERE c.market_id = m.id AND c.category = 'MINORISTA'
);

-- Actualizar mercados con clientes DETALLISTA
UPDATE markets m
SET category_id = 'a0000000-0000-0000-0000-000000000003'
WHERE EXISTS (
    SELECT 1 FROM customers c 
    WHERE c.market_id = m.id AND c.category = 'DETALLISTA'
);

COMMIT;

-- Verificación
SELECT m.id, m.name, m.category_id, mc.name as category_name 
FROM markets m 
LEFT JOIN market_categories mc ON m.category_id = mc.id 
LIMIT 10;
