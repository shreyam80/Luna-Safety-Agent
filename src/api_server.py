# api_server.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
from src.memory import memory
from src.sensors import start_sensor_background_thread
from src.main import process_one_segment

app = FastAPI()

class TranscriptRequest(BaseModel):
    transcript: str

class MessageInput(BaseModel):
    message: str

class ReasonInput(BaseModel):
    reason: str = "manual override"

@app.on_event("startup")
async def startup_event():
    print("🚀 Luna server starting...")
    start_sensor_background_thread()

@app.post("/transcribe")
async def transcribe(request: Request):
    data = await request.json()
    transcript = data.get("transcript", "")
    print(f"🎙️ Heard (from iOS): {transcript}")

    response = process_one_segment(transcript)

    return {"status": "ok", "response": response}

'''
    subtasks = plan_next_actions(
        transcript,
        flags,
        memory.get_memory_snapshot(),
        memory.get_actions_done_log()
    )

    result = execute_subtasks(subtasks)
    return result or "I'm here with you. What's going on?"
'''

@app.post("/stay_silent")
async def stay_silent(input: ReasonInput):
    memory.update_flags({"is_silent_mode": True})
    memory.update_action_done("stay_silent", {"triggered_by": input.reason})
    return {"status": "ok", "message": "🔇 Luna is now in silent mode."}

# We will probably delete this one
@app.post("/start_talking")
async def start_talking(input: ReasonInput):
    memory.update_flags({"is_silent_mode": False})
    memory.update_action_done("start_talking", {"triggered_by": input.reason})
    return {"status": "ok", "message": "🗣️ Luna will now resume talking."}

@app.get("/memory_snapshot")
async def get_memory():
    return memory.get_memory_snapshot()
