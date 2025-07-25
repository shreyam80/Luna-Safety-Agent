def speak(message: str):
    print(f"[Luna says]: {message}")

def send_text_to_contacts(contacts: list, message: str):
    for number in contacts:
        print(f"[Texting {number}]: {message}")

def call_emergency_services():
    print("[Calling 911]")

def get_location():
    return {"lat": 40.7128, "lon": -74.0060}