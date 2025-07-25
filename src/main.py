import threading
import time
from memory import memory
from planner import plan_next_actions
from executor import execute_subtasks

# Dummy functions you'll replace with real ones
def get_latest_transcript():
    # Simulate transcript input — replace with actual microphone or stream
    return "I think someone is following me"

def new_transcript_available():
    # Replace with real logic (e.g. microphone buffer updated)
    return True

def update_sensor_memory():
    # Simulate updating location, speed, etc. — you'll fill this out
    print("📡 Sensor data updated")
    memory.update_flags({
        "last_location": {"lat": 40.7128, "lon": -74.0060},
        "speed_mph": 2.5
    })

# Background thread that updates location/speed every 1 second
def read_sensor_data():
    while True:
        update_sensor_memory()
        time.sleep(1)

def main():
    # Start the sensor thread
    sensor_thread = threading.Thread(target=read_sensor_data)
    sensor_thread.daemon = True
    sensor_thread.start()

    print("🚀 Luna is live. Waiting for user input...")

    while True:
        if new_transcript_available():
            transcript = get_latest_transcript()

            if transcript.strip() != "":
                print(f"🎙️ Heard: {transcript}")

                flags = {
                    "tone_anxiety": True,
                    "danger_keywords": True,
                    "silent_mode": False
                }

                memory.update_flags(flags)
                memory.log_transcript(transcript)

                subtasks = plan_next_actions(
                    transcript,
                    flags,
                    memory.get_memory_snapshot(),
                    memory.get_actions_done()
                )

                execute_subtasks(subtasks)
        
        time.sleep(0.2)  # Keep CPU usage low

if __name__ == "__main__":
    main()
