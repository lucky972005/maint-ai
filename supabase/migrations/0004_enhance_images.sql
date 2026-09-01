-- Enhanced image support for machines and parts
-- Run in Supabase SQL Editor

-- Add additional image fields to machines table
ALTER TABLE machines 
ADD COLUMN IF NOT EXISTS images text[],
ADD COLUMN IF NOT EXISTS thumbnail_url text,
ADD COLUMN IF NOT EXISTS primary_image_index int DEFAULT 0;

-- Add additional image fields to parts table  
ALTER TABLE parts
ADD COLUMN IF NOT EXISTS images text[],
ADD COLUMN IF NOT EXISTS thumbnail_url text,
ADD COLUMN IF NOT EXISTS primary_image_index int DEFAULT 0;

-- Add indexes for image queries
CREATE INDEX IF NOT EXISTS idx_machines_images ON machines USING GIN (images);
CREATE INDEX IF NOT EXISTS idx_parts_images ON parts USING GIN (images);
