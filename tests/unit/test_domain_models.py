"""
Unit tests for domain models.

This module contains unit tests for domain entities and business logic.
"""

from app.domain.models.task import Task
from app.domain.models.task_list import TaskList
from app.domain.value_objects import TaskListName, TaskPriority, TaskStatus, TaskTitle


class TestTask:
    """Test cases for Task domain model."""

    def test_task_creation(self):
        """Test basic task creation."""
        title = TaskTitle(value="Test Task")
        task = Task(title=title, task_list_id=1, description="Test description")

        assert task.title == title
        assert task.task_list_id == 1
        assert task.description == "Test description"
        assert task.status == TaskStatus.pending
        assert task.priority == TaskPriority.medium
        assert task.user_id is None
        assert task.created_at is not None
        assert task.updated_at is not None

    def test_task_creation_with_custom_values(self):
        """Test task creation with custom status and priority."""
        title = TaskTitle(value="High Priority Task")
        task = Task(title=title, task_list_id=1, priority=TaskPriority.high, user_id=123)

        assert task.priority == TaskPriority.high
        assert task.user_id == 123

    def test_task_change_status(self):
        """Test changing task status."""
        title = TaskTitle(value="Test Task")
        task = Task(title=title, task_list_id=1)
        original_updated_at = task.updated_at

        # Wait a bit to ensure timestamp difference
        import time

        time.sleep(0.01)
        task.change_status(TaskStatus.in_progress)

        assert task.status == TaskStatus.in_progress
        assert task.updated_at is not None
        assert original_updated_at is not None
        assert task.updated_at > original_updated_at

    # def test_task_invalid_status_transition(self):
    #     """Test invalid status transition raises error."""
    #     # Currently all transitions are allowed in the implementation
    #     # This test would be useful when stricter business rules are
    #     # implemented
    #     pass

    def test_task_assign_to_user(self):
        """Test assigning task to a user."""
        title = TaskTitle(value="Test Task")
        task = Task(title=title, task_list_id=1)
        original_updated_at = task.updated_at

        import time

        time.sleep(0.01)

        task.assign_to_user(456)

        assert task.user_id == 456
        assert task.updated_at is not None
        assert original_updated_at is not None
        assert task.updated_at > original_updated_at

    def test_task_unassign_user(self):
        """Test unassigning user from task."""
        title = TaskTitle(value="Test Task")
        task = Task(title=title, task_list_id=1, user_id=789)
        original_updated_at = task.updated_at

        import time

        time.sleep(0.01)

        task.unassign_user()

        assert task.user_id is None
        assert task.updated_at > original_updated_at

    def test_task_update_title(self):
        """Test updating task title."""
        title = TaskTitle(value="Original Title")
        task = Task(title=title, task_list_id=1)
        original_updated_at = task.updated_at

        import time

        time.sleep(0.01)

        new_title = TaskTitle(value="Updated Title")
        task.update_title(new_title)

        assert task.title == new_title
        assert task.updated_at > original_updated_at

    def test_task_update_description(self):
        """Test updating task description."""
        title = TaskTitle(value="Test Task")
        task = Task(title=title, task_list_id=1, description="Original description")
        original_updated_at = task.updated_at

        import time

        time.sleep(0.01)

        task.update_description("Updated description")

        assert task.description == "Updated description"
        assert task.updated_at > original_updated_at

    def test_task_change_priority(self):
        """Test changing task priority."""
        title = TaskTitle(value="Test Task")
        task = Task(title=title, task_list_id=1)
        original_updated_at = task.updated_at

        import time

        time.sleep(0.01)

        task.change_priority(TaskPriority.high)

        assert task.priority == TaskPriority.high
        assert task.updated_at > original_updated_at

    def test_task_is_completed(self):
        """Test checking if task is completed."""
        title = TaskTitle(value="Test Task")
        task = Task(title=title, task_list_id=1)

        assert not task.is_completed()

        task.status = TaskStatus.completed
        assert task.is_completed()

    def test_task_is_assigned(self):
        """Test checking if task is assigned."""
        title = TaskTitle(value="Test Task")
        task = Task(title=title, task_list_id=1)

        assert not task.is_assigned()

        task.user_id = 123
        assert task.is_assigned()


class TestTaskList:
    """Test cases for TaskList domain model."""

    def test_task_list_creation(self):
        """Test basic task list creation."""
        name = TaskListName(value="Test List")
        task_list = TaskList(name=name)

        assert task_list.name == name
        assert task_list.id is None
        assert task_list.created_at is not None
        assert task_list.updated_at is not None

    def test_task_list_update_name(self):
        """Test updating task list name."""
        name = TaskListName(value="Original Name")
        task_list = TaskList(name=name)
        original_updated_at = task_list.updated_at

        import time

        time.sleep(0.01)

        new_name = TaskListName(value="Updated Name")
        task_list.update_name(new_name)

        assert task_list.name == new_name
        assert task_list.updated_at > original_updated_at
