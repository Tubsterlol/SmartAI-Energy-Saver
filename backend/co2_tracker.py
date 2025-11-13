from utils import read_csv, save_json, pretty_print

def calculate_co2():
    pretty_print("Calculating CO₂ + Green Score")

    df = read_csv("bills.csv")

    total_kwh = float(df["y"].sum())
    co2_kg = round(total_kwh * 0.82, 2)  # India's average factor
    green_score = max(0, round(100 - (co2_kg / 10), 2))

    save_json("co2.json", {
        "total_kWh": total_kwh,
        "total_CO2_kg": co2_kg,
        "green_score": green_score
    })

    print("✅ co2.json created")
    print(f"CO₂: {co2_kg} kg | Green Score: {green_score}/100")

if __name__ == "__main__":
    calculate_co2()
