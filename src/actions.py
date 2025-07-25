# actions.py
# This module performs real-world actions (mocked for testing)

from datetime import datetime

# ✅ Available actions per spec:
# - speak(message)
# - send_text_to_contacts()
# - call_police()
# - get_nearest_safe_location()
# - record_voice_and_location()
# - stay_silent()
# - guide_to_safety()

# 1. Say something to the user
def speak(message):
    print(f"🗣️ Luna says: {message}")

# 2. Notify user’s emergency contacts
def send_text_to_contacts(contact_list=None, message="Luna has detected danger."):
    contact_list = contact_list or ["+1234567890", "+1987654321"]
    print("📤 Sending alert message to contacts:")
    for contact in contact_list:
        print(f"  📱 To: {contact} — Message: {message}")

# 3. Call emergency services (mocked)
def call_police():
    print("🚨 Calling 911... [Mocked call initiated]")

# 4. Suggest a nearby safe location
def get_nearest_safe_location(current_location):
    print(f"🗺️ Finding safe location from: {current_location}")
    return "Starbucks on 5th Ave & 23rd St (open, staffed)"

# 5. Start logging for evidence (mocked)
def record_voice_and_location():
    print("🎙️🛰️ Recording voice and GPS for incident report...")

# 6. Stop talking temporarily
def stay_silent():
    print("🤫 Luna is staying silent until reactivated...")

# 7. Provide step-by-step directions to safety (mocked)
def guide_to_safety(destination):
    print(f"🧭 Guiding to: {destination} — Turn left on 5th Ave, walk 2 blocks, it's on your right.")

# 8. Log the event to a local file
def log_event_to_file(event_data, filename="safety_log.txt"):
    try:
        with open(filename, "a") as file:
            file.write("\n----- EVENT LOG -----\n")
            for key, value in event_data.items():
                file.write(f"{key}: {value}\n")
            file.write(f"Logged at: {datetime.now().isoformat()}\n")
        print(f"📝 Event successfully logged to {filename}")
    except Exception as e:
        print(f"❌ Failed to log event: {e}")

# Example usage
if __name__ == "__main__":
    speak("I'm here with you. Stay calm.")
    send_text_to_contacts()
    call_police()
    safe_spot = get_nearest_safe_location("New York, NY")
    print(f"✅ Safe place: {safe_spot}")
    record_voice_and_location()
    stay_silent()
    guide_to_safety(safe_spot)
    test_event = {
        "transcript": "Help, someone is following me",
        "location": "New York, NY",
        "flags": {"is_danger": True},
    }
    log_event_to_file(test_event)
