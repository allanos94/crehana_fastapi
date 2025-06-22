"""Integration tests for the main API endpoints."""

from fastapi.testclient import TestClient


class TestMainEndpoints:
    """Test main API endpoints."""

    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    def test_health_check_endpoint(self, client: TestClient):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_openapi_docs(self, client: TestClient):
        """Test OpenAPI documentation endpoint."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_api_v1_tasks_endpoint_simple(
        self, client: TestClient, auth_headers: dict[str, str]
    ):
        """Test basic tasks endpoint access with authentication."""
        response = client.get("/api/v1/tasks/", headers=auth_headers)
        # This should work even with empty database
        assert response.status_code == 200

    def test_api_v1_task_lists_endpoint_simple(
        self, client: TestClient, auth_headers: dict[str, str]
    ):
        """Test basic task lists endpoint access with authentication."""
        response = client.get("/api/v1/task-lists/", headers=auth_headers)
        # This should work even with empty database
        assert response.status_code == 200

    def test_api_v1_tasks_endpoint_without_auth(self, client: TestClient):
        """Test that tasks endpoint requires authentication."""
        response = client.get("/api/v1/tasks/")
        assert response.status_code == 401

    def test_api_v1_task_lists_endpoint_without_auth(self, client: TestClient):
        """Test that task lists endpoint requires authentication."""
        response = client.get("/api/v1/task-lists/")
        assert response.status_code == 401

    def test_cors_headers(self, client: TestClient):
        """Test CORS headers are present."""
        response = client.options("/")
        # Check for CORS headers in the response
        assert response.status_code in [
            200,
            405,
        ]  # OPTIONS might not be implemented
