
import os
from dotenv import load_dotenv
load_dotenv()

GEMINI_KEY = os.getenv('GEMINI_API_KEY') or None

# optional import; we guard usage so the project runs without Gemini key
try:
    import google.generativeai as genai
    if GEMINI_KEY:
        genai.configure(api_key=GEMINI_KEY)
except Exception:
    genai = None

class MechanicAgent:
    """MechanicAgent: returns diagnosis and repair steps.
    If GEMINI_API_KEY provided and google-generativeai is available,
    it will call Gemini for richer responses. Otherwise falls back to rule-based responses.
    """

    def analyze(self, vehicle_type: str, problem: str):
        # If Gemini is configured, call it
        if GEMINI_KEY and genai is not None:
            try:
                model = genai.get_model('chat-bison') if hasattr(genai, 'get_model') else genai.GenerativeModel('gemini-pro')
                prompt = self._build_prompt(vehicle_type, problem)
                # Use a compatibility layer: some versions expose model.generate_text or model.generate_content
                if hasattr(model, 'generate_text'):
                    resp = model.generate_text(prompt)
                    text = getattr(resp, 'text', str(resp))
                else:
                    resp = model.generate_content(prompt)
                    text = getattr(resp, 'text', str(resp))
                return {
                    "engine": "gemini",
                    "raw": text
                }
            except Exception as e:
                # fail gracefully to rule based
                return {
                    "engine": "fallback",
                    "error": f"gemini call failed: {e}",
                    "result": self._rule_based(vehicle_type, problem)
                }
        # fallback: rule based
        return {
            "engine": "rule-based",
            "result": self._rule_based(vehicle_type, problem)
        }

    def _build_prompt(self, vehicle_type, problem):
        return f"""
You are an expert vehicle mechanic. Vehicle type: {vehicle_type}\nUser problem: {problem}\n\nRespond in JSON with keys: symptoms (list), possible_cause (str), repair_steps (list), safety_tips (list).\n"""

    def _rule_based(self, vehicle_type, problem):
        p = problem.lower()
        # very simple rules for demonstration
        if 'brake' in p or 'braking' in p or 'brake' in p:
            if vehicle_type == 'scooty':
                return {
                    "vehicle": "Scooty",
                    "symptoms": ["noise while braking", "reduced braking efficiency"],
                    "possible_cause": "Worn brake shoes or loose cable",
                    "repair_steps": [
                        "Inspect brake shoe thickness",
                        "Tighten/adjust brake cable",
                        "Replace brake shoes if worn",
                        "Test brakes after adjustment"
                    ],
                    "safety_tips": ["Use gloves", "Park on level ground", "Keep engine off while working"]
                }
            else:
                return {
                    "vehicle": "Bike",
                    "symptoms": ["squealing or grinding noise", "soft brake lever"],
                    "possible_cause": "Worn brake pads or air in hydraulic lines",
                    "repair_steps": [
                        "Inspect brake pads and disc",
                        "Replace pads if below thickness limit",
                        "Bleed hydraulic brakes if necessary",
                        "Test ride carefully"
                    ],
                    "safety_tips": ["Use jack/stand", "Wear eye protection"]
                }
        if 'engine' in p or 'overheat' in p or 'hot' in p:
            return {
                "vehicle": vehicle_type.capitalize(),
                "symptoms": ["engine running hot", "temperature rise"],
                "possible_cause": "Cooling system issue or oil level low",
                "repair_steps": [
                    "Check coolant level / radiator for blockage",
                    "Check engine oil level and quality",
                    "Inspect for leaking hoses",
                    "Service cooling system if required"
                ],
                "safety_tips": ["Allow engine to cool before opening radiator cap"]
            }
        # default generic response
        return {
            "vehicle": vehicle_type.capitalize(),
            "symptoms": [problem],
            "possible_cause": "Multiple possible causes; needs inspection",
            "repair_steps": [
                "Perform visual inspection for loose parts",
                "Check common wear items (brakes, chain, tires)",
                "If unsure, consult a trained mechanic"
            ],
            "safety_tips": ["Don't ride the vehicle if unsafe"]
        }
