# Databricks notebook source
from pyspark.sql import functions as F

silver_path = "/tmp/healthops/team4/silver_ops"
gold_hourly_path = "/tmp/healthops/team4/gold_hourly_kpis"
gold_shift_path = "/tmp/healthops/team4/gold_shift_kpis"

df = spark.read.format("delta").load(silver_path)

hourly_kpis = (
    df.groupBy("hour_bucket", "department")
    .agg(
        F.count("visit_id").alias("er_visits"),
        F.avg("er_wait_minutes").alias("avg_er_wait_minutes"),
        F.avg("occupancy_rate").alias("avg_occupancy_rate"),
        F.countDistinct("staff_id").alias("staff_count"),
        F.sum("patients_seen").alias("patients_seen"),
    )
    .withColumn("patients_per_staff", F.col("patients_seen") / F.col("staff_count"))
)

shift_kpis = (
    df.groupBy("department", "shift")
    .agg(
        F.count("visit_id").alias("visits"),
        F.avg("er_wait_minutes").alias("avg_er_wait_minutes"),
        F.avg("occupancy_rate").alias("avg_occupancy_rate"),
        F.countDistinct("staff_id").alias("staff_count"),
        F.sum("patients_seen").alias("patients_seen"),
    )
    .withColumn("patients_per_staff", F.col("patients_seen") / F.col("staff_count"))
    .withColumn(
        "load_status",
        F.when(F.col("avg_occupancy_rate") >= 0.90, "Critical")
        .when(F.col("avg_occupancy_rate") >= 0.80, "High")
        .otherwise("Normal"),
    )
)

hourly_kpis.write.mode("overwrite").format("delta").save(gold_hourly_path)
shift_kpis.write.mode("overwrite").format("delta").save(gold_shift_path)

display(hourly_kpis)
display(shift_kpis)

