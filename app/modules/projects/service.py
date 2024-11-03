from datetime import datetime
from typing import List, Optional
import asyncpg
from fastapi import HTTPException, status
from .schema import (
    Project, ProjectCreate, ProjectUpdate, 
    ProjectStatus, ProjectList, ProjectStatistics
)

class ProjectService:
    def __init__(self, conn: asyncpg.Connection):
        self._conn = conn

    async def create_project(self, project: ProjectCreate) -> Project:
        query = '''
            INSERT INTO projects (
                name, description, start_date, end_date, status
            )
            VALUES ($1, $2, $3, $4, $5)
            RETURNING *
        '''
        try:
            row = await self._conn.fetchrow(
                query,
                project.name,
                project.description,
                project.start_date,
                project.end_date,
                project.status
            )
            return Project(**dict(row))
        except asyncpg.UniqueViolationError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project with this name already exists"
            )

    async def get_project(self, project_id: int) -> Project:
        # Get project details
        project_query = 'SELECT * FROM projects WHERE id = $1'
        project_row = await self._conn.fetchrow(project_query, project_id)
        
        if not project_row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )

        # Get project statistics
        stats_query = '''
            SELECT 
                COUNT(*) as total_tasks,
                COUNT(*) FILTER (WHERE status = 'completed') as completed_tasks,
                COUNT(*) FILTER (WHERE status = 'pending') as pending_tasks,
                COUNT(*) FILTER (
                    WHERE end_date < CURRENT_DATE 
                    AND status != 'completed'
                ) as overdue_tasks
            FROM tasks 
            WHERE project_id = $1
        '''
        stats_row = await self._conn.fetchrow(stats_query, project_id)
        
        project = Project(**dict(project_row))
        
        # Calculate statistics
        stats = ProjectStatistics(
            total_tasks=stats_row['total_tasks'],
            completed_tasks=stats_row['completed_tasks'],
            pending_tasks=stats_row['pending_tasks'],
            overdue_tasks=stats_row['overdue_tasks']
        )
        
        if stats.total_tasks > 0:
            stats.completion_rate = (stats.completed_tasks / stats.total_tasks) * 100
            
        project.statistics = stats
        return project

    async def get_projects(
        self,
        status: Optional[ProjectStatus] = None,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 10
    ) -> ProjectList:
        # Build query conditions
        conditions = []
        params = []
        param_index = 1

        if status:
            conditions.append(f"status = ${param_index}")
            params.append(status)
            param_index += 1

        if search:
            conditions.append(
                f"(name ILIKE ${param_index} OR description ILIKE ${param_index})"
            )
            params.append(f"%{search}%")
            param_index += 1

        # Base query
        query = 'SELECT * FROM projects'
        count_query = 'SELECT COUNT(*) FROM projects'

        # Add conditions
        if conditions:
            where_clause = ' WHERE ' + ' AND '.join(conditions)
            query += where_clause
            count_query += where_clause

        # Add pagination
        query += ' ORDER BY created_at DESC LIMIT $%d OFFSET $%d' % (
            param_index, param_index + 1
        )
        params.extend([page_size, (page - 1) * page_size])

        # Get total count and records
        total = await self._conn.fetchval(count_query, *params[:-2])
        rows = await self._conn.fetch(query, *params)

        # Get statistics for all projects
        projects = []
        for row in rows:
            project = await self.get_project(row['id'])
            projects.append(project)

        return ProjectList(
            items=projects,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total + page_size - 1) // page_size
        )

    async def update_project(
        self, 
        project_id: int, 
        project_update: ProjectUpdate
    ) -> Project:
        # Verify project exists
        await self.get_project(project_id)
        
        # Build update query
        update_fields = []
        params = []
        param_index = 1
        
        update_data = project_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            update_fields.append(f"{field} = ${param_index}")
            params.append(value)
            param_index += 1

        if not update_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )

        # Add updated_at
        update_fields.append(f"updated_at = ${param_index}")
        params.append(datetime.utcnow())
        param_index += 1

        # Add project_id
        params.append(project_id)

        query = f'''
            UPDATE projects 
            SET {', '.join(update_fields)}
            WHERE id = ${param_index}
            RETURNING *
        '''

        try:
            row = await self._conn.fetchrow(query, *params)
            return await self.get_project(row['id'])
        except asyncpg.UniqueViolationError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project with this name already exists"
            )

    async def delete_project(self, project_id: int) -> bool:
        # This will automatically delete associated tasks due to CASCADE
        query = 'DELETE FROM projects WHERE id = $1 RETURNING id'
        result = await self._conn.fetchrow(query, project_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )
        return True

    async def change_status(
        self, 
        project_id: int, 
        status: ProjectStatus
    ) -> Project:
        query = '''
            UPDATE projects 
            SET status = $1, updated_at = $2
            WHERE id = $3
            RETURNING *
        '''
        row = await self._conn.fetchrow(
            query, 
            status, 
            datetime.utcnow(), 
            project_id
        )
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )
        
        return await self.get_project(project_id)
