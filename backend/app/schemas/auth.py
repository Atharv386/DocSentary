from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class GitHubAuthRequest(BaseModel):
    code: str
    redirect_uri: Optional[str] = None


class DirectAuthRequest(BaseModel):
    username: str
    password: Optional[str] = "devpassword"


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class OrganizationSummary(BaseModel):
    id: str
    slug: str
    name: str
    role: str = "member"

    model_config = {"from_attributes": True}


class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: bool
    created_at: datetime
    organization: Optional[OrganizationSummary] = None

    model_config = {"from_attributes": True}


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse
