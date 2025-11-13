import os
import json
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def read_csv(filename: str) -> pd.DataFrame:
    
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"{filename} not found in {DATA_DIR}")
    return pd.read_csv(path)

def save_json(filename: str, data):
    
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def pretty_print(title: str):
    print(f"\n{'='*15} {title} {'='*15}\n")
