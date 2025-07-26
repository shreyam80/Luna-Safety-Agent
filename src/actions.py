# actions.py
# This module performs real-world actions (mocked for testing)

from datetime import datetime
from src.supabase_client import get_user_by_username, get_emergency_contacts, log_safety_event

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
import os
from dotenv import load_dotenv

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


from twilio.rest import Client

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(account_sid, auth_token)

# 2. Notify user’s emergency contacts
def send_text_to_contacts():
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

from src.memory import memory

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
    if not memory.get_flag("is_silent_mode"):
        print("🗣️ Luna is already in talking mode.")
        return

    # Step 1: Flip the flag
    memory.update_flags({"is_silent_mode": False})
    
    # Step 2: Log the safety event
    username = "shreya"  # Eventually make this dynamic
    log_safety_event(username, event_type="talking_resumed", details="Luna has resumed talking mode.")

    # Step 3: Confirm to user
    print("✅ Luna will now begin speaking again.")
    
    # Step 4: Mark the action done
    memory.update_action_done("start_talking", "")

def call_police():
    username = "shreya"  # You can parameterize this later
    user = get_user_by_username(username)
    phone_number = user.get("phone_number")  # User’s own phone for now

    if not phone_number:
        print("🚫 No phone number available to call.")
        return

    try:
        call = client.calls.create(
            to=phone_number,
            from_=twilio_number,
            twiml='<Response><Say voice="alice">This is Luna. The user may be in danger. Authorities are being contacted.</Say></Response>'
        )
        print(f"📞 Call initiated to police/user. SID: {call.sid}")

        # Log safety event in DB
        log_safety_event(user_id=user["id"], event_type="call_police", notes="Police called by Luna")

        # Update memory
        memory.update_action_done("call_police", {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "phone_called": phone_number,
            "sid": call.sid
        })

    except Exception as e:
        print(f"❌ Failed to call police: {e}")

def get_nearest_safe_location():
    return {
        "name": "Bright Cafe",
        "distance_meters": 50,
        "description": "Open cafe with people around"
    }
