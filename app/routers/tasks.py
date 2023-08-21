"""Task get, create, update and delete endpoints"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi_pagination import Params, Page
from fastapi_pagination.ext.ormar import paginate

from app.db import TodoUser, TodoTask
from app.security import get_current_user
from app.schemas import TaskInput, TaskStatus, TaskOut, TaskUpdate


router = APIRouter()


@router.post("/tasks", tags=["Tasks"])
async def create_task(task_data: TaskInput,
                      current_user: TodoUser = Depends(get_current_user)):
    """Create new task"""

    new_task = await TodoTask.objects.create(**task_data.dict(),
                                             user=current_user)
    return {"message": f"Task '{new_task.title}' created!"}


@router.get("/tasks",  response_model=Page[TaskOut], tags=["Tasks"])
async def get_all_user_tasks(
    user_id: Optional[int] = None,
    status: Optional[TaskStatus] = None,
    page: int = Query(1, description="Page number", ge=1),
    page_size: int = Query(10, description="Tasks per page", ge=1, le=100)
):
    """Get list of all user's tasks with pagination"""
    tasks = TodoTask.objects.select_related("user")

    if user_id is not None:
        tasks = tasks.filter(user=user_id)

    if status is not None:
        tasks = tasks.filter(status=status)

    params = Params(page=page, size=page_size)

    return await paginate(tasks, params=params)


@router.get("/tasks/{task_id}", response_model=TaskOut, tags=["Tasks"])
async def get_task(task_id: int):
    """Get info about specific task by its ID"""
    task = await (
        TodoTask.objects.select_related("user").get_or_none(id=task_id))

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


@router.put("/tasks/{task_id}", tags=["Tasks"])
async def update_task(task_id: int,
                      updated_task: TaskUpdate,
                      current_user: TodoUser = Depends(get_current_user)):
    """Update existing task"""
    task = await TodoTask.objects.get_or_none(id=task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task.user != current_user:
        raise HTTPException(
            status_code=401,
            detail="Can't update other user's tasks"
        )

    await task.update(**updated_task.dict(exclude_unset=True))
    return {"message": f"Task {task.title} updated successfully"}


@router.delete("/tasks/{task_id}", tags=["Tasks"])
async def delete_task(task_id: int,
                      current_user: TodoUser = Depends(get_current_user)):
    """Delete existing task"""
    task = await TodoTask.objects.get_or_none(id=task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task.user != current_user:
        raise HTTPException(
            status_code=401,
            detail="Can't delete other user's tasks"
        )

    await task.delete()
    return {"message": "Task deleted successfully"}
