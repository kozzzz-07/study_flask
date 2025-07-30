from typing import Optional
from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    nickname: Optional[str] = None
