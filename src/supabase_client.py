# supabase_client.py
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

# Get user by username
def get_user_by_username(username):
    response = supabase.table("users").select("*").eq("username", username).execute()
    print("RAW RESPONSE:", response)
    users = response.data
    if not users:
        raise ValueError(f"No user found with username: {username}")
    if len(users) > 1:
        raise ValueError(f"Multiple users found with username: {username}")
    return users[0]


# Get emergency contacts by user_id (foreign key in emergency_contacts table)
def get_emergency_contacts(user_id):
    response = supabase.table("emergency_contacts").select("*").eq("user_id", user_id).execute()
    return response.data

def log_safety_event(user_id, event_type, description=None):
    try:
        timestamp = datetime.utcnow().isoformat()
        data = {
            "user_id": user_id,
            "event_type": event_type,
            "timestamp": timestamp,
            "description": description or ""
        }

        response = supabase.table("safety_logs").insert(data).execute()

        if response.data:
            print("📝 Safety event logged.")
        else:
            print("⚠️ Logging safety event failed:", response)
    except Exception as e:
        print(f"❌ Error logging safety event: {e}")









# Example usage
if __name__ == "__main__":
    user = get_user_by_username("shreya")
    print("User:", user)

    if user:
        contacts = get_emergency_contacts(user["id"])
        print("Emergency Contacts:", contacts)
