"""Tests for exceptions and error handling."""

from app.exceptions import (
    ApplicationException,
    ConflictException,
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
    ValidationException,
)


class TestExceptions:
    """Test custom exceptions."""

    def test_application_exception(self):
        """Test base ApplicationException."""
        error = ApplicationException("Test error", 500)
        assert str(error) == "Test error"
        assert error.message == "Test error"
        assert error.code == 500

    def test_not_found_exception(self):
        """Test NotFoundException."""
        error = NotFoundException("Resource not found")
        assert str(error) == "Resource not found"
        assert error.code == 404

    def test_not_found_exception_default_message(self):
        """Test NotFoundException with default message."""
        error = NotFoundException()
        assert str(error) == "Resource not found"
        assert error.code == 404

    def test_validation_exception(self):
        """Test ValidationException."""
        error = ValidationException("Invalid data")
        assert str(error) == "Invalid data"
        assert error.code == 400

    def test_conflict_exception(self):
        """Test ConflictException."""
        error = ConflictException("Conflict occurred")
        assert str(error) == "Conflict occurred"
        assert error.code == 409

    def test_unauthorized_exception(self):
        """Test UnauthorizedException."""
        error = UnauthorizedException("Not authorized")
        assert str(error) == "Not authorized"
        assert error.code == 401

    def test_forbidden_exception(self):
        """Test ForbiddenException."""
        error = ForbiddenException("Access forbidden")
        assert str(error) == "Access forbidden"
        assert error.code == 403
