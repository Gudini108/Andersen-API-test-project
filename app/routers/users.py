"""User endpoints"""

from typing import List
from fastapi import APIRouter

from app.repo.users import UserRepo
from app.schemas.user_schemas import UserOut


router = APIRouter()


@router.get("/users", response_model=List[UserOut], tags=['Users'])
async def get_all_users():
    """Get list of all user's usernames"""
    return await UserRepo.get_all_users()
