import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from config import DATASET_PATH, PROCESSED_DIR


def load_ops_data(path=DATASET_PATH):
    df = pd.read_csv(path)
    for col in ["arrival_time", "triage_time", "doctor_seen_time", "discharge_time"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def add_features(df):
    df = df.copy()
    df["er_wait_minutes"] = (df["doctor_seen_time"] - df["arrival_time"]).dt.total_seconds() / 60
    df["triage_wait_minutes"] = (df["triage_time"] - df["arrival_time"]).dt.total_seconds() / 60
    df["length_of_stay_minutes"] = (df["discharge_time"] - df["arrival_time"]).dt.total_seconds() / 60
    df["occupancy_rate"] = df["beds_occupied"] / df["beds_total"]
    df["hour"] = df["arrival_time"].dt.hour
    df["date"] = df["arrival_time"].dt.date
    df["weekday"] = df["arrival_time"].dt.day_name()
    return df


def run_eda():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df = add_features(load_ops_data())

    print("\nColumns:")
    print(df.columns.tolist())
    print("\nShape:", df.shape)
    print("\nMissing values:")
    print(df.isna().sum())
    print("\nNumeric summary:")
    print(df.select_dtypes("number").describe())

    hourly = (
        df.set_index("arrival_time")
        .resample("h")
        .agg(
            visits=("visit_id", "count"),
            avg_wait_minutes=("er_wait_minutes", "mean"),
            avg_occupancy_rate=("occupancy_rate", "mean"),
            staff_count=("staff_id", "nunique"),
        )
        .reset_index()
    )
    shift_kpis = (
        df.groupby(["department", "shift"], as_index=False)
        .agg(
            visits=("visit_id", "count"),
            avg_wait_minutes=("er_wait_minutes", "mean"),
            avg_occupancy_rate=("occupancy_rate", "mean"),
            patients_seen=("patients_seen", "sum"),
            staff_count=("staff_id", "nunique"),
        )
    )
    shift_kpis["patients_per_staff"] = shift_kpis["patients_seen"] / shift_kpis["staff_count"]

    df.to_csv(PROCESSED_DIR / "ops_clean.csv", index=False)
    hourly.to_csv(PROCESSED_DIR / "hourly_kpis.csv", index=False)
    shift_kpis.to_csv(PROCESSED_DIR / "shift_kpis.csv", index=False)

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(9, 5))
    sns.lineplot(data=hourly, x="arrival_time", y="avg_wait_minutes", marker="o")
    plt.title("ER Wait Time Trend")
    plt.xticks(rotation=35)
    plt.tight_layout()
    plt.savefig(PROCESSED_DIR / "er_wait_trend.png", dpi=160)

    plt.figure(figsize=(8, 5))
    sns.barplot(data=shift_kpis, x="shift", y="avg_occupancy_rate", hue="department")
    plt.title("Average Bed Occupancy by Shift")
    plt.tight_layout()
    plt.savefig(PROCESSED_DIR / "shift_occupancy.png", dpi=160)

    print(f"\nSaved outputs to: {PROCESSED_DIR}")


if __name__ == "__main__":
    run_eda()
