from unittest.mock import Mock, PropertyMock

from app.infrastructure.db.models.task import Task

# Test the correct mock behavior
task = Mock(spec=Task)
task.id = 1

# Method 1: Configure the property to raise an exception
type(task).title = PropertyMock(side_effect=Exception("Database error"))

try:
    print(f"Task title: {task.title}")
except Exception as e:
    print(f"Exception caught: {e}")

try:
    title = task.title
    print(f"Title: {title}")
except Exception as e:
    print(f"Exception caught: {e}")

print("\n--- Method 2: Configure property directly ---")

# Method 2: Configure the Mock to raise when accessing title
task2 = Mock(spec=Task)
task2.id = 1
task2.configure_mock(**{"title": Mock(side_effect=Exception("Database error"))})

try:
    title = task2.title
    print(f"Title: {title}")
except Exception as e:
    print(f"Exception caught: {e}")
