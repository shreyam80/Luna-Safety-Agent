import os
from dotenv import load_dotenv
import google.generativeai as genai
from src.memory import memory

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

'''
def call_gemini_planner(prompt: str):
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content(prompt)
    print(response)
    try:
        raw = response.text.strip()

        # Remove triple backticks and 'json' language hint if present
        if raw.startswith("```"):
          raw = raw.strip("```json").strip("```").strip()

        # Try to safely parse it
        import ast
        return ast.literal_eval(raw)

    except Exception as e:
        print("🔮 Error parsing Gemini output:", e)
        print("🔮 Raw output:", response.text)
        return []
        '''
import ast  # Safely parses Python-like strings

def call_gemini_planner(prompt: str):
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content(prompt)
    raw = response.candidates[0].content.parts[0].text.strip()

    print("🧠 Raw Gemini Output:\n", raw)

    # Remove triple backticks or wrapping markers if present
    if raw.startswith("```"):
        raw = raw.strip("```json").strip("```").strip()

    try:
        # Parse string with single quotes to Python list of dicts
        subtasks = ast.literal_eval(raw)
        return subtasks
    except Exception as e:
        print("❌ Failed to parse subtasks:", e)
        return []



# The planner takes user input, flags, and memory to generate the next set of subtasks.
def plan_next_actions(transcript, flags, memory, actions_done):
    context_prompt = f"""
You are Luna, a personal safety agent that helps users in risky situations.

The user has just said: "{transcript}"

Current danger flags:
{flags}

Memory Snapshot:
{memory}

Actions already performed: {actions_done}

Your job is to:
1. Decide the safest next steps the user should take.
2. Prioritize actions that help the user feel safe and guided. Use the list of actions below.

Available actions are split into two types:

Passive actions:
- speak(message): Say something to the user.
- send_text_to_contacts(): Notify the user’s emergency circle.
- record_voice_and_location(): Begin logging voice and GPS for evidence.
- stay_silent(): Stop talking temporarily (only if user asks). Do not send anything in response.
- start_talking(): Resume talking after silence (only if user asks).

Critical actions (require permission):
- call_police(): Suggesting calling emergency services and wait for the user to confirm before calling.
- get_nearest_safe_location(): Suggest a nearby safe location and wait for the user to confirm before guiding. 
  You must clearly tell the user what the safe place is, why it's safe (e.g. "it has people nearby"), and ask: "Do you want me to guide you there?" 
  Do not guide them until they say yes.

  Important:
- You must **not repeat critical actions** more than once per session.
  These include:
  - call_police()
  - send_text_to_contacts()
  If these were already completed (see “Actions already performed”), do not suggest them again.

- Passive actions like speak() or record_voice_and_location() may be repeated if helpful.
- For get_nearest_safe_location(), tell the user the name of the place, how far it is, and why it's a safe location. Then ask if they want guidance. Wait for user confirmation before continuing.

3. For every action, include a short 'speak' message that explains what you're doing — say it calmly or firmly depending on context.
4. Assume the user may stop any action at any time and must be informed of what you're doing.
5. Include only helpful and timely actions — not all tools need to be used every time.
6. Use memory to make smarter decisions.

You must also respond to **direct user commands** like "call the police" or "stop talking" by initiating or stopping that action.

If the user simply says "yes", then check memory to figure out what the user is responding to. If it is about safe location, respond with speak and take them to the location you had suggested by giving clear directions on how to get there.

If silent mode is on, return no text. Do not speak. Only speak if user explicitly tells you to.

Your output should be a **Python list of dictionaries**. Do NOT wrap it in triple backticks or use markdown formatting. Just return the raw list like this:
[
  {{"action": "speak", "text": "I'm here with you. Let's stay safe."}},
  {{"action": "record_voice_and_location"}},
  {{"action": "get_nearest_safe_location", "text": "There’s a hotel 1 minute away that’s well-lit. Do you want me to guide you there?"}}
]

Only include one critical action (`call_police` or `get_nearest_safe_location`) per response. Ask permission before continuing. Respect user input at all times.

    """

    # Call Gemini LLM to get structured plan
    subtasks = call_gemini_planner(context_prompt)

    return subtasks
