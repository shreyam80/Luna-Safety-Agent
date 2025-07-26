# actions.py
# This module performs real-world actions (mocked for testing)

from datetime import datetime
from supabase_client import get_user_by_username, get_emergency_contacts, log_safety_event

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

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

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

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(account_sid, auth_token)

# 2. Notify user’s emergency contacts
def send_text_to_contacts(contact_list, message="This is Luna. Shreya may be in danger. Please check on them immediately."):
    username = "shreya"

    user = get_user_by_username(username)
    user_id = user.get("id")
    contact_list = get_emergency_contacts(user_id)

    if not contact_list:
        print("🚫 No contacts to notify.")
        return

    for contact in contact_list:
        contact_name = contact.get("contact_name", "Contact")
        contact_phone = contact.get("contact_phone")
        personalized_message = f"Hi {contact_name}, this is Luna. {user['name']} may be in danger. Please check on them immediately."
        try:
            msg = client.messages.create(
                body=personalized_message,
                from_=twilio_number,
                to=contact_phone
            )
            print(f"✅ Message sent to {contact_name}. SID: {msg.sid}")
        except Exception as e:
            print(f"❌ Failed to send message to {contact_phone}: {e}")

import datetime

def record_voice_and_location(location=None):
    now = datetime.datetime.now().isoformat()
    with open("safety_log.txt", "a") as f:
        f.write(f"{now} | Voice & Location Logging Started\n")
        if location:
            f.write(f"{now} | Location: {location}\n")
    print("🎙️ Voice and location logging simulated.")

from memory import memory

def stay_silent(username="shreya"):
    print('activating silent mode')
    user = get_user_by_username(username)
    user_id = user["id"]

    # Log safety event
    log_safety_event(
        user_id=user_id,
        event_type="silent_mode_triggered",
        description="Agent entered silent mode due to danger inference.",
    )

    # Update agent memory
    memory.update_flags({"is_silent_mode": True})
    memory.log_response("Luna is now in silent mode.")

    print("🤫 Silent mode activated.")

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
