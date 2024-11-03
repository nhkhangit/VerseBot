from datetime import datetime
from typing import Optional, List
from enum import Enum
from pydantic import Field
from ..base.schema import BaseSchema, BaseDBSchema

class ProjectStatus(str, Enum):
    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class ProjectStatistics(BaseSchema):
    total_tasks: int = 0
    completed_tasks: int = 0
    pending_tasks: int = 0
    overdue_tasks: int = 0
    completion_rate: float = 0.0

class ProjectCreate(BaseSchema):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: ProjectStatus = Field(default=ProjectStatus.PLANNING)

class ProjectUpdate(BaseSchema):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[ProjectStatus] = None

class Project(BaseDBSchema):
    name: str
    description: Optional[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    status: ProjectStatus
    statistics: Optional[ProjectStatistics] = None

class ProjectList(BaseSchema):
    items: List[Project]
    total: int
    page: int
    page_size: int
    total_pages: int
