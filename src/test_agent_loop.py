# test_agent_loop.py

from sensors import get_sensor_data
from actions import speak, send_text_to_contacts, get_nearest_safe_location, log_event_to_file
from memory import Memory

# Initialize memory
memory = Memory()

# Step 1: Simulate sensor input
sensor_data = get_sensor_data()
transcript = sensor_data.get("transcript", "")
memory.log_transcript(transcript)
flags = sensor_data.get("flags", {})
location = sensor_data.get("location", "Unknown")

# ✅ Log transcript and update flags
memory.log_transcript(transcript)
memory.update_flags(flags)

# Step 2: Greet and respond
speak("I'm here. Are you okay?")
memory.log_response("Asked user if okay.")

# Step 3: Check danger flags and take action
if flags.get("is_danger", False) or flags.get("is_danger_mode", False):
    # ✅ Update memory to reflect danger mode
    memory.update_flags({"is_danger_mode": True})
    
    speak("I'm alerting your emergency contacts now.")
    send_text_to_contacts()
    memory.log_response("Sent alert to contacts.")

    safe_location = get_nearest_safe_location(location)
    speak(f"Try heading toward: {safe_location}")
    memory.log_response(f"Suggested safe place: {safe_location}")
else:
    memory.log_response("No danger detected.")

# Step 4: Log full event for audit
log_event_to_file(sensor_data)

# Step 5: Summarize internal memory
memory.summarize()
