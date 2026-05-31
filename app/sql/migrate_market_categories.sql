-- Migration script to add market_categories table and category_id to markets
-- Run this on your existing database to fix the missing table

-- Add category_id column to markets table if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'markets' AND column_name = 'category_id'
    ) THEN
        ALTER TABLE markets ADD COLUMN category_id UUID REFERENCES market_categories(id);
    END IF;
END $$;

-- Create market_categories table if it doesn't exist
CREATE TABLE IF NOT EXISTS market_categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) NOT NULL UNIQUE,
    display_name VARCHAR(100) NOT NULL,
    icon_name VARCHAR(50) NOT NULL
);

-- Insert initial market categories if they don't exist
INSERT INTO market_categories (id, name, display_name, icon_name) VALUES
('a0000000-0000-0000-0000-000000000001', 'MAYORISTA', 'Mayorista', 'store'),
('a0000000-0000-0000-0000-000000000002', 'MINORISTA', 'Minorista', 'shopping-cart'),
('a0000000-0000-0000-0000-000000000003', 'DETALLISTA', 'Detallista', 'tag')
ON CONFLICT (name) DO NOTHING;

-- Fix optimized_routes table: add default value for created_at
DO $$
BEGIN
    -- Update existing NULL values to current timestamp
    UPDATE optimized_routes SET created_at = NOW() WHERE created_at IS NULL;

    -- Add default value to the column
    ALTER TABLE optimized_routes ALTER COLUMN created_at SET DEFAULT NOW();
END $$;

-- Update markets with categories based on their customers
-- Update markets with customers MAYORISTA
UPDATE markets m
SET category_id = 'a0000000-0000-0000-0000-000000000001'
WHERE EXISTS (
    SELECT 1 FROM customers c
    WHERE c.market_id = m.id AND c.category = 'MAYORISTA'
) AND m.category_id IS NULL;

-- Update markets with customers MINORISTA
UPDATE markets m
SET category_id = 'a0000000-0000-0000-0000-000000000002'
WHERE EXISTS (
    SELECT 1 FROM customers c
    WHERE c.market_id = m.id AND c.category = 'MINORISTA'
) AND m.category_id IS NULL;

-- Update markets with customers DETALLISTA
UPDATE markets m
SET category_id = 'a0000000-0000-0000-0000-000000000003'
WHERE EXISTS (
    SELECT 1 FROM customers c
    WHERE c.market_id = m.id AND c.category = 'DETALLISTA'
) AND m.category_id IS NULL;
