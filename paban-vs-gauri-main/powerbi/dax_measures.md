# Team 4 DAX Measures

Create these measures after loading `fact_er_visits`, `dim_department`, `dim_staff`, and `dim_bed_inventory`.

```DAX
Total ER Visits = COUNTROWS(fact_er_visits)

Average ER Wait Minutes = AVERAGE(fact_er_visits[er_wait_minutes])

Average Occupancy Rate = AVERAGE(fact_er_visits[occupancy_rate])

Bed Occupancy % = FORMAT([Average Occupancy Rate], "0.0%")

Total Patients Seen = SUM(fact_er_visits[patients_seen])

Active Staff = DISTINCTCOUNT(fact_er_visits[staff_id])

Patients Per Staff = DIVIDE([Total Patients Seen], [Active Staff])

Critical Occupancy Flag =
IF([Average Occupancy Rate] >= 0.9, "Critical", IF([Average Occupancy Rate] >= 0.8, "High", "Normal"))

Peak Hour Visits =
MAXX(
    SUMMARIZE(fact_er_visits, fact_er_visits[arrival_time], "Visits", COUNTROWS(fact_er_visits)),
    [Visits]
)
```

