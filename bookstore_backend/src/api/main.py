from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from src.core.db import Base, engine, get_db

# Create FastAPI app with metadata and tags for better OpenAPI
app = FastAPI(
    title="Bookstore Backend",
    description="Handles book transaction management, user authentication, and related services.",
    version="0.1.0",
    openapi_tags=[
        {"name": "health", "description": "Health and status endpoints"},
    ],
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Consider restricting in production via env
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    """Ensure database tables are created at startup."""
    # Import models to register with Base metadata (already imported above)
    Base.metadata.create_all(bind=engine)


@app.get("/", tags=["health"], summary="Health Check", description="Check service health status.")
def health_check(db: Session = Depends(get_db)):
    """Basic health check endpoint.

    Parameters:
        db: Injected SQLAlchemy session to verify DB setup during request handling.

    Returns:
        A simple JSON payload indicating the service is healthy.
    """
    # Optionally perform a lightweight DB interaction in future
    return {"message": "Healthy"}
