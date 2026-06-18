# PPT Content

## Slide 1: Title
HealthOps IQ: Hospital Operations and Resource Management

## Slide 2: Problem
Hospitals need to reduce ER waiting time, avoid bed shortages, and improve staff shift utilization.

## Slide 3: Dataset
Operations data with visit timestamps, department, shift, staff, bed capacity, occupied beds, and patient counts.

## Slide 4: Architecture
CSV data flows into Python EDA, MySQL star schema, Databricks medallion layers, forecasting model, and Power BI dashboard.

## Slide 5: Python EDA
Timestamp parsing, missing-value checks, hourly `.resample()`, ER wait time, occupancy rate, and shift-wise aggregations.

## Slide 6: MySQL Design
Fact table: `fact_er_visits`. Dimensions: `dim_department`, `dim_staff`, `dim_bed_inventory`.

## Slide 7: Databricks
Bronze stores raw data, Silver cleans and derives features, Gold creates hourly and shift-level KPIs.

## Slide 8: KPIs
Average ER wait, occupancy rate, patients per staff, peak hour visits, shift performance, critical occupancy flag.

## Slide 9: Forecasting
Linear Regression baseline predicts occupancy rate using visits, wait time, staff count, hour, weekday, and lag features.

## Slide 10: Power BI Dashboard
Gauge for bed occupancy, wait-time trend, shift performance chart, department heatmap, and slicers for date/department/shift.

## Slide 11: Business Impact
The dashboard helps hospital managers detect crowding early, balance staff shifts, and reduce patient waiting time.

## Slide 12: Future Scope
Use live hospital feeds, stronger ARIMA/Prophet forecasting, automated staff recommendations, and alert notifications.

