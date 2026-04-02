"""Auth schemas for JWT authentication."""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserRegister(BaseModel):
    """Schema for user registration."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, max_length=128, description="Password (min 8 chars)")
    full_name: Optional[str] = Field(None, max_length=255, description="Full name")
    workspace_name: Optional[str] = Field(None, max_length=255, description="Workspace name (creates new workspace)")
    # UTM tracking for Week 2 GTM channel attribution
    utm_source: Optional[str] = Field(None, max_length=255, description="UTM source parameter (e.g., 'hn', 'reddit', 'linkedin')")
    utm_medium: Optional[str] = Field(None, max_length=255, description="UTM medium parameter (e.g., 'post', 'article', 'referral')")
    utm_campaign: Optional[str] = Field(None, max_length=255, description="UTM campaign identifier")
    utm_content: Optional[str] = Field(None, max_length=255, description="UTM content parameter (A/B test variant)")
    utm_term: Optional[str] = Field(None, max_length=255, description="UTM term/keyword parameter")
    utm_referrer: Optional[str] = Field(None, max_length=255, description="UTM referrer (URL of referring page)")


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="Password")


class TokenResponse(BaseModel):
    """Schema for token response."""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Access token expiration in seconds")


class RefreshRequest(BaseModel):
    """Schema for token refresh request."""
    refresh_token: str = Field(..., description="Refresh token")


class UserResponse(BaseModel):
    """Schema for user response."""
    id: str
    email: str
    full_name: Optional[str]
    is_active: bool
    is_verified: bool
    workspace_id: str
    created_at: datetime
    last_login_at: Optional[datetime]

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    """Combined response with tokens and user info."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class LogoutRequest(BaseModel):
    """Schema for logout request."""
    refresh_token: Optional[str] = Field(None, description="Refresh token to revoke")


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str
