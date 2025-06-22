"""Integration tests for task endpoints with JWT authentication."""

from fastapi.testclient import TestClient


class TestTaskEndpoints:
    """Test task API endpoints."""

    def test_create_task(
        self, client: TestClient, sample_task_list, auth_headers: dict[str, str]
    ):
        """Test creating a new task."""
        task_data = {
            "title": "Test Task",
            "description": "Task description",
            "priority": "high",
            "task_list_id": sample_task_list.id,
        }

        response = client.post("/api/v1/tasks/", json=task_data, headers=auth_headers)
        assert response.status_code == 201

        data = response.json()
        assert data["title"] == task_data["title"]
        assert data["description"] == task_data["description"]
        assert data["priority"] == task_data["priority"]
        assert data["task_list_id"] == task_data["task_list_id"]
        assert data["status"] == "pending"
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_task_without_auth(self, client: TestClient, sample_task_list):
        """Test creating a task without authentication."""
        task_data = {
            "title": "Test Task",
            "task_list_id": sample_task_list.id,
        }

        response = client.post("/api/v1/tasks/", json=task_data)
        assert response.status_code == 401

    def test_create_task_invalid_task_list(
        self, client: TestClient, auth_headers: dict[str, str]
    ):
        """Test creating a task with invalid task list."""
        task_data = {
            "title": "Test Task",
            "task_list_id": 99999,  # Non-existent task list
        }

        response = client.post("/api/v1/tasks/", json=task_data, headers=auth_headers)
        assert response.status_code == 404

    def test_create_task_missing_required_field(
        self, client: TestClient, sample_task_list, auth_headers: dict[str, str]
    ):
        """Test creating a task with missing title."""
        task_data = {
            "task_list_id": sample_task_list.id,
            # Missing title
        }

        response = client.post("/api/v1/tasks/", json=task_data, headers=auth_headers)
        assert response.status_code == 422

    def test_create_task_invalid_priority(
        self, client: TestClient, sample_task_list, auth_headers: dict[str, str]
    ):
        """Test creating a task with invalid priority."""
        task_data = {
            "title": "Test Task",
            "priority": "invalid",
            "task_list_id": sample_task_list.id,
        }

        response = client.post("/api/v1/tasks/", json=task_data, headers=auth_headers)
        assert response.status_code == 422

    def test_get_task(
        self, client: TestClient, sample_task, auth_headers: dict[str, str]
    ):
        """Test getting a specific task."""
        response = client.get(f"/api/v1/tasks/{sample_task.id}", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_task.id
        assert data["title"] == sample_task.title

    def test_get_task_without_auth(self, client: TestClient, sample_task):
        """Test getting a task without authentication."""
        response = client.get(f"/api/v1/tasks/{sample_task.id}")
        assert response.status_code == 401

    def test_get_nonexistent_task(self, client: TestClient, auth_headers: dict[str, str]):
        """Test getting a non-existent task."""
        response = client.get("/api/v1/tasks/99999", headers=auth_headers)
        assert response.status_code == 404

    def test_list_tasks(
        self, client: TestClient, sample_task_list, auth_headers: dict[str, str]
    ):
        """Test listing tasks."""
        # Create some tasks first using a valid task_list_id
        task_data_1 = {
            "title": "Task 1",
            "task_list_id": sample_task_list.id,  # Usar el ID del fixture
        }
        task_data_2 = {
            "title": "Task 2",
            "task_list_id": sample_task_list.id,  # Usar el ID del fixture
        }

        # Verificar que las tareas se crean exitosamente
        response1 = client.post("/api/v1/tasks/", json=task_data_1, headers=auth_headers)
        assert response1.status_code == 201  # Verificar que se creó exitosamente

        response2 = client.post("/api/v1/tasks/", json=task_data_2, headers=auth_headers)
        assert response2.status_code == 201  # Verificar que se creó exitosamente

        # Ahora listar las tareas
        response = client.get("/api/v1/tasks/", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Should have at least our 2 tasks
        assert len(data) >= 2

    def test_list_tasks_without_auth(self, client: TestClient):
        """Test listing tasks without authentication."""
        response = client.get("/api/v1/tasks/")
        assert response.status_code == 401

    def test_update_task(
        self, client: TestClient, sample_task, auth_headers: dict[str, str]
    ):
        """Test updating a task."""
        update_data = {
            "title": "Updated Task Title",
            "description": "Updated description",
        }

        response = client.put(
            f"/api/v1/tasks/{sample_task.id}",
            json=update_data,
            headers=auth_headers,
        )
        assert response.status_code == 200

        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["description"] == update_data["description"]

    def test_update_task_without_auth(self, client: TestClient, sample_task):
        """Test updating a task without authentication."""
        update_data = {
            "title": "Updated Task Title",
        }

        response = client.put(f"/api/v1/tasks/{sample_task.id}", json=update_data)
        assert response.status_code == 401

    def test_update_nonexistent_task(
        self, client: TestClient, auth_headers: dict[str, str]
    ):
        """Test updating a non-existent task."""
        update_data = {
            "title": "Updated Task Title",
        }

        response = client.put(
            "/api/v1/tasks/99999", json=update_data, headers=auth_headers
        )
        assert response.status_code == 404

    def test_delete_task(
        self, client: TestClient, sample_task, auth_headers: dict[str, str]
    ):
        """Test deleting a task."""
        response = client.delete(f"/api/v1/tasks/{sample_task.id}", headers=auth_headers)
        assert response.status_code == 204

        # Verify task is deleted
        get_response = client.get(f"/api/v1/tasks/{sample_task.id}", headers=auth_headers)
        assert get_response.status_code == 404

    def test_delete_task_without_auth(self, client: TestClient, sample_task):
        """Test deleting a task without authentication."""
        response = client.delete(f"/api/v1/tasks/{sample_task.id}")
        assert response.status_code == 401

    def test_delete_nonexistent_task(
        self, client: TestClient, auth_headers: dict[str, str]
    ):
        """Test deleting a non-existent task."""
        response = client.delete("/api/v1/tasks/99999", headers=auth_headers)
        assert response.status_code == 404

    def test_assign_task(
        self,
        client: TestClient,
        sample_task,
        sample_user,
        auth_headers: dict[str, str],
    ):
        """Test assigning a task to a user."""
        response = client.patch(
            f"/api/v1/tasks/{sample_task.id}/assign",
            json={"user_id": sample_user.id},
            headers=auth_headers,
        )
        assert response.status_code == 200

        data = response.json()
        assert data["user_id"] == sample_user.id

    def test_assign_task_without_auth(self, client: TestClient, sample_task, sample_user):
        """Test assigning a task without authentication."""
        response = client.patch(
            f"/api/v1/tasks/{sample_task.id}/assign",
            json={"user_id": sample_user.id},
        )
        assert response.status_code == 401

    def test_unassign_task(
        self, client: TestClient, sample_task, auth_headers: dict[str, str]
    ):
        """Test unassigning a task."""
        response = client.patch(
            f"/api/v1/tasks/{sample_task.id}/unassign", headers=auth_headers
        )
        assert response.status_code == 200

        data = response.json()
        assert data["user_id"] is None

    def test_unassign_task_without_auth(self, client: TestClient, sample_task):
        """Test unassigning a task without authentication."""
        response = client.patch(f"/api/v1/tasks/{sample_task.id}/unassign")
        assert response.status_code == 401

    def test_update_task_status(
        self, client: TestClient, sample_task, auth_headers: dict[str, str]
    ):
        """Test updating task status."""
        response = client.patch(
            f"/api/v1/tasks/{sample_task.id}/status",
            json={"status": "completed"},
            headers=auth_headers,
        )
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "completed"

    def test_update_task_status_without_auth(self, client: TestClient, sample_task):
        """Test updating task status without authentication."""
        response = client.patch(
            f"/api/v1/tasks/{sample_task.id}/status",
            json={"status": "completed"},
        )
        assert response.status_code == 401
