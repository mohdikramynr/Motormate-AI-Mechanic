
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ChatRequest(BaseModel):
    user_message: str

class RepairStep(BaseModel):
    step_no: int
    description: str
    tools: Optional[List[str]] = None
    estimated_minutes: Optional[int] = None
