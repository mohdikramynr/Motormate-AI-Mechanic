from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import google.generativeai as genai

# Gemini setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    symptom: str


KEYWORDS = {
    "white smoke": "Engine oil burning - piston ring problem. Immediate checking required.",
    "black smoke": "Excess fuel burning - Carburetor or injector issue.",
    "not start": "Battery problem, spark plug issue or ignition switch fault.",
    "engine noise": "Serious engine issue - visit mechanic immediately.",
    "dead battery": "Battery replacement required.",
    "brake not working": "Brake shoe worn out or cable loose."
}

def find_keyword_response(text: str):
    for key, solution in KEYWORDS.items():
        if key in text:
            return f"🔧 Problem Detected: {key}\n Solution: {solution}"
    return None


@app.post("/analyze")
async def analyze_problem(query: Query):
    user_text = query.symptom.lower().strip()

    # 👉 Greeting handling
    if user_text in ["hi", "hello", "hey"]:
        return {"response": "👋 Hello! Tell me your bike or scooty problem."}

    if "how are you" in user_text:
        return {"response": " I'm good! Ready to fix your bike problems."}

    if "thank" in user_text:
        return {"response": " You're welcome! Ride safe."}

    # 👉 Keyword System First
    keyword_reply = find_keyword_response(user_text)
    if keyword_reply:
        return {"response": keyword_reply}

    # 👉 AI Fallback
    try:
        prompt = f"""
        You are an expert bike mechanic.
        User problem: {user_text}
        Give solution in simple clear language.
        """
        ai_response = model.generate_content(prompt)

        if ai_response.text:
            return {"response": ai_response.text}
    except Exception as e:
        print("Gemini Error:", e)

    return {"response": "Please describe your problem more clearly "}
