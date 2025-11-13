import numpy as np
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt
import os

from utils import read_csv, save_json, pretty_print

def generate_tips():
    pretty_print("Generating Energy Tips (Decision Tree)")

    df = read_csv("bills.csv")

    if "y" not in df.columns:
        raise ValueError("CSV must contain column 'y'.")

    df = df.reset_index(drop=True).copy()
    df["month_index"] = np.arange(1, len(df) + 1)
    df["usage_change"] = df["y"].diff().fillna(0)

    avg_usage = df["y"].mean()

    # Label usage levels
    def usage_class(y):
        if y < avg_usage * 0.9: return 0   # Low
        elif y < avg_usage * 1.1: return 1 # Medium
        else: return 2                     # High

    df["category"] = df["y"].apply(usage_class)

    # Train Tree
    X = df[["month_index", "y", "usage_change"]].values
    y_label = df["category"].values

    tree = DecisionTreeClassifier(max_depth=3, random_state=42)
    tree.fit(X, y_label)

    # Predict for latest
    predicted_class = int(tree.predict(X[-1].reshape(1, -1))[0])

    class_names = ["Low", "Medium", "High"]

    tips_map = {
        0: [
            "🌿 Your usage is lower than average. Great work!",
            "💡 Continue switching off appliances when not needed."
        ],
        1: [
            "⚡ Usage stable. Switch to LED bulbs to save ₹200/month.",
            "🔌 Unplug chargers to avoid standby wastage."
        ],
        2: [
            "⚠️ High usage detected — check AC filters and heavy appliances.",
            "🧺 Use washing machine during off-peak hours."
        ],
    }

    save_json("tips.json", {
        "predicted_class": predicted_class,
        "category": class_names[predicted_class],
        "tips": tips_map[predicted_class]
    })

   
    path = os.path.join(os.path.dirname(__file__), "data", "decision_tree.png")
    plt.figure(figsize=(8,5))
    plot_tree(
        tree,
        feature_names=["month_index", "usage", "usage_change"],
        class_names=class_names,
        filled=True,
        rounded=True
    )
    plt.title("Decision Tree for Tip Classification")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

    print("✅ tips.json created")
    print("✅ decision_tree.png created")

if __name__ == "__main__":
    generate_tips()
