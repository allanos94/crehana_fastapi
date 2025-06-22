"""
Task List endpoints for the API.

This module contains all REST endpoints related to task list operations.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies.auth import CurrentUser
from app.exceptions import ConflictException, NotFoundException
from app.infrastructure.db.session import get_db
from app.schemas.task_list import TaskListCreate, TaskListResponse, TaskListUpdate
from app.use_cases.task_list.create_task_list import create_task_list

router = APIRouter()


@router.post("/", response_model=TaskListResponse, status_code=201)
def create_task_list_endpoint(
    task_list: TaskListCreate, current_user: CurrentUser, db: Session = Depends(get_db)
):
    """Create a new task list."""
    try:
        created_task_list = create_task_list(db=db, name=task_list.name)
        return created_task_list
    except ConflictException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{task_list_id}", response_model=TaskListResponse)
def get_task_list_endpoint(
    task_list_id: int, current_user: CurrentUser, db: Session = Depends(get_db)
):
    """Get a task list by ID."""
    try:
        from app.infrastructure.db.repositories import TaskListRepository

        task_list_repo = TaskListRepository(db)
        task_list = task_list_repo.get_by_id(task_list_id)

        if not task_list:
            raise NotFoundException(f"Task list with id {task_list_id} not found")

        return task_list
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=list[TaskListResponse])
def list_task_lists_endpoint(
    current_user: CurrentUser,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """List all task lists."""
    try:
        from app.infrastructure.db.repositories import TaskListRepository

        task_list_repo = TaskListRepository(db)
        task_lists = task_list_repo.get_all(skip=skip, limit=limit)

        return task_lists
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{task_list_id}", response_model=TaskListResponse)
def update_task_list_endpoint(
    task_list_id: int,
    task_list_update: TaskListUpdate,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    """Update a task list."""
    try:
        from app.infrastructure.db.repositories import TaskListRepository

        task_list_repo = TaskListRepository(db)
        task_list = task_list_repo.get_by_id(task_list_id)

        if not task_list:
            raise NotFoundException(f"Task list with id {task_list_id} not found")

        # Update fields if provided
        if task_list_update.name is not None:
            # Check for name conflicts
            existing = task_list_repo.get_by_name(task_list_update.name)
            if existing and existing.id != task_list_id:
                raise ConflictException(
                    f"Task list with name '{task_list_update.name}' already exists"
                )
            task_list.name = task_list_update.name

        # Commit changes
        db.commit()
        db.refresh(task_list)
        return task_list
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ConflictException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{task_list_id}", status_code=204)
def delete_task_list_endpoint(
    task_list_id: int, current_user: CurrentUser, db: Session = Depends(get_db)
):
    """Delete a task list."""
    try:
        from app.infrastructure.db.repositories import TaskListRepository

        task_list_repo = TaskListRepository(db)
        task_list = task_list_repo.get_by_id(task_list_id)

        if not task_list:
            raise NotFoundException(f"Task list with id {task_list_id} not found")

        # Delete the task list (this will cascade delete all tasks)
        db.delete(task_list)
        db.commit()

        return {"message": "Task list deleted successfully"}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
