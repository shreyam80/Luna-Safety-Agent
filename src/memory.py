# memory.py
# This module stores and retrieves persistent memory for the agent

class Memory:
    def __init__(self):
        # Initial internal memory store
        self.flags = {
            "is_danger_mode": False,
            "code_phrase_detected": False,
            "last_route": None,
        }
        self.voice_log = []  # Stores voice transcripts
        self.agent_responses = []  # Stores Luna's actions

    def update_flags(self, new_flags):
        self.flags.update(new_flags)

    def get_flag(self, key):
        return self.flags.get(key, None)

    def log_transcript(self, transcript):
        self.voice_log.append(transcript)

    def log_response(self, response):
        self.agent_responses.append(response)

    def summarize(self):
        print("🧠 Agent Memory Summary")
        print("Flags:", self.flags)
        print("Last 3 Transcripts:", self.voice_log[-3:])
        print("Last 3 Responses:", self.agent_responses[-3:])

# Test
if __name__ == "__main__":
    memory = Memory()
    memory.update_flags({"is_danger_mode": True})
    memory.log_transcript("Help, I feel unsafe")
    memory.log_response("Sent alert to contacts")
    memory.summarize()
