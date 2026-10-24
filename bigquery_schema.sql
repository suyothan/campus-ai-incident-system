-- ====================================================================
-- Google BigQuery Schema & Analytical Queries
-- Project: CampusAI - Multimodal Infrastructure & Incident Diagnostics
-- Architecture: Cloud Run + GCS + Vertex AI + Firestore + BigQuery + Looker Studio
-- ====================================================================

-- 1. Create Dataset
CREATE SCHEMA IF NOT EXISTS `campus_incidents_analytics`
OPTIONS(
  location="US",
  description="Enterprise analytical data warehouse for campus facility incidents"
);

-- 2. Create Incident Events Fact Table (Streamed from Firestore)
CREATE OR REPLACE TABLE `campus_incidents_analytics.incident_events` (
    incident_id STRING NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    student_name STRING,
    roll_no STRING,
    department STRING,
    building STRING,
    room STRING,
    title STRING,
    category STRING,
    severity STRING,
    hazard_detected BOOLEAN,
    hazard_type STRING,
    status STRING,
    assigned_technician STRING,
    confidence_score INT64,
    resolved_at TIMESTAMP
);

-- ====================================================================
-- ANALYTICAL QUERIES (Used by Looker Studio & Executive Dashboard)
-- ====================================================================

-- QUERY 1: Mean Time to Resolution (MTTR) & Incident Velocity
SELECT 
    department,
    COUNT(incident_id) AS total_incidents,
    COUNTIF(severity = 'Critical') AS critical_hazards,
    ROUND(AVG(TIMESTAMP_DIFF(COALESCE(resolved_at, CURRENT_TIMESTAMP()), created_at, MINUTE)) / 60.0, 2) AS avg_resolution_hours,
    ROUND(COUNTIF(status = 'Resolved') * 100.0 / COUNT(incident_id), 1) AS resolution_rate_pct
FROM 
    `campus_incidents_analytics.incident_events`
GROUP BY 
    department
ORDER BY 
    total_incidents DESC;


-- QUERY 2: Campus Building Incident Heatmap & Recurrence Frequency
SELECT 
    building,
    category,
    COUNT(1) AS failure_frequency,
    ARRAY_AGG(room ORDER BY created_at DESC LIMIT 3) AS frequent_failure_locations
FROM 
    `campus_incidents_analytics.incident_events`
GROUP BY 
    building, category
ORDER BY 
    failure_frequency DESC;


-- QUERY 3: Daily Incident Inflow vs Resolution Burn-Down (Looker Studio Line Chart)
SELECT 
    DATE(created_at) AS report_date,
    COUNT(1) AS daily_reported_count,
    COUNTIF(status = 'Resolved') AS daily_resolved_count
FROM 
    `campus_incidents_analytics.incident_events`
GROUP BY 
    report_date
ORDER BY 
    report_date ASC;
