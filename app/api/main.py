"""
FastAPI main application module.

This module sets up the FastAPI application with all routes and middleware.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import auth, task, task_list
from app.infrastructure.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown events."""
    # Startup
    try:
        init_db()
    except Exception as e:
        print(f"Failed to initialize database: {e}")
    yield
    # Shutdown - cleanup if needed


app = FastAPI(
    title="Task Management API",
    description="A RESTful API for managing tasks and task lists",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(task.router, prefix="/api/v1/tasks", tags=["tasks"])
app.include_router(task_list.router, prefix="/api/v1/task-lists", tags=["task-lists"])


@app.get("/")
def read_root():
    """Root endpoint with API information."""
    return {
        "message": "Task Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "task-management-api"}
