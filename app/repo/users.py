from app.db import TodoUser
from app.schemas.user_schemas import TodoUserInput


class UserRepo():
    @staticmethod
    async def safe_get_user_by_username(username: str) -> TodoUser | None:
        return await TodoUser.objects.get_or_none(username=username)

    @staticmethod
    async def get_all_users():
        return await TodoUser.objects.all()

    @staticmethod
    async def save_user(user_input: TodoUserInput):
        return await TodoUser.objects.create(**user_input.dict())
