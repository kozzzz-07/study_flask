from typing import Optional
from pydantic import BaseModel, Field


class User(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1)
    age: int = Field(..., ge=0)
    nickname: Optional[str] = None
