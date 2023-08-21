"""Response endpoints schemas"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, validator


class UsersOut(BaseModel):
    """Response model to list all usernames"""
    username: str


class TaskStatus(str, Enum):
    """Model for choosing task status"""
    New = "New"
    InProgress = "In Progress"
    Completed = "Completed"


class TaskInput(BaseModel):
    """Response model for task input with status validation"""
    title: str = Field(..., min_length=1, max_length=256)
    description:  Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.New

    @validator("status", pre=True, always=True)
    def validate_status(cls, value):
        if value is None:
            return value
        return TaskStatus(value)


class TaskUpdate(TaskInput):
    """Response model to update task"""
    title: Optional[str] = Field(None, min_length=1, max_length=256)


class TaskOut(BaseModel):
    """Response model for filtering task response"""
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
