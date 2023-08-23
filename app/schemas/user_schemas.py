"""Response user models for endpoints"""

from typing import Optional
from pydantic import BaseModel


class UsersOut(BaseModel):
    """Response model to list all usernames"""
    id: int
    username: str


class TodoUserInput(BaseModel):
    username: str
    first_name: str
    password: str
    last_name: Optional[str]
