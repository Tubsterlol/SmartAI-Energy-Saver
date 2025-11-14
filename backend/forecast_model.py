import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.linear_model import LinearRegression
from utils import read_csv, save_json, clean_data, FORECAST_DIR

def run_forecast(filepath: str, rate_per_unit: float = 6.0) -> dict:
    df = read_csv(filepath)
    df = clean_data(df)
    y_col = "Units_Consumed_kWh"
    if y_col not in df.columns:
        raise ValueError(f"{y_col} not found in CSV")
    df = df.reset_index(drop=True)
    df["month_index"] = np.arange(1, len(df) + 1)
    X = df[["month_index"]].values
    y = df[y_col].values
    model = LinearRegression()
    model.fit(X, y)
    next_index = np.array([[len(df) + 1]])
    predicted_usage = float(model.predict(next_index)[0])
    predicted_bill = float(predicted_usage * rate_per_unit)
    y_pred = model.predict(X)
    save_json("forecast.json", {
        "previous_months": df.to_dict(orient="records"),
        "predicted_usage_kWh": round(predicted_usage, 2),
        "predicted_bill_inr": round(predicted_bill, 2),
        "rate_per_unit": rate_per_unit
    })
    plot_path = os.path.join(FORECAST_DIR, "forecast_plot.png")
    plt.figure(figsize=(7, 4))
    sns.lineplot(x=df["month_index"], y=y, marker="o", label="Actual")
    sns.lineplot(x=df["month_index"], y=y_pred, label="Trend Line")
    plt.scatter(len(df) + 1, predicted_usage, color="red", label="Next Month")
    plt.title("Electricity Usage Forecast (Linear Regression)")
    plt.xlabel("Month Index")
    plt.ylabel("Usage (kWh)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()
    return {
        "predicted_usage_kWh": round(predicted_usage, 2),
        "predicted_bill_inr": round(predicted_bill, 2)
    }
