CREATE DATABASE IF NOT EXISTS healthops_team4;
USE healthops_team4;

DROP TABLE IF EXISTS fact_er_visits;
DROP TABLE IF EXISTS dim_bed_inventory;
DROP TABLE IF EXISTS dim_staff;
DROP TABLE IF EXISTS dim_department;

CREATE TABLE dim_department (
    department_id INT PRIMARY KEY,
    department VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE dim_staff (
    staff_id VARCHAR(50) PRIMARY KEY,
    staff_role VARCHAR(50),
    department VARCHAR(100)
);

CREATE TABLE dim_bed_inventory (
    department VARCHAR(100) PRIMARY KEY,
    total_beds INT NOT NULL
);

CREATE TABLE fact_er_visits (
    visit_id VARCHAR(50) PRIMARY KEY,
    patient_id VARCHAR(50),
    department_id INT,
    staff_id VARCHAR(50),
    arrival_time DATETIME,
    triage_time DATETIME,
    doctor_seen_time DATETIME,
    discharge_time DATETIME,
    shift VARCHAR(20),
    beds_occupied INT,
    beds_total INT,
    er_wait_minutes DECIMAL(10,2),
    triage_wait_minutes DECIMAL(10,2),
    length_of_stay_minutes DECIMAL(10,2),
    occupancy_rate DECIMAL(8,4),
    patients_seen INT,
    FOREIGN KEY (department_id) REFERENCES dim_department(department_id),
    FOREIGN KEY (staff_id) REFERENCES dim_staff(staff_id)
);

CREATE OR REPLACE VIEW vw_hourly_ops_kpis AS
SELECT
    DATE_FORMAT(arrival_time, '%Y-%m-%d %H:00:00') AS hour_bucket,
    department_id,
    COUNT(*) AS er_visits,
    AVG(er_wait_minutes) AS avg_er_wait_minutes,
    AVG(occupancy_rate) AS avg_occupancy_rate,
    COUNT(DISTINCT staff_id) AS staff_count,
    SUM(patients_seen) / NULLIF(COUNT(DISTINCT staff_id), 0) AS patients_per_staff
FROM fact_er_visits
GROUP BY DATE_FORMAT(arrival_time, '%Y-%m-%d %H:00:00'), department_id;

CREATE OR REPLACE VIEW vw_shift_performance AS
SELECT
    d.department,
    f.shift,
    COUNT(*) AS visits,
    AVG(f.er_wait_minutes) AS avg_er_wait_minutes,
    AVG(f.occupancy_rate) AS avg_occupancy_rate,
    SUM(f.patients_seen) AS patients_seen,
    COUNT(DISTINCT f.staff_id) AS staff_count,
    SUM(f.patients_seen) / NULLIF(COUNT(DISTINCT f.staff_id), 0) AS patients_per_staff
FROM fact_er_visits f
JOIN dim_department d ON f.department_id = d.department_id
GROUP BY d.department, f.shift;

