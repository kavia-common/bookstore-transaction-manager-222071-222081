from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Type of the token")


class UserBase(BaseModel):
    email: EmailStr = Field(..., description="Unique email for the user")
    full_name: str | None = Field(default=None, description="Full name of the user")


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Password for user registration")


class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="Email for login")
    password: str = Field(..., description="Password for login")


class UserOut(UserBase):
    id: int = Field(..., description="User identifier")

    class Config:
        from_attributes = True
