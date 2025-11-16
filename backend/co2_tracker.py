import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

DATA_FOLDER = os.path.join(os.path.dirname(__file__), "data")
PLOT_FOLDER = os.path.join(os.path.dirname(__file__), "forecast")
os.makedirs(PLOT_FOLDER, exist_ok=True)

def generate_co2_plot(filename):
    path = os.path.join(DATA_FOLDER, filename)
    df = pd.read_csv(path)

    df.columns = df.columns.str.strip().str.replace(" ", "_").str.replace("-", "_")

    df['Units_Consumed_kWh'] = pd.to_numeric(df['Units_Consumed_kWh'], errors='coerce').fillna(0)
    df.loc[df['Units_Consumed_kWh'] < 0, 'Units_Consumed_kWh'] = 0

    df['Date'] = pd.to_datetime(df['Billing_Period_End'], errors='coerce')
    df = df.dropna(subset=['Date'])

    df['CO2_kg'] = df['Units_Consumed_kWh'] * 0.233
    df = df.sort_values("Date")

    X = np.array(df['Date'].map(pd.Timestamp.toordinal)).reshape(-1, 1)
    y = df['CO2_kg'].values

    model = LinearRegression()
    model.fit(X, y)

    y_pred = model.predict(X)

    plt.figure(figsize=(10, 5))
    plt.plot(df['Date'], y, marker='o', label="Actual CO₂")
    plt.plot(df['Date'], y_pred, linestyle='--', label="Regression Trend")
    plt.xlabel("Date")
    plt.ylabel("CO₂ (kg)")
    plt.title("CO₂ Emissions Linear Regression Trend")
    plt.legend()
    plt.tight_layout()

    output_file = os.path.join(PLOT_FOLDER, "co2_plot.png")
    plt.savefig(output_file)
    plt.close()

    return "co2_plot.png"
