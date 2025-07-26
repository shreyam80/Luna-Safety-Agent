# api_server.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
from src.memory import memory
from src.planner import plan_action
from src.executor import execute_action

app = FastAPI()

class MessageInput(BaseModel):
    message: str

class ReasonInput(BaseModel):
    reason: str = "manual override"

@app.post("/speak")
async def speak(input: MessageInput):
    return

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
