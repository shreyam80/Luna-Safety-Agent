# executor.py
from src.actions import (
    speak,
    send_text_to_contacts,
    call_police,
    get_nearest_safe_location,
    record_voice_and_location,
    stay_silent,
    start_talking
)
from src.memory import memory

# Execute each subtask returned by the planner
def execute_subtasks(subtasks, memory):
    for task in subtasks:
        action = task.get("action")
        text = task.get("text")  # This may be None for actions that don’t need it

        # 1. Speak the explanation if provided
        if action != "stay_silent" and memory.get_flag("is_silent_mode") == False and text:
            speak(text)

        # 2. Handle each supported action
        if action == "speak":
            # Already handled by text-to-speech above
            continue

        elif action == "send_text_to_contacts":
            if not memory.was_action_done("send_text_to_contacts"):
                send_text_to_contacts()
                memory.update_action_done("send_text_to_contacts", True)
            else:
                print("Skipping: Already notified contacts.")

        elif action == "call_police":
            if not memory.was_action_done("call_police"):
                # This assumes user confirmation was already obtained
                call_police()
                memory.update_action_done("call_police", True)
            else:
                print("Skipping: Already called police.")

        elif action == "record_voice_and_location":
            record_voice_and_location()

        elif action == "guide_to_safety":
            # This assumes user said yes to guide
            get_nearest_safe_location()

        elif action == "stay_silent":
            memory.update_flags({"is_silent_mode": True})
            print("Luna will stay silent until told to speak.")

        elif action == "start_talking":
            memory.update_flags({"is_silent_mode": False})
            speak("I'm here again. Let me know if you need help.")

        else:
            print(f"Unknown action: {action}")
