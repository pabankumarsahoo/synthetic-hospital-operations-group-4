import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from config import DATASET_PATH, PROCESSED_DIR
from eda import add_features, load_ops_data


def train_forecast():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df = add_features(load_ops_data(DATASET_PATH))
    hourly = (
        df.set_index("arrival_time")
        .resample("h")
        .agg(
            occupancy_rate=("occupancy_rate", "mean"),
            visits=("visit_id", "count"),
            avg_wait_minutes=("er_wait_minutes", "mean"),
            staff_count=("staff_id", "nunique"),
        )
        .ffill()
        .reset_index()
    )
    hourly["hour"] = hourly["arrival_time"].dt.hour
    hourly["dayofweek"] = hourly["arrival_time"].dt.dayofweek
    hourly["lag_1"] = hourly["occupancy_rate"].shift(1)
    hourly["lag_24"] = hourly["occupancy_rate"].shift(24)
    hourly = hourly.dropna()

    if len(hourly) < 5:
        print("Sample data is small. Add the real dataset for a stronger forecast.")
        return

    features = ["visits", "avg_wait_minutes", "staff_count", "hour", "dayofweek", "lag_1", "lag_24"]
    split = int(len(hourly) * 0.8)
    train, test = hourly.iloc[:split], hourly.iloc[split:]
    model = LinearRegression()
    model.fit(train[features], train["occupancy_rate"])
    test = test.copy()
    test["predicted_occupancy_rate"] = model.predict(test[features]).clip(0, 1)
    print("MAE:", round(mean_absolute_error(test["occupancy_rate"], test["predicted_occupancy_rate"]), 4))
    print("R2:", round(r2_score(test["occupancy_rate"], test["predicted_occupancy_rate"]), 4))
    test.to_csv(PROCESSED_DIR / "bed_occupancy_forecast.csv", index=False)


if __name__ == "__main__":
    train_forecast()
