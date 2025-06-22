"""
Delete task list use case.

This module contains the business logic for deleting an existing task list.
"""

from sqlalchemy.orm import Session

from app.domain.models.task_list import TaskList


def delete_task_list(db: Session, task_list_id: int) -> bool:
    """
    Delete a task list by its ID.

    Args:
        db: Database session for persistence.
        task_list_id: ID of the task list to delete.

    Returns:
        bool: True if the task list was found and deleted, False otherwise.
    """
    task_list = db.query(TaskList).filter(TaskList.id == task_list_id).first()
    if task_list:
        db.delete(task_list)
        db.commit()
        return True
    return False
