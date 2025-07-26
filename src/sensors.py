
# This module gathers real-world input: (mocked) voice transcription and location data
from datetime import datetime
import time
from src.memory import memory
import threading

# Mocked function to simulate speech-to-text transcription
def get_voice_transcript():
    # In environments where input() is not supported, we use a fixed sample string
    print("🎙️ [Mock] Listening for voice input...")
    transcript = "Help, someone is following me"
    print(f"🗣️ [Mock] Transcribed: {transcript}")
    return transcript

# Mocked function to simulate location fetching
def get_location():
    # In environments where input() is not supported, we use a fixed location
    print("📍 [Mock] Fetching location...")
    location = "New York, NY"
    print(f"📍 [Mock] Location: {location}")
    return location

# Function to generate structured input data for the agent
def get_sensor_data():
    voice = get_voice_transcript()
    location = get_location()

    # Check for danger based on keywords
    danger_keywords = ["help", "follow", "scared", "unsafe"]
    is_danger = any(keyword in voice.lower() for keyword in danger_keywords)

    # Construct sensor output
    return {
        "transcript": voice,  # ✅ Make sure this line exists
        "location": location,
        "flags": {
            "is_danger": True,
        },
    }


    # Flags for planning (can add more sophisticated ones later)
    danger_flags = {
        "is_danger": any(word in voice.lower() for word in ["help", "follow", "scared", "danger"]),
        "fast_walking": False  # Placeholder — could be GPS delta based in future
    }

    return {
        "voice_transcript": voice,
        "danger_flags": danger_flags,
        "location": location,
        "timestamp": datetime.now().isoformat()
    }

def update_sensor_memory():
    print("📡 Sensor data updated")
    memory.update_flags({
        "last_location": {"lat": 40.7128, "lon": -74.0060},
        "speed_mph": 2.5
    })

def read_sensor_data():
    while True:
        update_sensor_memory()
        time.sleep(1)

def start_sensor_background_thread():
    sensor_thread = threading.Thread(target=read_sensor_data)
    sensor_thread.daemon = True
    sensor_thread.start()

# For testing this file directly
if __name__ == "__main__":
    data = get_sensor_data()
    print("\n📦 Input Data:")
    print(data)
