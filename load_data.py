import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import os
import sys

DB_USER = "root"
DB_PASSWORD = quote_plus("Zayahaya@1806")
DB_HOST = "127.0.0.1"
DB_PORT = "3306"
DB_NAME = "traffic_crash_db"

CSV_PATH = "Traffic_CrashesData.csv"
TABLE_NAME = "CrashTable"

def load_csv_to_mysql():
    if not os.path.exists(CSV_PATH):
        print(f"[ERROR] CSV file not found: {CSV_PATH}")
        sys.exit(1)

    print(f"[INFO] Reading CSV: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH, low_memory=False)

    print(f"[INFO] Rows loaded: {len(df):,}")
    print(f"[INFO] Columns loaded: {len(df.columns)}")

    # Normalize column names
    df.columns = [c.strip().upper().replace(" ", "_") for c in df.columns]

    engine = create_engine(
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    print("[INFO] Loading data into MySQL...")

    df.to_sql(
        TABLE_NAME,
        engine,
        if_exists="replace",
        index=False,
        chunksize=5000,
        method="multi"
    )

    print(f"[SUCCESS] Table '{TABLE_NAME}' created successfully.")
    print("[SUCCESS] Data imported into MySQL.")

if __name__ == "__main__":
    load_csv_to_mysql()