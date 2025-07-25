from schema import InputData
from actions import speak, send_text_to_contacts, call_emergency_services, get_location
import re

# This function executes each subtask based on its name
def execute_plan(subtasks: list, input_data: InputData):
    for task in subtasks:
        print(f"[Executor] Running task: {task}")

        # Handle speak("...") command
        if task.startswith("speak("):
            # Extract text using regex
            match = re.match(r"speak\(\"(.+)\"\)", task)
            if match:
                message = match.group(1)
                speak(message)
        
        elif task == "send_text_to_contacts()":
            send_text_to_contacts(input_data.permanent_flags["contacts"], input_data.transcript)

        elif task == "call_emergency_services()":
            call_emergency_services()

        elif task == "get_location()":
            location = get_location()
            print(f"[Executor] Location fetched: {location}")

        else:
            print(f"[Executor] Unknown task: {task}")
