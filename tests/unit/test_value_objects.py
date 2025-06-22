"""
Unit tests for value objects.

This module contains unit tests for domain value objects.
"""

import pytest
from pydantic import ValidationError

from app.domain.value_objects import TaskListName, TaskPriority, TaskStatus, TaskTitle


class TestTaskStatus:
    """Test cases for TaskStatus enum."""

    def test_task_status_values(self):
        """Test that TaskStatus has correct values."""
        assert TaskStatus.pending == "pending"
        assert TaskStatus.in_progress == "in_progress"
        assert TaskStatus.completed == "completed"

    def test_task_status_string_representation(self):
        """Test string representation of TaskStatus."""
        assert str(TaskStatus.pending) == "pending"
        assert str(TaskStatus.in_progress) == "in_progress"
        assert str(TaskStatus.completed) == "completed"

    def test_get_completed_statuses(self):
        """Test getting completed statuses."""
        completed_statuses = TaskStatus.get_completed_statuses()
        assert TaskStatus.completed in completed_statuses
        assert TaskStatus.pending not in completed_statuses
        assert TaskStatus.in_progress not in completed_statuses

    def test_get_active_statuses(self):
        """Test getting active statuses."""
        active_statuses = TaskStatus.get_active_statuses()
        assert TaskStatus.pending in active_statuses
        assert TaskStatus.in_progress in active_statuses
        assert TaskStatus.completed not in active_statuses


class TestTaskPriority:
    """Test cases for TaskPriority enum."""

    def test_task_priority_values(self):
        """Test that TaskPriority has correct values."""
        assert TaskPriority.low == "low"
        assert TaskPriority.medium == "medium"
        assert TaskPriority.high == "high"

    def test_task_priority_string_representation(self):
        """Test string representation of TaskPriority."""
        assert str(TaskPriority.low) == "low"
        assert str(TaskPriority.medium) == "medium"
        assert str(TaskPriority.high) == "high"

    def test_get_order_value(self):
        """Test getting numeric order values for priorities."""
        assert TaskPriority.get_order_value(TaskPriority.low) == 1
        assert TaskPriority.get_order_value(TaskPriority.medium) == 2
        assert TaskPriority.get_order_value(TaskPriority.high) == 3


class TestTaskTitle:
    """Test cases for TaskTitle value object."""

    def test_valid_task_title(self):
        """Test creation of valid task title."""
        title = TaskTitle(value="Valid Task Title")
        assert title.value == "Valid Task Title"

    def test_task_title_strip_whitespace(self):
        """Test that task title strips leading/trailing whitespace."""
        title = TaskTitle(value="  Trimmed Title  ")
        assert title.value == "Trimmed Title"

    def test_empty_task_title_raises_error(self):
        """Test that empty task title raises validation error."""
        with pytest.raises(ValidationError):
            TaskTitle(value="")

    def test_whitespace_only_task_title_raises_error(self):
        """Test that whitespace-only task title raises validation error."""
        with pytest.raises(ValidationError):
            TaskTitle(value="   ")

    def test_task_title_too_long_raises_error(self):
        """Test that overly long task title raises validation error."""
        long_title = "x" * 201  # Assuming max length is 200
        with pytest.raises(ValidationError):
            TaskTitle(value=long_title)

    def test_task_title_equality(self):
        """Test task title equality."""
        title1 = TaskTitle(value="Same Title")
        title2 = TaskTitle(value="Same Title")
        title3 = TaskTitle(value="Different Title")

        assert title1 == title2
        assert title1 != title3


class TestTaskListName:
    """Test cases for TaskListName value object."""

    def test_valid_task_list_name(self):
        """Test creation of valid task list name."""
        name = TaskListName(value="Valid List Name")
        assert name.value == "Valid List Name"

    def test_task_list_name_strip_whitespace(self):
        """Test that task list name strips leading/trailing whitespace."""
        name = TaskListName(value="  Trimmed Name  ")
        assert name.value == "Trimmed Name"

    def test_empty_task_list_name_raises_error(self):
        """Test that empty task list name raises validation error."""
        with pytest.raises(ValidationError):
            TaskListName(value="")

    def test_whitespace_only_task_list_name_raises_error(self):
        """Test that whitespace-only task list name raises validation error."""
        with pytest.raises(ValidationError):
            TaskListName(value="   ")

    def test_task_list_name_too_long_raises_error(self):
        """Test that overly long task list name raises validation error."""
        long_name = "x" * 101  # Assuming max length is 100
        with pytest.raises(ValidationError):
            TaskListName(value=long_name)

    def test_task_list_name_equality(self):
        """Test task list name equality."""
        name1 = TaskListName(value="Same Name")
        name2 = TaskListName(value="Same Name")
        name3 = TaskListName(value="Different Name")

        assert name1 == name2
        assert name1 != name3
