"""Integration tests for TaskList endpoints with JWT authentication."""

from fastapi.testclient import TestClient


class TestTaskListEndpoints:
    """Test TaskList API endpoints."""

    def test_create_task_list(self, client: TestClient, auth_headers: dict[str, str]):
        """Test creating a new task list."""
        task_list_data = {
            "name": "New Task List",
        }

        response = client.post(
            "/api/v1/task-lists/", json=task_list_data, headers=auth_headers
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == task_list_data["name"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_task_list_without_auth(self, client: TestClient):
        """Test creating a task list without authentication."""
        task_list_data = {
            "name": "New Task List",
        }

        response = client.post("/api/v1/task-lists/", json=task_list_data)
        assert response.status_code == 401

    def test_create_task_list_invalid_name(
        self, client: TestClient, auth_headers: dict[str, str]
    ):
        """Test creating task list with invalid name."""
        task_list_data = {
            "name": "",  # Empty name should be invalid
        }

        response = client.post(
            "/api/v1/task-lists/", json=task_list_data, headers=auth_headers
        )
        assert response.status_code == 422

    def test_get_task_list(
        self, client: TestClient, sample_task_list, auth_headers: dict[str, str]
    ):
        """Test getting a specific task list."""
        response = client.get(
            f"/api/v1/task-lists/{sample_task_list.id}", headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_task_list.id
        assert data["name"] == sample_task_list.name

    def test_get_task_list_without_auth(self, client: TestClient, sample_task_list):
        """Test getting a task list without authentication."""
        response = client.get(f"/api/v1/task-lists/{sample_task_list.id}")
        assert response.status_code == 401

    def test_get_nonexistent_task_list(
        self, client: TestClient, auth_headers: dict[str, str]
    ):
        """Test getting a non-existent task list."""
        response = client.get("/api/v1/task-lists/99999", headers=auth_headers)
        assert response.status_code == 404

    def test_list_task_lists(self, client: TestClient, auth_headers: dict[str, str]):
        """Test listing task lists."""
        # Create some task lists first
        task_list_data_1 = {
            "name": "Task List 1",
        }
        task_list_data_2 = {
            "name": "Task List 2",
        }

        client.post("/api/v1/task-lists/", json=task_list_data_1, headers=auth_headers)
        client.post("/api/v1/task-lists/", json=task_list_data_2, headers=auth_headers)

        response = client.get("/api/v1/task-lists/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2

    def test_list_task_lists_without_auth(self, client: TestClient):
        """Test listing task lists without authentication."""
        response = client.get("/api/v1/task-lists/")
        assert response.status_code == 401

    def test_list_task_lists_with_pagination(
        self, client: TestClient, auth_headers: dict[str, str]
    ):
        """Test listing task lists with pagination."""
        # Create multiple task lists
        for i in range(5):
            task_list_data = {
                "name": f"Task List {i}",
            }
            client.post("/api/v1/task-lists/", json=task_list_data, headers=auth_headers)

        # Test pagination - API returns list directly
        response = client.get("/api/v1/task-lists/?skip=0&limit=2", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Should return at most 2 task lists due to limit
        assert len(data) <= 2

    def test_update_task_list(
        self, client: TestClient, sample_task_list, auth_headers: dict[str, str]
    ):
        """Test updating a task list."""
        update_data = {
            "name": "Updated Task List Name",
        }

        response = client.put(
            f"/api/v1/task-lists/{sample_task_list.id}",
            json=update_data,
            headers=auth_headers,
        )
        assert response.status_code == 200

        data = response.json()
        assert data["name"] == update_data["name"]

    def test_update_task_list_without_auth(self, client: TestClient, sample_task_list):
        """Test updating a task list without authentication."""
        update_data = {
            "name": "Updated Task List Name",
        }

        response = client.put(
            f"/api/v1/task-lists/{sample_task_list.id}", json=update_data
        )
        assert response.status_code == 401

    def test_update_nonexistent_task_list(
        self, client: TestClient, auth_headers: dict[str, str]
    ):
        """Test updating a non-existent task list."""
        update_data = {
            "name": "Updated Name",
        }

        response = client.put(
            "/api/v1/task-lists/99999", json=update_data, headers=auth_headers
        )
        assert response.status_code == 404

    def test_delete_task_list(
        self, client: TestClient, sample_task_list, auth_headers: dict[str, str]
    ):
        """Test deleting a task list."""
        response = client.delete(
            f"/api/v1/task-lists/{sample_task_list.id}", headers=auth_headers
        )
        assert response.status_code == 204

        # Verify task list is deleted
        get_response = client.get(
            f"/api/v1/task-lists/{sample_task_list.id}", headers=auth_headers
        )
        assert get_response.status_code == 404

    def test_delete_task_list_without_auth(self, client: TestClient, sample_task_list):
        """Test deleting a task list without authentication."""
        response = client.delete(f"/api/v1/task-lists/{sample_task_list.id}")
        assert response.status_code == 401

    def test_delete_nonexistent_task_list(
        self, client: TestClient, auth_headers: dict[str, str]
    ):
        """Test deleting a non-existent task list."""
        response = client.delete("/api/v1/task-lists/99999", headers=auth_headers)
        assert response.status_code == 404

    def test_create_task_list_duplicate_name(
        self, client: TestClient, auth_headers: dict[str, str]
    ):
        """Test creating task list with duplicate name."""
        task_list_data = {
            "name": "Duplicate Test List",
        }

        # Create first task list
        first_response = client.post(
            "/api/v1/task-lists/", json=task_list_data, headers=auth_headers
        )
        assert first_response.status_code == 201

        # Try to create second with same name
        second_response = client.post(
            "/api/v1/task-lists/", json=task_list_data, headers=auth_headers
        )
        # Depending on implementation, this might be 409 (conflict) or 201 (allowed)
        assert second_response.status_code in [201, 409]
