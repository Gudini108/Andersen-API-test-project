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
    return {"message": f"Task {new_task.title} created!"}


@router.get("/tasks",  response_model=Page[TaskOut], tags=["Tasks"])
async def get_all_user_tasks(
    status: Optional[TaskStatus] = None,
    current_user: TodoUser = Depends(get_current_user),
    page: int = Query(1, description="Page number", ge=1),
    page_size: int = Query(5, description="Tasks per page", ge=1, le=100)
):
    """Get list of all user's tasks with pagination"""
    tasks = TodoTask.objects.filter(user=current_user)

    if status is not None:
        tasks = tasks.filter(status=status)

    params = Params(page=page, size=page_size)

    return await paginate(tasks, params=params)


@router.get("/tasks/{task_id}", response_model=TaskOut, tags=["Tasks"])
async def get_task(task_id: int,
                   current_user: TodoUser = Depends(get_current_user)):
    """Get info about specific task by its ID"""
    task = await TodoTask.objects.get_or_none(user=current_user, id=task_id)
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
    task = await TodoTask.objects.get_or_none(user=current_user, id=task_id)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    await task.update(**updated_task.dict(exclude_unset=True))
    return {"message": f"Task {task.title} updated successfully"}


@router.delete("/tasks/{task_id}", tags=["Tasks"])
async def delete_task(task_id: int,
                      current_user: TodoUser = Depends(get_current_user)):
    """Delete existing task"""
    task = await TodoTask.objects.get_or_none(user=current_user, id=task_id)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    await task.delete()
    return {"message": "Task deleted successfully"}
