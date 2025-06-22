"""
TaskList domain model.

This module contains the pure TaskList domain entity without any infrastructure
dependencies. Following Clean Architecture principles, this model contains
only business logic and rules.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.domain.value_objects import CompletionPercentage, TaskListName


@dataclass
class TaskList:
    """
    TaskList domain entity representing a collection of related tasks.

    This is a pure domain model that contains business logic and rules,
    without any dependencies on external frameworks or infrastructure.

    Attributes:
        name: Name of the task list (using TaskListName value object).
        id: Unique identifier for the task list.
        created_at: Timestamp when the task list was created.
        updated_at: Timestamp when the task list was last updated.
    """

    name: TaskListName
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Post-initialization to set timestamps if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = self.created_at

    def update_name(self, new_name: TaskListName) -> None:
        """
        Update the task list name.

        Args:
            new_name: New name for the task list.
        """
        self.name = new_name
        self.updated_at = datetime.now()

    def calculate_completion_percentage(
        self, total_tasks: int, completed_tasks: int
    ) -> CompletionPercentage:
        """
        Calculate the completion percentage for this task list.

        Args:
            total_tasks: Total number of tasks in the list.
            completed_tasks: Number of completed tasks in the list.

        Returns:
            CompletionPercentage: The calculated completion percentage.
        """
        return CompletionPercentage.calculate_from_tasks(total_tasks, completed_tasks)

    def is_empty(self, task_count: int) -> bool:
        """
        Check if the task list is empty.

        Args:
            task_count: Number of tasks in the list.

        Returns:
            bool: True if the list has no tasks, False otherwise.
        """
        return task_count == 0

    def is_fully_completed(self, total_tasks: int, completed_tasks: int) -> bool:
        """
        Check if all tasks in the list are completed.

        Args:
            total_tasks: Total number of tasks in the list.
            completed_tasks: Number of completed tasks in the list.

        Returns:
            bool: True if all tasks are completed, False otherwise.
        """
        if total_tasks == 0:
            return False
        return completed_tasks == total_tasks
