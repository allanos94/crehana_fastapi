"""
User domain model.

This module contains the pure User domain entity without any infrastructure
dependencies. Following Clean Architecture principles, this model contains
only business logic and rules.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.domain.value_objects import UserEmail


@dataclass
class User:
    """
    User domain entity representing a system user.

    This is a pure domain model that contains business logic and rules,
    without any dependencies on external frameworks or infrastructure.

    Attributes:
        email: Unique email address of the user (using UserEmail value object).
        name: Optional display name of the user.
        id: Unique identifier for the user.
        created_at: Timestamp when the user was created.
        updated_at: Timestamp when the user was last updated.
    """

    email: UserEmail
    name: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Post-initialization to set timestamps if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = self.created_at

    def update_name(self, new_name: Optional[str]) -> None:
        """
        Update the user's display name.

        Args:
            new_name: New display name for the user.
        """
        self.name = new_name
        self.updated_at = datetime.now()

    def update_email(self, new_email: UserEmail) -> None:
        """
        Update the user's email address.

        Args:
            new_email: New email address for the user.
        """
        self.email = new_email
        self.updated_at = datetime.now()

    def has_name(self) -> bool:
        """
        Check if the user has a display name set.

        Returns:
            bool: True if the user has a name, False otherwise."""
        return self.name is not None and self.name.strip() != ""

    def get_display_name(self) -> str:
        """
        Get the display name for the user.

        Returns:
            str: The user's name if available, otherwise their email.
        """
        if self.has_name():
            return self.name  # type: ignore
        return str(self.email)
