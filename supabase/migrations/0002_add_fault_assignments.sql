-- Add assignment workflow fields to fault_reports
-- Run in Supabase SQL Editor

-- Add new columns for assignment workflow
ALTER TABLE fault_reports 
ADD COLUMN IF NOT EXISTS assigned_to uuid REFERENCES profiles(id),
ADD COLUMN IF NOT EXISTS assigned_at timestamptz,
ADD COLUMN IF NOT EXISTS due_date timestamptz;

-- Update status check constraint to include 'in_progress'
ALTER TABLE fault_reports 
DROP CONSTRAINT IF EXISTS fault_reports_status_check;

ALTER TABLE fault_reports 
ADD CONSTRAINT fault_reports_status_check 
CHECK (status IN ('open','assigned','in_progress','resolved'));

-- Add index for assigned_to queries
CREATE INDEX IF NOT EXISTS idx_faults_assigned_to ON fault_reports(assigned_to);
CREATE INDEX IF NOT EXISTS idx_faults_status ON fault_reports(status);
CREATE INDEX IF NOT EXISTS idx_faults_due_date ON fault_reports(due_date);
