
# MotorMate — Multi-Agent (Communication + Mechanic) — AI-Ready

This project is a minimal multi-agent system with:
- CommunicationAgent — handles user interaction and extracts vehicle type (bike/scooty) + problem description
- MechanicAgent — analyzes the structured problem and returns diagnosis & repair plan. Optionally uses Google AI Studio (Gemini) if GEMINI_API_KEY is provided.
- FastAPI coordinator that orchestrates the flow.

## Setup
1. Copy `.env.example` to `.env` and put your `GEMINI_API_KEY` if you want AI responses.
2. Create virtualenv and install:
   ```
   pip install -r requirements.txt
   ```
3. Run:
   ```
   uvicorn app.main:app --reload
   ```
4. POST to `/chat` with JSON:
   ```
   { "user_message": "My scooty makes noise when braking" }
   ```
