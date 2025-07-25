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

import pyttsx3

# Initialize engine once globally
tts_engine = pyttsx3.init()

def speak(text):
    """
    Use text-to-speech to say the given text out loud.
    """
    print(f"🗣️ Luna says: {text}")
    try:
        tts_engine.say(text)
        tts_engine.runAndWait()
    except Exception as e:
        print("⚠️ Error using text-to-speech:", e)


from dotenv import load_dotenv
from twilio.rest import Client
import os

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(account_sid, auth_token)

# 2. Notify user’s emergency contacts
def send_text_to_contacts(contact_list, message="This is Luna. The user may be in danger. Please check on them immediately."):
    if not contact_list:
        print("🚫 No contacts to notify.")
        return

    for contact in contact_list:
        try:
            msg = client.messages.create(
                body=message,
                from_=twilio_number,
                to=contact
            )
            print(f"✅ Message sent to {contact}. SID: {msg.sid}")
        except Exception as e:
            print(f"❌ Failed to send message to {contact}: {e}")

import datetime

def record_voice_and_location(location=None):
    now = datetime.datetime.now().isoformat()
    with open("safety_log.txt", "a") as f:
        f.write(f"{now} | Voice & Location Logging Started\n")
        if location:
            f.write(f"{now} | Location: {location}\n")
    print("🎙️ Voice and location logging simulated.")

from memory import memory

def stay_silent():
    print("🔇 Luna will stop talking.")
    memory.update_flags({"silent_mode": True})

def start_talking():
    print("🔊 Luna will resume talking.")
    memory.update_flags({"silent_mode": False})

def call_police():
    print("🚨 Simulated 911 call placed.")
    # IRL: Trigger emergency call via Twilio Voice or OS-level call API

def get_nearest_safe_location():
    return {
        "name": "Bright Cafe",
        "distance_meters": 50,
        "description": "Open cafe with people around"
    }
