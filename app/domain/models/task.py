"""
Task domain model.

This module contains the pure Task domain entity without any infrastructure
dependencies. Following Clean Architecture principles, this model contains
only business logic and rules.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from app.domain.value_objects import TaskPriority, TaskStatus, TaskTitle


@dataclass
class Task:
    """
    Task domain entity representing a single task within a task list.

    This is a pure domain model that contains business logic and rules,
    without any dependencies on external frameworks or infrastructure.

    Attributes:
        id: Unique identifier for the task.
        title: Title of the task (using TaskTitle value object).
        description: Optional detailed description of the task.
        status: Current status of the task (using TaskStatus value object).
        priority: Priority level of the task (using TaskPriority value object).
        task_list_id: Foreign key reference to the task list.
        user_id: Optional foreign key reference to the assigned user.
        created_at: Timestamp when the task was created.
        updated_at: Timestamp when the task was last updated.
    """

    title: TaskTitle
    task_list_id: int
    id: Optional[int] = None
    description: Optional[str] = None
    status: TaskStatus = field(default=TaskStatus.pending)
    priority: TaskPriority = field(default=TaskPriority.medium)
    user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Post-initialization to set timestamps if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = self.created_at

    def change_status(self, new_status: TaskStatus) -> None:
        """
        Change the task status with business rules validation.

        Args:
            new_status: The new status to set for the task.

        Raises:
            ValueError: If the status transition is not allowed.
        """
        if not self._is_valid_status_transition(self.status, new_status):
            raise ValueError(
                f"Invalid status transition from {self.status} to {new_status}"
            )

        self.status = new_status
        self.updated_at = datetime.now()

    def assign_to_user(self, user_id: int) -> None:
        """
        Assign the task to a user.

        Args:
            user_id: ID of the user to assign the task to.
        """
        self.user_id = user_id
        self.updated_at = datetime.now()

    def unassign_user(self) -> None:
        """Remove user assignment from the task."""
        self.user_id = None
        self.updated_at = datetime.now()

    def update_title(self, new_title: TaskTitle) -> None:
        """
        Update the task title.

        Args:
            new_title: New title for the task.
        """
        self.title = new_title
        self.updated_at = datetime.now()

    def update_description(self, new_description: Optional[str]) -> None:
        """
        Update the task description.

        Args:
            new_description: New description for the task.
        """
        self.description = new_description
        self.updated_at = datetime.now()

    def change_priority(self, new_priority: TaskPriority) -> None:
        """
        Change the task priority.

        Args:
            new_priority: New priority level for the task.
        """
        self.priority = new_priority
        self.updated_at = datetime.now()

    def is_completed(self) -> bool:
        """Check if the task is completed."""
        return self.status == TaskStatus.completed

    def is_assigned(self) -> bool:
        """Check if the task is assigned to a user."""
        return self.user_id is not None

    def _is_valid_status_transition(
        self, from_status: TaskStatus, to_status: TaskStatus
    ) -> bool:
        """
        Validate if a status transition is allowed based on business rules.

        Args:
            from_status: Current status.
            to_status: Target status.

        Returns:
            bool: True if transition is valid, False otherwise."""
        # Business rule: Any status can transition to any other status
        # In a real-world scenario, you might have more complex rules
        valid_transitions = {
            TaskStatus.pending: [TaskStatus.in_progress, TaskStatus.completed],
            TaskStatus.in_progress: [TaskStatus.pending, TaskStatus.completed],
            TaskStatus.completed: [TaskStatus.pending, TaskStatus.in_progress],
        }

        return to_status in valid_transitions.get(from_status, [])
