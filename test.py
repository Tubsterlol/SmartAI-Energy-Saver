import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
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

    # Proper Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    # Evaluation on test data
    y_test_pred = model.predict(X_test)
    mae = float(mean_absolute_error(y_test, y_test_pred))
    r2 = float(r2_score(y_test, y_test_pred))

    # Forecast next month
    next_index = np.array([[len(df) + 1]])
    predicted_usage = float(model.predict(next_index)[0])
    predicted_bill = float(predicted_usage * rate_per_unit)

    # Prediction for full graph
    y_pred_full = model.predict(X)

    save_json("forecast.json", {
        "previous_months": df.to_dict(orient="records"),
        "predicted_usage_kWh": round(predicted_usage, 2),
        "predicted_bill_inr": round(predicted_bill, 2),
        "rate_per_unit": rate_per_unit,
        "mae": round(mae, 2),
        "r2_score": round(r2, 4)
    })

    plot_path = os.path.join(FORECAST_DIR, "forecast_plot.png")

    plt.figure(figsize=(8, 4))

    sns.lineplot(x=df["month_index"], y=y, marker="o", label="Actual")

    sns.lineplot(x=df["month_index"], y=y_pred_full, label="Regression Fit")

    plt.scatter(len(df) + 1, predicted_usage, color="red", s=80, label="Forecast")

    plt.title("Electricity Usage Forecast (Linear Regression)")
    plt.xlabel("Month Index")
    plt.ylabel("Usage (kWh)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()

    return {
        "predicted_usage_kWh": round(predicted_usage, 2),
        "predicted_bill_inr": round(predicted_bill, 2),
        "mae": round(mae, 2),
        "r2_score": round(r2, 4)
    }
