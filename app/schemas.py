from enum import Enum
from typing import Optional
from fastapi import HTTPException
from pydantic import BaseModel, Field, validator


class TaskStatus(str, Enum):
    New = "New"
    InProgress = "In Progress"
    Completed = "Completed"


class TaskInput(BaseModel):
    title: str = Field(..., min_length=1, max_length=256)
    description:  Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.New

    @validator("status", pre=True, always=True)
    def validate_status(cls, value):
        if value is None:
            return value
        return TaskStatus(value)


class TaskUpdate(TaskInput):
    title: Optional[str] = Field(None, min_length=1, max_length=256)


class TaskRequestFilter(BaseModel):
    status: Optional[TaskStatus] = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus

    @validator("id")
    def validate_task_owner(cls, value, values, **kwargs):
        current_user = values.get("current_user")
        if current_user and current_user.id != value.user.id:
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to access this task"
            )
        return value
