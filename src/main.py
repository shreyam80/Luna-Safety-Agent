import time
from schema import InputData
from planner import generate_plan
from executor import execute_plan

# This will simulate incoming sensor data
def simulate_sensor_input():
    return InputData(
        transcript="I think someone is following me",
        location={"lat": 40.7128, "lon": -74.0060},
        location_history=[
            {"lat": 40.7130, "lon": -74.0062},
            {"lat": 40.7135, "lon": -74.0065}
        ],
        speed=2.5,
        is_danger=True,
        permanent_flags={
            "home": {"lat": 40.7110, "lon": -74.0050},
            "contacts": ["+1234567890", "+1098765432"],
            "student": True
        }
    )

def main_loop():
    while True:
        input_data = simulate_sensor_input()

        # Step 1: Generate plan from LLM
        subtasks = generate_plan(input_data)

        # Step 2: Execute those subtasks
        execute_plan(subtasks, input_data)

        # Wait for a few seconds before checking again
        time.sleep(10)

if __name__ == "__main__":
    main_loop()
