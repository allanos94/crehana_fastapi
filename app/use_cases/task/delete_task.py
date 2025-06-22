"""
Delete task use case.

This module contains the business logic for deleting an existing task.
"""

from sqlalchemy.orm import Session

from app.domain.models.task import Task


def delete_task(db: Session, task_id: int) -> bool:
    """
    Delete a task by its ID.

    Args:
        db: Database session for persistence.
        task_id: ID of the task to delete.

    Returns:
        bool: True if the task was found and deleted, False otherwise.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        return True
    return False
