"""
Get task list use case.

This module contains the business logic for retrieving a single task list.
"""

from sqlalchemy.orm import Session

from app.domain.models.task_list import TaskList


def get_task_list(db: Session, task_list_id: int) -> TaskList | None:
    """
    Retrieve a single task list by its ID.
    F
    Args:
        db: Database session for data access.
        task_list_id: ID of the task list to retrieve.

    Returns:
        TaskList | None: The task list instance if found, None otherwise.
    """
    return db.query(TaskList).filter(TaskList.id == task_list_id).first()
