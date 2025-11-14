import os
import pandas as pd
import json

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
FORECAST_DIR = os.path.join(os.path.dirname(__file__), "forecast")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(FORECAST_DIR, exist_ok=True)

def read_csv(filepath: str) -> pd.DataFrame:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"{filepath} not found")
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.strip().str.replace(" ", "_").str.replace("(", "").str.replace(")", "")
    return df

def save_json(filename: str, data: dict):
    file_path = os.path.join(FORECAST_DIR, filename)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    drop_cols = ["Bill_ID", "Meter_Number", "Provider_Name", "Payment_Status", "Payment_Date"]
    for col in drop_cols:
        if col in df.columns:
            df.drop(col, axis=1, inplace=True)
    numeric_cols = df.select_dtypes(include="number").columns
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(df[col].median())
    return df
