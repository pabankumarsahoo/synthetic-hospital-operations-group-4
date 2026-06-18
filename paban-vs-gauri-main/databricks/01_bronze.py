# Databricks notebook source
# Team 4 Bronze: raw ingest
raw_path = "/FileStore/healthops/team4/hospital_ops_sample.csv"
bronze_path = "/tmp/healthops/team4/bronze_ops"

df_raw = (
    spark.read.option("header", True)
    .option("inferSchema", True)
    .csv(raw_path)
)

df_raw.write.mode("overwrite").format("delta").save(bronze_path)
display(df_raw)

