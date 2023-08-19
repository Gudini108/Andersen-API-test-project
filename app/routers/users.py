from fastapi import APIRouter

from app.db import TodoUser


router = APIRouter()


@router.get("/users", tags=['Users'])
async def get_all_users():
    users = await TodoUser.objects.all()
    usernames = [user.username for user in users]
    return usernames
