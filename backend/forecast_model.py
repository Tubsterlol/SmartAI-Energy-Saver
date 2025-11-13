import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns
import os

from utils import read_csv, save_json, pretty_print

def run_forecast(rate_per_unit: float = 6.0):
    pretty_print("Running Linear Regression Forecast")

    df = read_csv("bills.csv")

    if "ds" not in df.columns or "y" not in df.columns:
        raise ValueError("CSV must contain 'ds' (date) and 'y' (usage).")

    df = df.reset_index(drop=True).copy()
    df["month_index"] = np.arange(1, len(df) + 1)

    X = df[["month_index"]].values
    y = df["y"].values

    model = LinearRegression()
    model.fit(X, y)

    # Predict next month
    next_index = np.array([[len(df) + 1]])
    predicted_usage = float(model.predict(next_index)[0])
    predicted_bill = float(predicted_usage * rate_per_unit)

    # Regression line for plot
    y_pred = model.predict(X)

    # Save JSON
    save_json("forecast.json", {
        "previous_months": df.to_dict(orient="records"),
        "predicted_usage_kWh": round(predicted_usage, 2),
        "predicted_bill_inr": round(predicted_bill, 2),
        "rate_per_unit": rate_per_unit
    })

    # Save plot
    plot_path = os.path.join(os.path.dirname(__file__), "data", "forecast_plot.png")
    plt.figure(figsize=(7,4))
    sns.lineplot(x=df["month_index"], y=df["y"], marker="o", label="Actual")
    sns.lineplot(x=df["month_index"], y=y_pred, label="Trend Line")
    plt.scatter(len(df)+1, predicted_usage, color="red", label="Next Month")
    plt.title("Electricity Usage Forecast (Linear Regression)")
    plt.xlabel("Month Index")
    plt.ylabel("Usage (kWh)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()

    print("✅ forecast.json created")
    print("✅ forecast_plot.png created")
    print(f"Predicted next month: {predicted_usage:.2f} kWh → ₹{predicted_bill:.2f}")

if __name__ == "__main__":
    run_forecast()
