"""User endpoints"""

from typing import List
from fastapi import APIRouter

from app.db import TodoUser
from app.schemas import UsersOut


router = APIRouter()


@router.get("/users", response_model=List[UsersOut], tags=['Users'])
async def get_all_users():
    """Get list of all user's usernames"""
    users = await TodoUser.objects.all()
    return users
