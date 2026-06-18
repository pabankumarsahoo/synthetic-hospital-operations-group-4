from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_DATA = ROOT / "data" / "raw" / "hospital_ops_sample.csv"
PROCESSED_DIR = ROOT / "data" / "processed"

# Update this path when you download the real Team 4 ops dataset.
DATASET_PATH = RAW_DATA

MYSQL_URL = "mysql+pymysql://root:your_password@localhost:3306/healthops_team4"

