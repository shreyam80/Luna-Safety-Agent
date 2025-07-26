# memory.py
# This module stores and retrieves persistent memory for the agent
from datetime import datetime

class Memory:
    def __init__(self):
        # Initial internal memory store
        self.flags = {
            "is_silent_mode": False,
            "last_route": None,
        }

        self.actions_done_log = []
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

    def was_action_done(self, action_name):
        return any(entry["action"] == action_name for entry in memory.actions_done_log)
    
    def get_memory_snapshot(self):
        # Return a lightweight memory snapshot for the planner
        return {
            "flags": self.flags,
            "recent_voice_log": self.voice_log[-3:],
            "recent_responses": self.agent_responses[-3:],
            "actions_done": self.actions_done_log
        }
    
    def get_actions_done(self):
        return self.actions_done_log

    def update_action_done(self, action_name, details=None):
        self.actions_done_log.append({
        "action": action_name,
        "timestamp": datetime.utcnow().isoformat(),
        "details": details
    })

# External helper functions for executor
'''
def update_memory(action_name, status=True, memory=None):
    if memory:
        memory.update_action_done(action_name, status)
        '''

memory = Memory()

# Test
if __name__ == "__main__":
    test_memory = Memory()
    test_memory.update_flags({"is_danger_mode": True})
    test_memory.log_transcript("Help, I feel unsafe")
    test_memory.log_response("Sent alert to contacts")
    test_memory.summarize()
