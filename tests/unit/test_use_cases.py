"""Unit tests for use cases."""

from unittest.mock import Mock, patch

import pytest

from app.domain.models.task import Task
from app.domain.models.task_list import TaskList
from app.domain.value_objects import TaskListName, TaskTitle
from app.exceptions import NotFoundException
from app.use_cases.task.create_task import create_task
from app.use_cases.task.get_task import get_task
from app.use_cases.task.list_tasks import list_tasks
from app.use_cases.task_list.create_task_list import create_task_list


class TestCreateTask:
    """Test create_task use case."""

    @patch("app.use_cases.task.create_task.TaskListRepository")
    @patch("app.use_cases.task.create_task.TaskRepository")
    def test_create_task_success(self, mock_task_repo_class, mock_task_list_repo_class):
        """Test successful task creation."""
        # Setup mocks
        mock_db = Mock()
        mock_task_repo = Mock()
        mock_task_list_repo = Mock()
        mock_task_repo_class.return_value = mock_task_repo
        mock_task_list_repo_class.return_value = mock_task_list_repo

        # Mock task list exists
        task_list = TaskList(name=TaskListName(value="Test List"))
        task_list.id = 1
        mock_task_list_repo.get_by_id.return_value = task_list

        # Mock task creation
        created_task = Task(title=TaskTitle(value="Test Task"), task_list_id=1)
        created_task.id = 1
        mock_task_repo.create.return_value = created_task

        # Execute
        result = create_task(
            db=mock_db, task_list_id=1, title="Test Task", description="Test description"
        )

        # Assert
        assert result == created_task
        mock_task_list_repo.get_by_id.assert_called_once_with(1)
        mock_task_repo.create.assert_called_once()

    @patch("app.use_cases.task.create_task.TaskListRepository")
    def test_create_task_nonexistent_task_list(self, mock_task_list_repo_class):
        """Test creating task with non-existent task list."""
        # Setup mocks
        mock_db = Mock()
        mock_task_list_repo = Mock()
        mock_task_list_repo_class.return_value = mock_task_list_repo

        # Mock task list doesn't exist
        mock_task_list_repo.get_by_id.return_value = None

        # Execute & Assert
        with pytest.raises(NotFoundException):
            create_task(db=mock_db, task_list_id=99999, title="Test Task")


class TestGetTask:
    """Test get_task use case."""

    @patch("app.use_cases.task.get_task.TaskRepository")
    def test_get_task_success(self, mock_task_repo_class):
        """Test successful task retrieval."""
        # Setup mocks
        mock_db = Mock()
        mock_task_repo = Mock()
        mock_task_repo_class.return_value = mock_task_repo

        # Mock task exists
        task = Task(title=TaskTitle(value="Test Task"), task_list_id=1)
        task.id = 1
        mock_task_repo.get_by_id.return_value = task

        # Execute
        result = get_task(db=mock_db, task_id=1)

        # Assert
        assert result == task
        mock_task_repo.get_by_id.assert_called_once_with(1)

    @patch("app.use_cases.task.get_task.TaskRepository")
    def test_get_nonexistent_task(self, mock_task_repo_class):
        """Test getting non-existent task."""
        # Setup mocks
        mock_db = Mock()
        mock_task_repo = Mock()
        mock_task_repo_class.return_value = mock_task_repo

        # Mock task doesn't exist
        mock_task_repo.get_by_id.return_value = None

        # Execute & Assert
        with pytest.raises(NotFoundException):
            get_task(db=mock_db, task_id=99999)


class TestListTasks:
    """Test list_tasks use case."""

    @patch("app.use_cases.task.list_tasks.TaskListRepository")
    @patch("app.use_cases.task.list_tasks.TaskRepository")
    def test_list_tasks_success(self, mock_task_repo_class, mock_task_list_repo_class):
        """Test successful task listing."""
        # Setup mocks
        mock_db = Mock()
        mock_task_repo = Mock()
        mock_task_list_repo = Mock()
        mock_task_repo_class.return_value = mock_task_repo
        mock_task_list_repo_class.return_value = mock_task_list_repo

        # Mock task list exists
        mock_task_list = Mock()
        mock_task_list_repo.get_by_id.return_value = mock_task_list

        # Mock tasks
        tasks = [
            Task(title=TaskTitle(value="Task 1"), task_list_id=1),
            Task(title=TaskTitle(value="Task 2"), task_list_id=1),
        ]

        # Mock the repository methods
        mock_task_repo.get_tasks_with_filters.return_value = tasks
        mock_task_repo.get_by_task_list_id.return_value = tasks

        # Execute
        result = list_tasks(db=mock_db, task_list_id=1, skip=0, limit=10)

        # Assert
        assert result["tasks"] == tasks
        assert result["total"] == 2


class TestCreateTaskList:
    """Test create_task_list use case."""

    @patch("app.use_cases.task_list.create_task_list.TaskListRepository")
    def test_create_task_list_success(self, mock_task_list_repo_class):
        """Test successful task list creation."""
        # Setup mocks
        mock_db = Mock()
        mock_task_list_repo = Mock()
        mock_task_list_repo_class.return_value = mock_task_list_repo
        # Mock task list creation
        created_task_list = TaskList(name=TaskListName(value="Test List"))
        created_task_list.id = 1
        mock_task_list_repo.create.return_value = created_task_list

        # Mock that no existing task list with same name exists
        mock_task_list_repo.get_by_name.return_value = None
        # Execute
        result = create_task_list(db=mock_db, name="Test List")

        # Assert
        assert result == created_task_list
        mock_task_list_repo.create.assert_called_once()
