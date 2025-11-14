import numpy as np
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt
import pandas as pd
import os

def run_tips(csv_path):
    df = pd.read_csv(csv_path)

    if "Units_Consumed_kWh" not in df.columns:
        raise ValueError("CSV must contain column 'Units_Consumed_kWh'.")

    df = df.reset_index(drop=True).copy()
    df["y"] = df["Units_Consumed_kWh"]
    df["month_index"] = np.arange(1, len(df) + 1)
    df["usage_change"] = df["y"].diff().fillna(0)
    avg_usage = df["y"].mean()

    def usage_class(v):
        if v < avg_usage * 0.9: return 0
        elif v < avg_usage * 1.1: return 1
        else: return 2

    df["category"] = df["y"].apply(usage_class)

    X = df[["month_index", "y", "usage_change"]].values
    y_label = df["category"].values

    tree = DecisionTreeClassifier(max_depth=3, random_state=42)
    tree.fit(X, y_label)

    predicted_class = int(tree.predict(X[-1].reshape(1, -1))[0])

    classes = ["Low", "Medium", "High"]

    tips_map = {
        0: ["Your usage is low. Keep conserving energy.", "Turn off appliances when not in use."],
        1: ["Your usage is stable.", "Switch to LED bulbs."],
        2: ["High usage detected.", "Check AC filters and heavy appliances."]
    }

    out = {
        "predicted_class": predicted_class,
        "category": classes[predicted_class],
        "tips": tips_map[predicted_class]
    }

    forecast_dir = os.path.join(os.path.dirname(__file__), "forecast")
    os.makedirs(forecast_dir, exist_ok=True)
    path = os.path.join(forecast_dir, "tips_tree.png")

    plt.figure(figsize=(8,5))
    plot_tree(
        tree,
        feature_names=["month_index", "usage", "usage_change"],
        class_names=classes,
        filled=True,
        rounded=True
    )
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

    return out
