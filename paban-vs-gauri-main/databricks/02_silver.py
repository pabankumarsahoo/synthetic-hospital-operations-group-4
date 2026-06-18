# Databricks notebook source
from pyspark.sql import functions as F

bronze_path = "/tmp/healthops/team4/bronze_ops"
silver_path = "/tmp/healthops/team4/silver_ops"

df = spark.read.format("delta").load(bronze_path)

silver = (
    df.withColumn("arrival_time", F.to_timestamp("arrival_time"))
    .withColumn("triage_time", F.to_timestamp("triage_time"))
    .withColumn("doctor_seen_time", F.to_timestamp("doctor_seen_time"))
    .withColumn("discharge_time", F.to_timestamp("discharge_time"))
    .withColumn("er_wait_minutes", (F.col("doctor_seen_time").cast("long") - F.col("arrival_time").cast("long")) / 60)
    .withColumn("triage_wait_minutes", (F.col("triage_time").cast("long") - F.col("arrival_time").cast("long")) / 60)
    .withColumn("length_of_stay_minutes", (F.col("discharge_time").cast("long") - F.col("arrival_time").cast("long")) / 60)
    .withColumn("occupancy_rate", F.col("beds_occupied") / F.col("beds_total"))
    .withColumn("hour_bucket", F.date_trunc("hour", F.col("arrival_time")))
    .withColumn("date", F.to_date("arrival_time"))
)

silver.write.mode("overwrite").format("delta").save(silver_path)
display(silver)

