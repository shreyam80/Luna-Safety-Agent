from schema import InputData
import os
import google.generativeai as genai

# Load Gemini API key from environment
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

def generate_plan(input_data: InputData):
    # Construct the prompt to send to Gemini
    prompt = f"""
You are Luna, a calm safety assistant for women walking alone.
The user said: "{input_data.transcript}"
Location: {input_data.location}
Speed: {input_data.speed}
Danger mode: {input_data.is_danger}
Past movement: {input_data.location_history}

Your job is to return a list of actions to take, like:
- speak("I’m here with you")
- get_location()
- send_text_to_contacts()
- call_emergency_services()

Only return a Python list of strings like this:
["speak('I’m with you')", "send_text_to_contacts()"]
    """

    response = model.generate_content(prompt)
    plan = eval(response.text)  # Caution: this assumes trusted output

    return plan
