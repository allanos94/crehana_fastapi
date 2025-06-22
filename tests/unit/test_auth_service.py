"""
Unit tests for authentication services.

This module tests:
- Password hashing and verification
- JWT token creation and validation
- User authentication logic
"""

from datetime import timedelta

from app.services.auth import AuthService


class TestAuthService:
    """Test cases for AuthService."""

    def test_password_hashing(self):
        """Test password hashing and verification."""
        password = "test_password_123"

        # Hash password
        hashed = AuthService.get_password_hash(password)

        # Verify hash is different from original password
        assert hashed != password
        assert hashed.startswith("$2b$")  # bcrypt hash prefix

        # Verify password verification works
        assert AuthService.verify_password(password, hashed) is True
        assert AuthService.verify_password("wrong_password", hashed) is False

    def test_jwt_token_creation(self):
        """Test JWT token creation."""
        user_data = {"sub": "test@example.com"}

        # Create token
        token = AuthService.create_access_token(user_data)

        # Verify token is a string
        assert isinstance(token, str)
        assert len(token) > 0

        # Verify token has three parts (header.payload.signature)
        assert len(token.split(".")) == 3

    def test_jwt_token_creation_with_expiry(self):
        """Test JWT token creation with custom expiry."""
        user_data = {"sub": "test@example.com"}
        expires_delta = timedelta(minutes=15)

        # Create token with custom expiry
        token = AuthService.create_access_token(user_data, expires_delta)

        # Verify token is created
        assert isinstance(token, str)
        assert len(token) > 0

    def test_jwt_token_verification_valid(self):
        """Test JWT token verification with valid token."""
        user_data = {"sub": "test@example.com"}

        # Create and verify token
        token = AuthService.create_access_token(user_data)
        payload = AuthService.verify_token(token)

        # Verify payload
        assert payload is not None
        assert payload["sub"] == "test@example.com"
        assert "exp" in payload

    def test_jwt_token_verification_invalid(self):
        """Test JWT token verification with invalid token."""
        invalid_token = "invalid.token.here"

        # Verify invalid token returns None
        payload = AuthService.verify_token(invalid_token)
        assert payload is None

    def test_jwt_token_verification_expired(self):
        """Test JWT token verification with expired token."""
        user_data = {"sub": "test@example.com"}

        # Create token with past expiry
        past_time = timedelta(minutes=-1)
        token = AuthService.create_access_token(user_data, past_time)

        # Verify expired token returns None
        payload = AuthService.verify_token(token)
        assert payload is None

    def test_get_user_from_token_valid(self):
        """Test extracting user from valid token."""
        email = "test@example.com"
        user_data = {"sub": email}

        # Create token and extract user
        token = AuthService.create_access_token(user_data)
        extracted_email = AuthService.get_user_from_token(token)

        assert extracted_email == email

    def test_get_user_from_token_invalid(self):
        """Test extracting user from invalid token."""
        invalid_token = "invalid.token.here"

        # Verify invalid token returns None
        extracted_email = AuthService.get_user_from_token(invalid_token)
        assert extracted_email is None

    def test_get_user_from_token_missing_sub(self):
        """Test extracting user from token without sub field."""
        user_data = {"user_id": "123"}  # Missing 'sub' field

        # Create token and try to extract user
        token = AuthService.create_access_token(user_data)
        extracted_email = AuthService.get_user_from_token(token)

        assert extracted_email is None
