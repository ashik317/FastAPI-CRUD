from fastapi import FastAPI

from .routers import course, user, auth
from app.startup import startup_db

# CREATE the FastAPI app
app = FastAPI(title="Course API")

# Register startup event
app.add_event_handler("startup", startup_db)

# Include routers
app.include_router(course.router)
app.include_router(user.router)
app.include_router(auth.router)
