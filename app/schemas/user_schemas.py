"""Response user models for endpoints"""

from typing import Optional
from pydantic import BaseModel


class UserOut(BaseModel):
    """Response model for user"""
    id: int
    username: str


class TodoUserInput(BaseModel):
    """Response model for user input"""
    username: str
    first_name: str
    password: str
    last_name: Optional[str]
