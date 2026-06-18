# Viva Questions and Answers

1. What is the main goal of your project?
Answer: To optimize bed occupancy, ER wait times, and staff efficiency using historical hospital operations data.

2. Why did you use a star schema?
Answer: A star schema makes analytics faster and clearer by keeping measurable events in a fact table and descriptive attributes in dimensions.

3. What is the fact table?
Answer: `fact_er_visits`, because each row represents an ER/hospital visit event with wait time, occupancy, staff, and shift measures.

4. What is bed occupancy rate?
Answer: It is occupied beds divided by total available beds.

5. How did Python help?
Answer: Python was used for EDA, timestamp conversion, feature engineering, hourly resampling, KPI creation, and forecasting.

6. Why use Databricks?
Answer: Databricks supports scalable PySpark processing and a Bronze/Silver/Gold medallion architecture for reliable analytics pipelines.

7. What is the difference between Bronze, Silver, and Gold?
Answer: Bronze is raw data, Silver is cleaned and enriched data, and Gold contains business-ready KPI tables.

8. Which Power BI visuals are most important?
Answer: Occupancy gauge, ER wait trend line chart, shift performance bar chart, department heatmap, and KPI cards.

9. What model did you use for forecasting?
Answer: A Linear Regression baseline using time, visit, wait-time, staff, and lag features. It can later be upgraded to ARIMA or Prophet.

10. What is patients per staff?
Answer: It measures staff workload by dividing patients seen by the number of active staff members.

