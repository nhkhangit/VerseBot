from datetime import date, datetime
from typing import List, Optional
import asyncpg
from fastapi import HTTPException, status
from .schema import Task, TaskCreate, TaskUpdate, TaskStatus, TaskList

class TaskService:
    def __init__(self, conn: asyncpg.Connection):
        self._conn = conn

    async def create_task(self, task: TaskCreate) -> Task:
        # Kiểm tra project tồn tại
        project_exists = await self._conn.fetchval(
            'SELECT EXISTS(SELECT 1 FROM projects WHERE id = $1)',
            task.project_id
        )
        if not project_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {task.project_id} not found"
            )

        # Validate dates
        if task.end_date < task.start_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="End date cannot be earlier than start date"
            )

        query = '''
            INSERT INTO tasks (
                title, description, assignee, start_date, end_date,
                priority, project_id, status
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            RETURNING id, title, description, assignee, start_date,
                      end_date, priority, status, project_id,
                      created_at, updated_at
        '''
        row = await self._conn.fetchrow(
            query,
            task.title,
            task.description,
            task.assignee,
            task.start_date,
            task.end_date,
            task.priority,
            task.project_id,
            TaskStatus.PENDING
        )
        
        task_obj = Task(**dict(row))
        task_obj.calculate_metadata()
        return task_obj

    async def get_task(self, task_id: int) -> Optional[Task]:
        query = 'SELECT * FROM tasks WHERE id = $1'
        row = await self._conn.fetchrow(query, task_id)
        
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {task_id} not found"
            )
        
        task = Task(**dict(row))
        task.calculate_metadata()
        return task

    async def get_tasks(
        self,
        project_id: Optional[int] = None,
        status: Optional[TaskStatus] = None,
        assignee: Optional[str] = None,
        priority: Optional[int] = None,
        page: int = 1,
        page_size: int = 10
    ) -> TaskList:
        # Build query conditions
        conditions = []
        params = []
        param_index = 1

        if project_id:
            conditions.append(f"project_id = ${param_index}")
            params.append(project_id)
            param_index += 1

        if status:
            conditions.append(f"status = ${param_index}")
            params.append(status)
            param_index += 1

        if assignee:
            conditions.append(f"assignee = ${param_index}")
            params.append(assignee)
            param_index += 1

        if priority:
            conditions.append(f"priority = ${param_index}")
            params.append(priority)
            param_index += 1

        # Base query
        query = 'SELECT * FROM tasks'
        count_query = 'SELECT COUNT(*) FROM tasks'

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

        # Create task objects
        tasks = []
        for row in rows:
            task = Task(**dict(row))
            task.calculate_metadata()
            tasks.append(task)

        return TaskList(
            tasks=tasks,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total + page_size - 1) // page_size
        )

    async def update_task(self, task_id: int, task_update: TaskUpdate) -> Task:
        # Get current task
        current_task = await self.get_task(task_id)
        
        # Build update query
        update_fields = []
        params = []
        param_index = 1
        
        update_data = task_update.dict(exclude_unset=True)
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

        # Add task_id
        params.append(task_id)

        query = f'''
            UPDATE tasks 
            SET {', '.join(update_fields)}
            WHERE id = ${param_index}
            RETURNING *
        '''

        row = await self._conn.fetchrow(query, *params)
        task = Task(**dict(row))
        task.calculate_metadata()
        return task

    async def delete_task(self, task_id: int) -> bool:
        query = 'DELETE FROM tasks WHERE id = $1 RETURNING id'
        result = await self._conn.fetchrow(query, task_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {task_id} not found"
            )
        return True

    async def change_status(self, task_id: int, status: TaskStatus) -> Task:
        query = '''
            UPDATE tasks 
            SET status = $1, updated_at = $2
            WHERE id = $3
            RETURNING *
        '''
        row = await self._conn.fetchrow(query, status, datetime.utcnow(), task_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {task_id} not found"
            )
        
        task = Task(**dict(row))
        task.calculate_metadata()
        return task