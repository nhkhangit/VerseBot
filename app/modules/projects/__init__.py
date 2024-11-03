from fastapi import FastAPI, APIRouter, Depends, Query, Path
from typing import Optional
from .service import ProjectService
from .schema import (
    Project, ProjectCreate, ProjectUpdate,
    ProjectStatus, ProjectList
)
from ..base.module import BaseModule
from ...core.database import get_connection

class ProjectModule(BaseModule):
    def __init__(self, app: FastAPI = None):  # Make app optional with default None
        super().__init__(app)  # Pass app to parent class
        self.prefix = "/projects"
        self.tags = ["projects"]

    @property
    def name(self) -> str:
        return "projects"

    def register_routes(self) -> None:
        @self.router.post("/", response_model=Project)
        async def create_project(
            project: ProjectCreate,
            conn = Depends(get_connection)
        ):
            """Create a new project"""
            service = ProjectService(conn)
            return await service.create_project(project)

        @self.router.get("/", response_model=ProjectList)
        async def get_projects(
            status: Optional[ProjectStatus] = Query(
                None, 
                description="Filter by project status"
            ),
            search: Optional[str] = Query(
                None, 
                description="Search in name and description"
            ),
            page: int = Query(1, ge=1, description="Page number"),
            page_size: int = Query(
                10, 
                ge=1, 
                le=100, 
                description="Items per page"
            ),
            conn = Depends(get_connection)
        ):
            """Get list of projects with filtering and pagination"""
            service = ProjectService(conn)
            return await service.get_projects(
                status=status,
                search=search,
                page=page,
                page_size=page_size
            )

        @self.router.get("/{project_id}", response_model=Project)
        async def get_project(
            project_id: int = Path(..., gt=0),
            conn = Depends(get_connection)
        ):
            """Get project details including statistics"""
            service = ProjectService(conn)
            return await service.get_project(project_id)

        @self.router.put("/{project_id}", response_model=Project)
        async def update_project(
            project_update: ProjectUpdate,
            project_id: int = Path(..., gt=0),
            conn = Depends(get_connection)
        ):
            """Update project details"""
            service = ProjectService(conn)
            return await service.update_project(project_id, project_update)

        @self.router.delete("/{project_id}")
        async def delete_project(
            project_id: int = Path(..., gt=0),
            conn = Depends(get_connection)
        ):
            """Delete project and all associated tasks"""
            service = ProjectService(conn)
            await service.delete_project(project_id)
            return {"message": "Project deleted successfully"}

        @self.router.patch("/{project_id}/status", response_model=Project)
        async def change_project_status(
            status: ProjectStatus,
            project_id: int = Path(..., gt=0),
            conn = Depends(get_connection)
        ):
            """Change project status"""
            service = ProjectService(conn)
            return await service.change_status(project_id, status)
        
    async def init_module(self) -> None:
        async with self.app.state.pool.acquire() as conn:
            # Kiểm tra và tạo enum type nếu chưa tồn tại
            await conn.execute('''
                DO $$ BEGIN
                    CREATE TYPE project_status AS ENUM (
                        'planning',
                        'active',
                        'on_hold',
                        'completed',
                        'cancelled'
                    );
                EXCEPTION
                    WHEN duplicate_object THEN null;
                END $$;
            ''')

            # Tạo bảng projects với các cột cập nhật
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS projects (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL UNIQUE,
                    description TEXT,
                    start_date TIMESTAMP,
                    end_date TIMESTAMP,
                    status project_status DEFAULT 'planning',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP
                );
                
                CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status);
                CREATE INDEX IF NOT EXISTS idx_projects_name ON projects(name);
            ''')

            # Kiểm tra và thêm cột status nếu chưa tồn tại
            await conn.execute('''
                DO $$ 
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 
                        FROM information_schema.columns 
                        WHERE table_name = 'projects' AND column_name = 'status'
                    ) THEN
                        ALTER TABLE projects 
                        ADD COLUMN status project_status DEFAULT 'planning';
                    END IF;
                END $$;
            ''')