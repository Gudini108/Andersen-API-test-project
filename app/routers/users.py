"""User endpoints"""

from typing import List
from fastapi import APIRouter

from app.repo.user import UserRepo
from app.schemas.schemas import UsersOut


router = APIRouter()


@router.get("/users", response_model=List[UsersOut], tags=['Users'])
async def get_all_users():
    """Get list of all user's usernames"""
    return await UserRepo.get_all_users()
