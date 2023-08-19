from enum import Enum
from typing import Optional
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
    description:  Optional[str]
    status: TaskStatus
