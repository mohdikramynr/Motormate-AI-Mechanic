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
    "white smoke": "Engine oil is burning due to worn piston rings.",
    "black smoke": "Too much fuel is burning - carburetor or injector issue.",
    "not start": "Battery, spark plug, or ignition switch problem.",
    "engine noise": "Loose parts or low engine oil.",
    "dead battery": "Battery has no charge.",
    "brake not working": "Brake shoe worn or cable loose.",
    "bike overheating": "Cooling system failure or low coolant.",
    "engine stalls": "Fuel supply problem or dirty air filter.",
    "low mileage": "Clogged air filter or wrong fuel mixture.",
    "hard gear": "Clutch cable tight or gearbox issue.",
    "bike jerking": "Fuel injector blockage or spark plug fault.",
    "vibration": "Loose nuts or wheel imbalance.",
    "chain noise": "Dry or loose chain.",
    "oil leakage": "Damaged engine gasket or seal.",
    "headlight not working": "Blown bulb or wiring issue."
}

def find_keyword_response(text: str):
    for key, solution in KEYWORDS.items():
        if key in text:
            return f""" Problem Detected: {key}
Solution: {solution}

     Important Notice:
If your bike or scooty has any serious problem, unusual noise, heavy smoke, or feels unsafe to ride, immediately check your mechanic.

     Safety Tip:
Wear gloves and avoid touching hot parts. If problem continues, visit a professional mechanic.
"""
    return None


@app.post("/analyze")
async def analyze_problem(query: Query):
    user_text = query.symptom.lower().strip()

    #  Greeting handling
    if user_text in ["hi", "hello", "hey"]:
        return {"response": " Hello! Tell me your bike or scooty problem."}

    if "how are you" in user_text:
        return {"response": " I'm good! Ready to fix your bike problems."}

    if "thank" in user_text:
        return {"response": " You're welcome! Ride safe."}
    
    # ✅ Mechanic location / contact query
    if any(word in user_text for word in ["mechanic", "where is mechanic", "contact mechanic", "repair shop"]):
        return {
            "response": """
     Recommended Mechanic:

    Name: Islam Auto Center  
    Contact Number: 9416680786  

You can visit or call for professional bike and scooty repair services.
"""
        }

    #  Keyword System First
    keyword_reply = find_keyword_response(user_text)
    if keyword_reply:
        return {"response": keyword_reply}

    #  AI Fallback
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
