from pydantic import BaseModel
from datetime import date
from typing import Optional

class ExpenseSchema(BaseModel):
    amount: float
    category: str
    date: date
    notes: Optional[str] = None

class IncomeSchema(BaseModel):
    amount: float
    source: str
    date: date
    notes: Optional[str] = None
