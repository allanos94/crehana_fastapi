"""
Mock email notification service for task assignments.

This module provides a mock implementation of email notifications
that logs instead of sending actual emails. In a real implementation,
this would integrate with services like SendGrid, SES, etc.
"""

import logging
from typing import Optional

from app.infrastructure.db.models.task import Task
from app.infrastructure.db.models.user import User

# Set up logger for notifications
logger = logging.getLogger(__name__)


class EmailNotificationService:
    """Mock email notification service."""

    @staticmethod
    def send_task_assignment_notification(task: Task, assigned_user: User) -> bool:
        """
        Send notification when a task is assigned to a user.

        Args:
            task: The task that was assigned
            assigned_user: The user the task was assigned to

        Returns:
            bool: True if notification was "sent" successfully
        """
        try:
            # Mock email content
            subject = f"New Task Assigned: {task.title}"
            body = f"""
            Hello {assigned_user.name or assigned_user.email},

            You have been assigned a new task:

            Title: {task.title}
            Description: {task.description or "No description provided"}
            Status: {task.status}
            Priority: {task.priority}

            Please log in to the task management system to view more details.

            Best regards,
            Task Management System
            """

            # In a real implementation, this would send an actual email
            logger.info(
                f"MOCK EMAIL SENT - To: {assigned_user.email}, "
                f"Subject: {subject}, Task ID: {task.id}"
            )
            logger.debug(f"Email body: {body}")

            return True

        except Exception as e:
            logger.error(f"Failed to send task assignment notification: {e}")
            return False

    @staticmethod
    def send_task_unassignment_notification(task: Task, unassigned_user: User) -> bool:
        """
        Send notification when a task is unassigned from a user.

        Args:
            task: The task that was unassigned
            unassigned_user: The user the task was unassigned from

        Returns:
            bool: True if notification was "sent" successfully
        """
        try:
            # Mock email content
            subject = f"Task Unassigned: {task.title}"
            body = f"""
            Hello {unassigned_user.name or unassigned_user.email},

            The following task has been unassigned from you:

            Title: {task.title}
            Description: {task.description or "No description provided"}

            If you have any questions, please contact your project manager.

            Best regards,
            Task Management System
            """

            # In a real implementation, this would send an actual email
            logger.info(
                f"MOCK EMAIL SENT - To: {unassigned_user.email}, "
                f"Subject: {subject}, Task ID: {task.id}"
            )
            logger.debug(f"Email body: {body}")

            return True

        except Exception as e:
            logger.error(f"Failed to send task unassignment notification: {e}")
            return False

    @staticmethod
    def send_task_status_change_notification(
        task: Task, old_status: str, assigned_user: Optional[User] = None
    ) -> bool:
        """
        Send notification when a task status changes.

        Args:
            task: The task whose status changed
            old_status: The previous status
            assigned_user: The user assigned to the task (if any)

        Returns:
            bool: True if notification was "sent" successfully
        """
        if not assigned_user:
            logger.debug(f"No user assigned to task {task.id}, skipping notification")
            return True

        try:
            # Mock email content
            subject = f"Task Status Updated: {task.title}"
            body = f"""
            Hello {assigned_user.name or assigned_user.email},

            The status of your assigned task has been updated:

            Title: {task.title}
            Previous Status: {old_status}
            New Status: {task.status}

            Please log in to the task management system to view more details.

            Best regards,
            Task Management System
            """

            # In a real implementation, this would send an actual email
            logger.info(
                f"MOCK EMAIL SENT - To: {assigned_user.email}, "
                f"Subject: {subject}, Task ID: {task.id}, "
                f"Status: {old_status} -> {task.status}"
            )
            logger.debug(f"Email body: {body}")

            return True

        except Exception as e:
            logger.error(f"Failed to send task status change notification: {e}")
            return False
