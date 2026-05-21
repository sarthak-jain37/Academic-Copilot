from typing import Optional

from pydantic import BaseModel
from datetime import datetime

class QuestionCreate(BaseModel):
    query: str
    
class QuestionResponse(BaseModel):
    query: str
    answer: str
    sources: list[str]