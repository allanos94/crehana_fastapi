"""Tests for infrastructure components."""

from unittest.mock import patch

from app.infrastructure.database import SessionLocal, engine, init_db


class TestDatabase:
    """Test database infrastructure."""

    def test_database_url_from_env(self):
        """Test that DATABASE_URL is properly loaded from environment."""
        import os

        assert os.getenv("DATABASE_URL") is not None

    @patch("app.infrastructure.database.Base.metadata.create_all")
    def test_init_db(self, mock_create_all):
        """Test database initialization."""
        init_db()
        mock_create_all.assert_called_once_with(bind=engine)

    def test_session_local_factory(self):
        """Test SessionLocal factory is properly configured."""
        assert SessionLocal is not None

        # Test creating a session
        session = SessionLocal()
        assert session is not None
        session.close()

    def test_engine_configuration(self):
        """Test engine is properly configured."""
        assert engine is not None
        assert hasattr(engine, "dialect")


class TestSessionManagement:
    """Test session management."""

    def test_database_session_lifecycle(self, db_session):
        """Test database session lifecycle."""
        # This test uses the existing db_session fixture
        # to verify it works correctly
        assert db_session is not None  # Test that we can execute a query
        from sqlalchemy import text

        result = db_session.execute(text("SELECT 1 as test")).fetchone()
        assert result[0] == 1
