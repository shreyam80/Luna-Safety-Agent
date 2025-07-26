# Technical Explanation

## Introduction: What Is Luna?

Luna is an AI-powered voice agent designed to **keep people safe** in situations where they might feel vulnerable — like walking alone at night, sensing they’re being followed, or feeling uneasy but unsure what to do.

Most safety tools on the market today are **reactive** — they wait until something bad happens, then send an alert or call 911. Luna is different. It’s both **preventative** and **supportive**.

Luna doesn’t just wait for emergencies. It listens, monitors, and responds in real-time. If it senses something might be wrong, it can gently check in — like a caring friend — and guide you through the situation. This supportive role is called **“communication mode”**, and it’s one of Luna’s most unique features.

---
## 1. Agent Workflow

Describe step-by-step how your agent processes an input:
1. Receive user input  
2. (Optional) Retrieve relevant memory  
3. Plan sub-tasks (e.g., using ReAct / BabyAGI pattern)  
4. Call tools or APIs as needed  
5. Summarize and return final output  

## 1. Agent Workflow

Here’s how Luna works behind the scenes every time you speak or move:

1. **Receive User Input**  
   The iOS app continuously listens to your voice and captures your GPS location, movement, and speed. When you speak (or Luna detects something suspicious), the app sends that data to the backend.

2. **(Optional) Retrieve Relevant Memory**  
   If you've used Luna before, the backend remembers things like your typical routes or whether you’ve already been checked on during this trip. This helps Luna avoid repeating itself or overreacting.

3. **Plan What To Do Next**  
   Luna passes your voice input and sensor context to a powerful language model (Gemini), which thinks through what to do next. Should it ask if you’re okay? Should it say something comforting? Should it prepare to call for help? This is where **communication mode** becomes vital — Luna doesn’t just react; it supports, reassures, and reasons.

   This planning process supports both **single-step actions** (e.g., “Say: You’re almost home”) and **multi-step chains** (e.g., “Ask if okay → wait → call if no response”).

4. **Execute the Plan**  
   Once the LLM decides on an action, Luna’s backend executes it:
   - It might speak out loud via the phone’s speaker
   - If things escalate, it can call a contact or emergency line using Twilio
   - It logs actions and timestamps to Supabase for later review or pattern detection

5. **Respond and Stay Ready**  
   Luna then waits for a user response or continues monitoring in the background. It may ask follow-ups or fall silent, depending on what you choose or how things evolve.

--- 
## 2. Key Modules
1. **Planner** (`planner.py`)  
   Formats the full prompt and sends it to the Gemini LLM. The prompt includes not just what the user said, but also the context: time of day, location, whether the user has stopped moving, and whether Luna already asked something recently.

   Gemini returns a structured, machine-readable decision like:
   ```json
   {
     "action": "speak_then_wait",
     "message": "Hey, I just wanted to check in. Are you feeling safe?",
     "confirm_required": true
   }

   This complexity allows Luna to balance between being too passive and too intrusive — always trying to feel like a calm friend, not an alarm.

2. **Executor**
Takes the plan from the planner and carries it out:

Uses text-to-speech or offloads the audio to the frontend

Makes calls via Twilio if instructed

Ensures that critical actions like calling are only taken with user confirmation, or if urgent red flags are triggered

3. **Main Loop**
The brain that runs the entire experience. It:

Receives input from the frontend or sensors

Manages timing and scheduling of planning + execution

Uses multithreading to handle speech and sensor inputs in parallel without blocking responsiveness

4. **Memory**
Stores user-specific data about the current trip and recent interactions. For example:

Has Luna already asked this user if they’re okay?

Did the user already decline help?

Has the user stopped walking in an unusual place?

Eventually, this will expand to include past trip histories and patterns.

5. **Sensors**
Analyzes GPS, speed, and potential route deviation. In future iterations, it may also infer tone of voice, changes in breathing, or sudden phone movement.

## 3. Tool Integration

- **Google Gemini API**

Called from planner.py with structured prompts and fallback retries

Uses few-shot examples to guide the LLM in safety-oriented, calm responses

- **Twilio API**

Used by executor.py to call a contact or emergency number

Confirmed via LLM-driven logic before initiating

- **Supabase**

Used to store:

User profile info (age, gender, preferences)

Trip logs and timestamps

Action history (e.g., when Luna intervened)

Accessed via REST with authentication headers using an internal HTTP client

- **FastAPI**

Serves endpoints like:

/transcribe_audio (main loop input)

/start_trip, /end_trip

/set_silent_mode

Connects the Swift frontend to the backend intelligence layer

## 4. Observability & Testing

- **Logging**

Every planning and execution decision is logged to logs/luna_decisions.log with timestamps and module traces.

All LLM prompts and outputs are stored with session IDs (anonymized) for future analysis or rollback.

- **Testing**

TEST.sh runs a full path test of:

A user speech transcript (mocked)

Planner decision

Executor response

Supabase log entry

- **Error Handling**

Each module includes retry-on-failure logic (e.g., LLM request timeout, Twilio failure)

Fallback to simple verbal apology or guidance when in uncertain states

## 5. Known Limitations

- **Multistep action complexity**
The LLM occasionally outputs responses that are too verbose or multi-threaded in nature. We've added constraints to prompt for only one decision at a time, but the model still sometimes over-plans.

- **No real-time emotion/tone inference yet**
Currently, we assume deviation in tone could be useful, but haven’t integrated any emotion detection models.

- **Frontend delays may break flow**
Swift app is still in development; without real-time audio feedback, responses may seem delayed or disconnected from user expectations.

- **Silent Mode is manually triggered**
Ideally, Luna would detect when to stay silent (e.g., in a Lyft ride) using context. For now, users must press a button.

- **Incomplete fallback strategy for poor connectivity**
If LLM fails due to no signal, the system does not yet fall back to hardcoded flows (e.g., pre-saved messages or decisions).



