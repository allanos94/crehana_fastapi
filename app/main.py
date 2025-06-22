from fastapi import FastAPI

app = FastAPI(
    title="Task Management API",
    description="A FastAPI backend for task and task list management",
    version="1.0.0",
)


@app.get("/")
def read_root():
    """
    Root endpoint for health check.

    Returns:
        dict: A simple message indicating the API is running.
    """
    return {"message": "Task management API is running"}
