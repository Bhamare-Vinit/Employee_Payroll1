from pydantic import BaseModel,Field
from typing import Optional,Dict, Any

class Employee(BaseModel):
    id: int
    name: str
    salary: float
    department: str

class UpdateEmployee(BaseModel):
    name: Optional[str] = None
    salary: Optional[float] = None
    department: Optional[str] = None
