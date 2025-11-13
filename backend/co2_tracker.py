import os
import pandas as pd

DATA_FOLDER = os.path.join(os.path.dirname(__file__), "../data")

def calculate_co2(df_or_path):
    if isinstance(df_or_path, str):
        path = os.path.join(DATA_FOLDER, df_or_path)
        df = pd.read_csv(path)
    else:
        df = df_or_path

    # Example processing
    df['CO2_kg'] = df['kWh'] * 0.233
    return df.to_dict(orient='records')
