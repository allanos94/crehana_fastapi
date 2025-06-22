"""
List tasks use case.

This module contains the business logic for listing tasks with filtering
and completion percentage calculation.
"""

from typing import Any, Optional

from sqlalchemy.orm import Session

from app.exceptions import NotFoundException
from app.infrastructure.db.models import Task, TaskPriority, TaskStatus
from app.infrastructure.db.repositories import TaskListRepository, TaskRepository


def list_tasks(
    db: Session,
    task_list_id: int,
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    user_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
) -> dict[str, Any]:
    """
    List tasks from a task list with optional filtering.

    Args:
        db: Database session for data access.
        task_list_id: ID of the task list to retrieve tasks from.
        status: Optional status filter for tasks.
        priority: Optional priority filter for tasks.
        user_id: Optional user filter for tasks.
        skip: Number of tasks to skip for pagination.
        limit: Maximum number of tasks to return.

    Returns:
        Dict[str, Any]: Dictionary containing tasks list and completion stats.

    Raises:
        NotFoundException: If the task list doesn't exist.
    """
    # Verify that the task list exists
    task_list_repo = TaskListRepository(db)
    task_list = task_list_repo.get_by_id(task_list_id)
    if not task_list:
        raise NotFoundException(f"Task list with id {task_list_id} not found")

    # Get filtered tasks
    task_repo = TaskRepository(db)
    tasks = task_repo.get_tasks_with_filters(
        task_list_id=task_list_id,
        status=status,
        priority=priority,
        user_id=user_id,
        skip=skip,
        limit=limit,
    )

    # Get all tasks for completion percentage calculation
    all_tasks = task_repo.get_by_task_list_id(task_list_id)
    total = len(all_tasks)
    completed = len([t for t in all_tasks if t.status == TaskStatus.completed])
    percent_complete = (completed / total * 100) if total else 0

    return {
        "tasks": tasks,
        "total": total,
        "completed": completed,
        "percent_complete": round(percent_complete, 2),
        "pagination": {"skip": skip, "limit": limit, "returned": len(tasks)},
    }


def list_all_tasks(
    db: Session,
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    user_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Task]:
    """
    List all tasks across all task lists with optional filtering.

    Args:
        db: Database session for data access.
        status: Optional status filter for tasks.
        priority: Optional priority filter for tasks.
        user_id: Optional user filter for tasks.
        skip: Number of tasks to skip for pagination.
        limit: Maximum number of tasks to return.

    Returns:
        List[Task]: List of tasks matching the filters.
    """
    task_repo = TaskRepository(db)
    return task_repo.get_tasks_with_filters(
        status=status, priority=priority, user_id=user_id, skip=skip, limit=limit
    )
