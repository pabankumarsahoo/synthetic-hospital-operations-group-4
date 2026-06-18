# HealthOps IQ – Hospital Operations & Resource Management

A data-driven analytics project focused on improving hospital operational efficiency through data engineering, analytics, forecasting, and business intelligence.

## Team 4 Members

1. Gouri Shankar Nayak 
2. Paban Kumar Sahoo
3. Binayak Padhiary


## Project Objective

Healthcare organizations face challenges in managing bed occupancy, emergency room wait times, staff allocation, and resource utilization. This project uses Python, MySQL, Databricks, and Power BI to analyze hospital operations and provide actionable insights.

### Key Goals

* Optimize bed occupancy rates
* Reduce emergency room waiting times
* Improve staff shift efficiency
* Forecast future resource requirements
* Create executive dashboards for decision-making

## Technology Stack

* Python
* MySQL
* Databricks Community Edition
* Power BI Desktop
* Git & GitHub

## Project Structure

```text
data/raw/                  Raw hospital operations dataset
data/processed/            Cleaned datasets and KPI outputs
src/                       Python scripts for EDA, ETL and forecasting
sql/                       Database schema and KPI queries
databricks/                Bronze, Silver and Gold layer notebooks
powerbi/                   Dashboard layouts and DAX measures
docs/                      Project report, PPT and documentation
```

## Setup Instructions

### Python Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Run Analytics Pipeline

```powershell
python src\eda.py
python src\forecast_bed_occupancy.py
```

Generated outputs will be stored inside:

```text
data/processed/
```

## MySQL Setup

1. Open `sql/01_schema.sql`
2. Execute the script in MySQL Workbench
3. Update database credentials in `src/config.py`
4. Run:

```powershell
python src\etl_mysql.py
```

## Databricks Workflow

1. Upload dataset to Databricks FileStore
2. Import Bronze notebook
3. Import Silver notebook
4. Import Gold KPI notebook
5. Execute notebooks sequentially

## Power BI Dashboard

Dashboard includes:

* Bed Occupancy Analysis
* ER Wait Time Trends
* Department Performance
* Staff Utilization Metrics
* Forecasting Insights
* Operational KPI Monitoring

## Expected Outcomes

* Better resource allocation
* Reduced patient wait times
* Improved workforce planning
* Enhanced operational visibility
* Data-driven hospital management decisions

## License

Academic Project – Educational Use Only

---

Developed by Team 4 for Hospital Operations & Resource Management.
