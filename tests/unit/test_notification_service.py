"""
Unit tests for email notification service.

This module tests:
- Task assignment notifications
- Task unassignment notifications
- Task status change notifications
"""

from unittest.mock import Mock, PropertyMock

from app.infrastructure.db.models.task import Task
from app.infrastructure.db.models.user import User
from app.services.notification import EmailNotificationService


class TestEmailNotificationService:
    """Test cases for EmailNotificationService."""

    def test_send_task_assignment_notification_success(self):
        """Test successful task assignment notification."""
        # Create mock objects
        user = Mock(spec=User)
        user.email = "user@example.com"
        user.name = "Test User"

        task = Mock(spec=Task)
        task.id = 1
        task.title = "Test Task"
        task.description = "Test description"
        task.status = "pending"
        task.priority = "medium"

        # Send notification
        result = EmailNotificationService.send_task_assignment_notification(task, user)

        # Verify success
        assert result is True

    def test_send_task_assignment_notification_no_name(self):
        """Test task assignment notification with user having no name."""
        # Create mock objects
        user = Mock(spec=User)
        user.email = "user@example.com"
        user.name = None

        task = Mock(spec=Task)
        task.id = 1
        task.title = "Test Task"
        task.description = None
        task.status = "pending"
        task.priority = "high"

        # Send notification
        result = EmailNotificationService.send_task_assignment_notification(task, user)

        # Verify success
        assert result is True

    def test_send_task_unassignment_notification_success(self):
        """Test successful task unassignment notification."""
        # Create mock objects
        user = Mock(spec=User)
        user.email = "user@example.com"
        user.name = "Test User"

        task = Mock(spec=Task)
        task.id = 1
        task.title = "Test Task"
        task.description = "Test description"

        # Send notification
        result = EmailNotificationService.send_task_unassignment_notification(task, user)

        # Verify success
        assert result is True

    def test_send_task_status_change_notification_with_user(self):
        """Test task status change notification with assigned user."""
        # Create mock objects
        user = Mock(spec=User)
        user.email = "user@example.com"
        user.name = "Test User"

        task = Mock(spec=Task)
        task.id = 1
        task.title = "Test Task"
        task.status = "completed"

        old_status = "in_progress"

        # Send notification
        result = EmailNotificationService.send_task_status_change_notification(
            task, old_status, user
        )

        # Verify success
        assert result is True

    def test_send_task_status_change_notification_no_user(self):
        """Test task status change notification without assigned user."""
        # Create mock objects
        task = Mock(spec=Task)
        task.id = 1
        task.title = "Test Task"
        task.status = "completed"

        old_status = "in_progress"

        # Send notification
        result = EmailNotificationService.send_task_status_change_notification(
            task, old_status, None
        )

        # Verify success (should skip notification gracefully)
        assert result is True

    def test_send_task_assignment_notification_exception_handling(self):
        """Test exception handling in task assignment notification."""
        # Create mock that raises exception
        user = Mock(spec=User)
        user.email = "user@example.com"
        user.name = "Test User"

        # Create task mock that raises exception when accessing attributes
        task = Mock(spec=Task)
        task.id = 1
        # Configure the title property to raise an exception
        type(task).title = PropertyMock(side_effect=Exception("Database error"))

        # Send notification
        result = EmailNotificationService.send_task_assignment_notification(task, user)

        # Verify failure is handled gracefully
        assert result is False

    def test_send_task_unassignment_notification_exception_handling(self):
        """Test exception handling in task unassignment notification."""
        # Create mock that raises exception
        user = Mock(spec=User)
        user.email = "user@example.com"
        user.name = "Test User"

        # Create task mock that raises exception when accessing attributes
        task = Mock(spec=Task)
        task.id = 1
        # Configure the title property to raise an exception
        type(task).title = PropertyMock(side_effect=Exception("Database error"))

        # Send notification
        result = EmailNotificationService.send_task_unassignment_notification(task, user)

        # Verify failure is handled gracefully
        assert result is False

    def test_send_task_status_change_notification_exception_handling(self):
        """Test exception handling in task status change notification."""
        # Create mock that raises exception
        user = Mock(spec=User)
        user.email = "user@example.com"
        user.name = "Test User"

        # Create task mock that raises exception when accessing attributes
        task = Mock(spec=Task)
        task.id = 1
        # Configure the title property to raise an exception
        type(task).title = PropertyMock(side_effect=Exception("Database error"))

        old_status = "in_progress"

        # Send notification
        result = EmailNotificationService.send_task_status_change_notification(
            task, old_status, user
        )

        # Verify failure is handled gracefully
        assert result is False
