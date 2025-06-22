"""
Update task list use case.

This module contains the business logic for updating an existing task list.
"""

from sqlalchemy.orm import Session

from app.domain.models.task_list import TaskList


def update_task_list(db: Session, task_list_id: int, name: str) -> TaskList | None:
    """
    Update an existing task list's name.

    Args:
        db: Database session for persistence.
        task_list_id: ID of the task list to update.
        name: New name for the task list.
          Returns:
        TaskList | None: The updated task list instance if found,
            None otherwise.
    """
    task_list = db.query(TaskList).filter(TaskList.id == task_list_id).first()
    if task_list:
        task_list.name = name
        db.commit()
        db.refresh(task_list)
    return task_list
