from fastapi_pagination.ext.ormar import paginate
from fastapi_pagination import Params

from app.db import TodoTask
from app.schemas.schemas import TaskUpdate


class TaskRepo():
    @staticmethod
    async def safe_get_task_by_id(task_id: int) -> TodoTask | None:
        return await (
            TodoTask.objects.select_related("user").get_or_none(id=task_id))

    @staticmethod
    async def get_paginated_tasks(
        pagination_params: Params,
        filters: dict
    ):
        tasks = TodoTask.objects.select_related("user")
        tasks = tasks.filter(**filters)
        return await paginate(tasks, params=pagination_params)

    @staticmethod
    async def create_task(task_input, user):
        return await TodoTask.objects.create(**task_input.dict(), user=user)

    @staticmethod
    async def update_task(current_task: TodoTask, task_update: TaskUpdate):
        return await current_task.update(
            **task_update.dict(exclude_unset=True)
        )

    @staticmethod
    async def delete_task(current_task: TodoTask):
        return await current_task.delete()
