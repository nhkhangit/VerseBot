from datetime import datetime, date
from typing import Optional
from enum import Enum
from ..base.schema import BaseSchema, BaseDBSchema
from pydantic import Field, conint

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TaskPriority(int, Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4
    CRITICAL = 5

class TaskCreate(BaseSchema):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    assignee: str = Field(..., min_length=1, max_length=100)
    start_date: date
    end_date: date
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    project_id: int = Field(..., gt=0)

class TaskUpdate(BaseSchema):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    assignee: Optional[str] = Field(None, min_length=1, max_length=100)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None

class Task(BaseDBSchema):
    title: str
    description: Optional[str]
    assignee: str
    start_date: date
    end_date: date
    priority: TaskPriority
    status: TaskStatus
    project_id: int
    is_overdue: bool = False
    days_remaining: Optional[int] = None

    def calculate_metadata(self) -> None:
        """Calculate additional metadata for the task"""
        today = date.today()
        self.is_overdue = self.end_date < today and self.status != TaskStatus.COMPLETED
        if self.end_date >= today:
            self.days_remaining = (self.end_date - today).days
        else:
            self.days_remaining = 0

class TaskList(BaseSchema):
    tasks: list[Task]
    total: int
    page: int
    page_size: int
    total_pages: int