from fastapi import APIRouter, HTTPException, Depends, Body, Query
from fastapi_pagination import Params, paginate
from ormar.exceptions import NoMatch
from pydantic import ValidationError

from app.security import get_current_user
from app.db import TodoUser, TodoTask

router = APIRouter()


@router.post("/tasks", tags=["Tasks"])
async def create_task(task_data: dict = Body(...),
                      current_user: TodoUser = Depends(get_current_user)):
    """Create new task"""
    title = task_data.get("title")
    new_task = await TodoTask.objects.create(title=title, user=current_user)
    return {"message": f"Task {new_task.title} created!"}


@router.get("/tasks", tags=["Tasks"])
async def get_all_user_tasks(
    current_user: TodoUser = Depends(get_current_user),
    page: int = Query(1, description="Page number", ge=1),
    page_size: int = Query(5, description="Tasks per page", ge=1, le=100)
):
    """Get list of all user's tasks"""
    tasks = await TodoTask.objects.filter(user=current_user).all()

    if not tasks:
        return {"message": "You currently have no Tasks."}

    params = Params(page=page, size=page_size)

    filtered_tasks = [
        {
            "Task": task.title,
            "Description": task.description,
            "Status": task.status
        }
        for task in tasks
    ]

    return paginate(filtered_tasks, params=params)


@router.get("/tasks/{task_id}", tags=["Tasks"])
async def get_task(task_id: int,
                   current_user: TodoUser = Depends(get_current_user)):
    """Get info about specific task by its ID"""
    try:
        task = await TodoTask.objects.select_related("user").get(id=task_id)

        if task.user != current_user:
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to access this task"
            )

        filtered_task = {
                "Task": task.title,
                "Description": task.description,
                "Status": task.status
                }

        return filtered_task

    except NoMatch:
        raise HTTPException(
            status_code=404,
            detail="Couldn't find this task"
        )


@router.get("/tasks/status/{status}", tags=["Tasks"])
async def get_tasks_by_status(
    status: str,
    current_user: TodoUser = Depends(get_current_user),
    page: int = Query(1, description="Page number", ge=1),
    page_size: int = Query(5, description="Tasks per page", ge=1, le=100)
):
    """Filter tasks by status"""
    status_dict = {
        "new": "New",
        "in progress": "In Progress",
        "completed": "Completed"
    }
    lowercase_status = status.lower()
    if lowercase_status not in status_dict:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid status. Choose 'New', 'In Progress', or 'Completed'")
        )

    tasks = await (
        TodoTask.objects.filter(user=current_user,
                                status=status_dict[lowercase_status]).all())

    if not tasks:
        return {
            "message": "You do not have any "
            f"'{status_dict[lowercase_status]}' tasks."}

    params = Params(page=page, size=page_size)

    filtered_tasks = [
        {
            "Task": task.title,
            "Description": task.description,
            "Status": task.status
        }
        for task in tasks
    ]

    return paginate(filtered_tasks, params=params)


@router.put("/tasks/{task_id}", tags=["Tasks"])
async def update_task(task_id: int, updated_task: dict = Body(...),
                      current_user: TodoUser = Depends(get_current_user)):
    """Update existing task"""
    try:
        task_to_update = await TodoTask.objects.get(id=task_id)
        if task_to_update.user != current_user:
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to update this task")

        await task_to_update.update(**updated_task)
        return {"message": f"Task {task_to_update.title} updated successfully"}

    except NoMatch:
        raise HTTPException(
            status_code=404,
            detail="Couldn't find this task"
        )

    except ValidationError:
        return {
            "message": "Please choose 'New', 'In Progress' or 'Completed' "
            "for a status"
            }


@router.delete("/tasks/{task_id}", tags=["Tasks"])
async def delete_task(task_id: int,
                      current_user: TodoUser = Depends(get_current_user)):
    """Delete existing task"""
    try:
        task = await TodoTask.objects.select_related("user").get(id=task_id)
        if task.user != current_user:
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to delete this task")

        await task.delete()
        return {"message": "Task deleted successfully"}

    except NoMatch:
        raise HTTPException(
            status_code=404,
            detail="Couldn't find this task"
        )
