-- Add AI detection results field to fault_reports
-- Run in Supabase SQL Editor

-- Add new column for AI detection results
ALTER TABLE fault_reports 
ADD COLUMN IF NOT EXISTS ai_detection_results jsonb;

-- Add index for AI analysis queries
CREATE INDEX IF NOT EXISTS idx_faults_ai_results ON fault_reports USING GIN (ai_detection_results);
