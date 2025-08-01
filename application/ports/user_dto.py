from typing import Optional
from pydantic import BaseModel, Field


class UserCreateDTO(BaseModel):
    name: str = Field(..., min_length=1)
    age: int = Field(..., ge=0)
    nickname: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    nickname: Optional[str] = None
