from forecast_model import run_forecast
from generate_tips import generate_tips
from co2_tracker import calculate_co2
from utils import pretty_print

if __name__ == "__main__":
    pretty_print("SmartAI Backend — Running All Modules")
    run_forecast()
    generate_tips()
    calculate_co2()
    pretty_print("All outputs saved in backend/data/")
