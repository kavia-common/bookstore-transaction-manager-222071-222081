from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.security import get_current_user, get_password_hash, verify_password, create_access_token
from src.core.db import get_db
from src.models.models import User
from src.schemas.auth import Token, UserCreate, UserLogin, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, summary="Register user", description="Create a new user account.")
def register_user(payload: UserCreate, db: Session = Depends(get_db)) -> UserOut:
    """Register a new user.

    Parameters:
        payload: UserCreate containing email, password, and optional full_name.
        db: SQLAlchemy session.

    Returns:
        UserOut: The created user (without password).
    """
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user = User(
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=get_password_hash(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user  # Pydantic model will convert


@router.post("/login", response_model=Token, summary="Login", description="Authenticate user and get a JWT token.")
def login(payload: UserLogin, db: Session = Depends(get_db)) -> Token:
    """Authenticate and return JWT access token."""
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

    token = create_access_token(subject=user.email)
    return Token(access_token=token, token_type="bearer")


@router.get("/me", response_model=UserOut, summary="Current user", description="Return the current authenticated user.")
def me(current_user: User = Depends(get_current_user)) -> UserOut:
    """Return the current authenticated user."""
    return current_user
