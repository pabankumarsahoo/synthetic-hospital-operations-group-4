import pandas as pd
from sqlalchemy import create_engine, text
from config import DATASET_PATH, MYSQL_URL
from eda import add_features, load_ops_data


def build_tables(df):
    dim_department = (
        df[["department"]].drop_duplicates().sort_values("department").reset_index(drop=True)
    )
    dim_department.insert(0, "department_id", range(1, len(dim_department) + 1))

    dim_staff = df[["staff_id", "staff_role", "department"]].drop_duplicates()

    dim_bed_inventory = (
        df[["department", "beds_total"]]
        .drop_duplicates()
        .rename(columns={"beds_total": "total_beds"})
    )

    fact_er_visits = df.merge(dim_department, on="department", how="left")[
        [
            "visit_id",
            "patient_id",
            "department_id",
            "staff_id",
            "arrival_time",
            "triage_time",
            "doctor_seen_time",
            "discharge_time",
            "shift",
            "beds_occupied",
            "beds_total",
            "er_wait_minutes",
            "triage_wait_minutes",
            "length_of_stay_minutes",
            "occupancy_rate",
            "patients_seen",
        ]
    ]
    return dim_department, dim_staff, dim_bed_inventory, fact_er_visits


def load_to_mysql():
    df = add_features(load_ops_data(DATASET_PATH))
    dim_department, dim_staff, dim_bed_inventory, fact_er_visits = build_tables(df)
    engine = create_engine(MYSQL_URL)
    with engine.begin() as conn:
        conn.execute(text("CREATE DATABASE IF NOT EXISTS healthops_team4"))
        conn.execute(text("USE healthops_team4"))
        dim_department.to_sql("dim_department", conn, if_exists="replace", index=False)
        dim_staff.to_sql("dim_staff", conn, if_exists="replace", index=False)
        dim_bed_inventory.to_sql("dim_bed_inventory", conn, if_exists="replace", index=False)
        fact_er_visits.to_sql("fact_er_visits", conn, if_exists="replace", index=False)
    print("Loaded Team 4 star-schema tables into MySQL.")


if __name__ == "__main__":
    load_to_mysql()

