from fastapi import FastAPI, APIRouter, Depends, Query, Path
from typing import Optional
from .service import TaskService
from .schema import (
    Task, TaskCreate, TaskUpdate, TaskStatus,
    TaskPriority, TaskList
)
from ..base.module import BaseModule
from ...core.database import get_connection

class TaskModule(BaseModule):
    def __init__(self, app: FastAPI = None):  # Make app optional with default None
        super().__init__(app)  # Pass app to parent class
        self.prefix = "/tasks"
        self.tags = ["tasks"]

    @property
    def name(self) -> str:
        return "tasks"

    def register_routes(self) -> None:
        @self.router.post("/", response_model=Task)
        async def create_task(
            task: TaskCreate,
            conn = Depends(get_connection)
        ):
            service = TaskService(conn)
            return await service.create_task(task)

        @self.router.get("/", response_model=TaskList)
        async def get_tasks(
            project_id: Optional[int] = Query(None, description="Filter by project ID"),
            status: Optional[TaskStatus] = Query(None, description="Filter by status"),
            assignee: Optional[str] = Query(None, description="Filter by assignee"),
            priority: Optional[TaskPriority] = Query(None, description="Filter by priority"),
            page: int = Query(1, ge=1, description="Page number"),
            page_size: int = Query(10, ge=1, le=100, description="Items per page"),
            conn = Depends(get_connection)
        ):
            service = TaskService(conn)
            return await service.get_tasks(
                project_id=project_id,
                status=status,
                assignee=assignee,
                priority=priority,
                page=page,
                page_size=page_size
            )

        @self.router.get("/{task_id}", response_model=Task)
        async def get_task(
            task_id: int,
            conn = Depends(get_connection)
        ):
            service = TaskService(conn)
            return await service.get_task(task_id)

        @self.router.put("/{task_id}", response_model=Task)
        async def update_task(
            task_id: int,
            task_update: TaskUpdate,
            conn = Depends(get_connection)
        ):
            service = TaskService(conn)
            return await service.update_task(task_id, task_update)

        @self.router.delete("/{task_id}")
        async def delete_task(
            task_id: int,
            conn = Depends(get_connection)
        ):
            service = TaskService(conn)
            await service.delete_task(task_id)
            return {"message": "Task deleted successfully"}

        @self.router.patch("/{task_id}/status", response_model=Task)
        async def change_task_status(
            task_id: int,
            status: TaskStatus,
            conn = Depends(get_connection)
        ):
            service = TaskService(conn)
            print(status)
            return await service.change_status(task_id, status)

    async def init_module(self) -> None:
        async with self.app.state.pool.acquire() as conn:
            # Tạo enum type cho task status
            await conn.execute('''
                DO $$ BEGIN
                    CREATE TYPE task_status AS ENUM (
                        'pending',
                        'in_progress',
                        'completed',
                        'cancelled'
                    );
                EXCEPTION
                    WHEN duplicate_object THEN null;
                END $$;
            ''')

            # Tạo bảng tasks
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    assignee VARCHAR(100) NOT NULL,
                    start_date DATE NOT NULL,
                    end_date DATE NOT NULL,
                    priority INTEGER NOT NULL CHECK (priority >= 1 AND priority <= 5),
                    status task_status DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP
                );
                
                CREATE INDEX IF NOT EXISTS idx_tasks_project_id ON tasks(project_id);
                CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
                CREATE INDEX IF NOT EXISTS idx_tasks_assignee ON tasks(assignee);
            ''')

            # Kiểm tra và thêm cột status nếu chưa tồn tại
            await conn.execute('''
                DO $$ 
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 
                        FROM information_schema.columns 
                        WHERE table_name = 'tasks' AND column_name = 'status'
                    ) THEN
                        ALTER TABLE tasks 
                        ADD COLUMN status task_status DEFAULT 'pending';
                    END IF;
                END $$;
            ''')