"""
Task endpoints for the API.

This module contains all REST endpoints related to task operations.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.dependencies.auth import CurrentUser
from app.domain.value_objects import TaskPriority as DomainTaskPriority
from app.domain.value_objects import TaskStatus as DomainTaskStatus
from app.exceptions import NotFoundException
from app.infrastructure.db.models import TaskPriority, TaskStatus
from app.infrastructure.db.session import get_db
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.notification import EmailNotificationService
from app.services.user import UserService
from app.use_cases.task.create_task import create_task
from app.use_cases.task.get_task import get_task
from app.use_cases.task.list_tasks import list_all_tasks, list_tasks

router = APIRouter()


def convert_domain_to_db_priority(domain_priority: DomainTaskPriority) -> TaskPriority:
    """Convert domain priority to database priority."""
    return TaskPriority(domain_priority.value)


def convert_domain_to_db_status(domain_status: DomainTaskStatus) -> TaskStatus:
    """Convert domain status to database status."""
    return TaskStatus(domain_status.value)


def convert_optional_domain_to_db_status(
    domain_status: Optional[DomainTaskStatus],
) -> Optional[TaskStatus]:
    """Convert optional domain status to optional database status."""
    return convert_domain_to_db_status(domain_status) if domain_status else None


def convert_optional_domain_to_db_priority(
    domain_priority: Optional[DomainTaskPriority],
) -> Optional[TaskPriority]:
    """Convert optional domain priority to optional database priority."""
    return convert_domain_to_db_priority(domain_priority) if domain_priority else None


class TaskStatusUpdate(BaseModel):
    """Schema for task status update."""

    status: TaskStatus


class TaskAssignment(BaseModel):
    """Schema for task assignment."""

    user_id: int


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task_endpoint(
    task: TaskCreate, current_user: CurrentUser, db: Session = Depends(get_db)
):
    """Create a new task."""
    try:
        created_task = create_task(
            db=db,
            task_list_id=task.task_list_id,
            title=task.title,
            description=task.description,
            priority=convert_domain_to_db_priority(task.priority),
            user_id=task.user_id,
        )
        return created_task
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{task_id}", response_model=TaskResponse)
def get_task_endpoint(
    task_id: int, current_user: CurrentUser, db: Session = Depends(get_db)
):
    """Get a task by ID."""
    try:
        task = get_task(db=db, task_id=task_id)
        return task
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=list[TaskResponse])
def list_tasks_endpoint(
    current_user: CurrentUser,
    db: Session = Depends(get_db),
    task_list_id: Optional[int] = Query(None, description="Filter by task list ID"),
    status: Optional[DomainTaskStatus] = Query(None, description="Filter by status"),
    priority: Optional[DomainTaskPriority] = Query(
        None, description="Filter by priority"
    ),
    user_id: Optional[int] = Query(None, description="Filter by assigned user ID"),
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(
        100, ge=1, le=1000, description="Maximum number of tasks to return"
    ),
):
    """List tasks with optional filtering."""
    try:
        if task_list_id:
            # Get tasks for a specific task list
            result = list_tasks(
                db=db,
                task_list_id=task_list_id,
                status=convert_optional_domain_to_db_status(status),
                priority=convert_optional_domain_to_db_priority(priority),
                user_id=user_id,
                skip=skip,
                limit=limit,
            )
            return result["tasks"]
        else:
            # Get all tasks across all task lists
            return list_all_tasks(
                db=db,
                status=convert_optional_domain_to_db_status(status),
                priority=convert_optional_domain_to_db_priority(priority),
                user_id=user_id,
                skip=skip,
                limit=limit,
            )
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{task_id}", response_model=TaskResponse)
def update_task_endpoint(
    task_id: int,
    task_update: TaskUpdate,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    """Update a task."""
    try:  # Get the existing task
        task = get_task(db=db, task_id=task_id)

        # Update fields if provided
        if task_update.title is not None:
            task.title = task_update.title
        if task_update.description is not None:
            task.description = task_update.description
        if task_update.priority is not None:
            task.priority = convert_domain_to_db_priority(task_update.priority)
        if task_update.user_id is not None:
            task.user_id = task_update.user_id

        # Commit changes
        db.commit()
        db.refresh(task)
        return task
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{task_id}/status", response_model=TaskResponse)
def change_task_status_endpoint(
    task_id: int,
    status_data: TaskStatusUpdate,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    """Change task status."""
    try:
        # Get the existing task
        task = get_task(db=db, task_id=task_id)

        # Store old status for notification
        old_status = task.status  # Update status from schema
        task.status = status_data.status

        # Commit changes
        db.commit()
        db.refresh(task)

        # Send notification if task is assigned to a user
        if task.user_id:
            user_service = UserService(db)
            assigned_user = user_service.get_user_by_id(task.user_id)
            if assigned_user:
                EmailNotificationService.send_task_status_change_notification(
                    task, old_status.value, assigned_user
                )

        return task
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{task_id}/assign", response_model=TaskResponse)
def assign_task_endpoint(
    task_id: int,
    assign_data: TaskAssignment,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    """Assign a task to a user."""
    try:
        # Get the existing task
        task = get_task(db=db, task_id=task_id)

        # Validate that the user exists
        user_service = UserService(db)
        user = user_service.get_user_by_id(assign_data.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Store previous assignment for notification
        previous_user_id = task.user_id

        # Update user assignment from schema
        task.user_id = assign_data.user_id  # Commit changes
        db.commit()
        db.refresh(task)

        # Send notification to newly assigned user
        EmailNotificationService.send_task_assignment_notification(task, user)

        # If task was previously assigned to another user, notify them
        if previous_user_id and previous_user_id != assign_data.user_id:
            previous_user = user_service.get_user_by_id(previous_user_id)
            if previous_user:
                EmailNotificationService.send_task_unassignment_notification(
                    task, previous_user
                )

        return task
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{task_id}/unassign", response_model=TaskResponse)
def unassign_task_endpoint(
    task_id: int, current_user: CurrentUser, db: Session = Depends(get_db)
):
    """Unassign a task from a user."""
    try:
        # Get the existing task
        task = get_task(db=db, task_id=task_id)

        # Store user for notification before unassigning
        unassigned_user = None
        if task.user_id:
            user_service = UserService(db)
            unassigned_user = user_service.get_user_by_id(task.user_id)

        # Remove user assignment
        task.user_id = None  # Commit changes
        db.commit()
        db.refresh(task)

        # Send notification to unassigned user
        if unassigned_user:
            EmailNotificationService.send_task_unassignment_notification(
                task, unassigned_user
            )

        return task
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{task_id}", status_code=204)
def delete_task_endpoint(
    task_id: int, current_user: CurrentUser, db: Session = Depends(get_db)
):
    """Delete a task."""
    try:
        # Get the task to ensure it exists
        task = get_task(db=db, task_id=task_id)

        # Delete the task
        db.delete(task)
        db.commit()

        return {"message": "Task deleted successfully"}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
