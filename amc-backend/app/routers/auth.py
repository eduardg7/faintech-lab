"""Authentication router with JWT endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from datetime import datetime, timezone
from typing import Optional

from app.core.database import get_db
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
    TokenData,
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
)
from app.core.errors import AMCError, ValidationError, NotFoundError
from app.models.user import User, RefreshToken
from app.models.workspace import Workspace
from app.schemas.auth import (
    UserRegister,
    UserLogin,
    TokenResponse,
    RefreshRequest,
    UserResponse,
    AuthResponse,
    LogoutRequest,
    MessageResponse,
)


router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Dependency to get the current authenticated user from JWT token.
    
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    token_data = TokenData.from_token(token, expected_type="access")
    
    if not token_data:
        raise credentials_exception
    
    # Get user from database
    query = select(User).where(
        and_(User.id == token_data.user_id, User.is_active == True)
    )
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise credentials_exception
    
    return user


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user"
)
async def register(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user account.
    
    - **email**: User email address (unique)
    - **password**: Password (min 8 characters)
    - **full_name**: Optional full name
    - **workspace_name**: Optional workspace name (creates new workspace)
    """
    # Check if user already exists
    existing_query = select(User).where(User.email == user_data.email)
    existing_result = await db.execute(existing_query)
    if existing_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    # Create or get workspace
    workspace_id: str
    if user_data.workspace_name:
        # Create new workspace
        workspace = Workspace(
            name=user_data.workspace_name,
            slug=user_data.workspace_name.lower().replace(" ", "-")[:100],
            tier="pro"
        )
        db.add(workspace)
        await db.flush()
        workspace_id = workspace.id
    else:
        # Use default workspace (for now, create a personal one)
        workspace = Workspace(
            name=f"Personal - {user_data.email}",
            slug=user_data.email.split("@")[0][:100],
            tier="pro"
        )
        db.add(workspace)
        await db.flush()
        workspace_id = workspace.id
    
    # Create user
    user = User(
        workspace_id=workspace_id,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        full_name=user_data.full_name,
        is_active=True,
        is_verified=True,  # For MVP, auto-verify (add email verification later)
    )
    db.add(user)
    await db.flush()
    
    # Create tokens
    access_token = create_access_token(
        subject=user.id,
        workspace_id=user.workspace_id,
        email=user.email
    )
    refresh_token_str, token_hash, expires_at = create_refresh_token(
        subject=user.id,
        workspace_id=user.workspace_id
    )
    
    # Store refresh token
    refresh_token = RefreshToken(
        user_id=user.id,
        token_hash=token_hash,
        jti=refresh_token_str.split(".")[-1][:64],  # Use last part as JTI
        expires_at=expires_at
    )
    db.add(refresh_token)
    await db.commit()
    
    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token_str,
        token_type="bearer",
        expires_in=JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            workspace_id=user.workspace_id,
            created_at=user.created_at,
            last_login_at=user.last_login_at
        )
    )


@router.post(
    "/login",
    response_model=AuthResponse,
    summary="Login with email and password"
)
async def login(
    credentials: UserLogin,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Login with email and password.
    
    - **email**: User email address
    - **password**: Password
    
    Returns access token, refresh token, and user info.
    """
    # Find user by email
    query = select(User).where(
        and_(User.email == credentials.email, User.is_active == True)
    )
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login
    user.last_login_at = datetime.utcnow()
    
    # Create tokens
    access_token = create_access_token(
        subject=user.id,
        workspace_id=user.workspace_id,
        email=user.email
    )
    refresh_token_str, token_hash, expires_at = create_refresh_token(
        subject=user.id,
        workspace_id=user.workspace_id
    )
    
    # Store refresh token with device info
    refresh_token = RefreshToken(
        user_id=user.id,
        token_hash=token_hash,
        jti=refresh_token_str.split(".")[-1][:64],
        expires_at=expires_at,
        user_agent=request.headers.get("user-agent"),
        ip_address=request.client.host if request.client else None
    )
    db.add(refresh_token)
    await db.commit()
    
    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token_str,
        token_type="bearer",
        expires_in=JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            workspace_id=user.workspace_id,
            created_at=user.created_at,
            last_login_at=user.last_login_at
        )
    )


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token"
)
async def refresh_token(
    data: RefreshRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Refresh access token using refresh token.
    
    - **refresh_token**: Valid refresh token
    
    Returns new access token and refresh token.
    """
    # Verify refresh token
    token_data = TokenData.from_token(data.refresh_token, expected_type="refresh")
    
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if token is revoked in database
    import hashlib
    token_hash = hashlib.sha256(data.refresh_token.encode()).hexdigest()
    
    query = select(RefreshToken).where(
        and_(
            RefreshToken.token_hash == token_hash,
            RefreshToken.is_revoked == False
        )
    )
    result = await db.execute(query)
    stored_token = result.scalar_one_or_none()
    
    if not stored_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token revoked or expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user
    user_query = select(User).where(User.id == token_data.user_id)
    user_result = await db.execute(user_query)
    user = user_result.scalar_one_or_none()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Revoke old refresh token (rotation)
    stored_token.revoke()
    
    # Create new tokens
    access_token = create_access_token(
        subject=user.id,
        workspace_id=user.workspace_id,
        email=user.email
    )
    new_refresh_token_str, new_token_hash, expires_at = create_refresh_token(
        subject=user.id,
        workspace_id=user.workspace_id
    )
    
    # Store new refresh token
    new_refresh_token = RefreshToken(
        user_id=user.id,
        token_hash=new_token_hash,
        jti=new_refresh_token_str.split(".")[-1][:64],
        expires_at=expires_at
    )
    db.add(new_refresh_token)
    await db.commit()
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token_str,
        token_type="bearer",
        expires_in=JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="Logout and revoke refresh token"
)
async def logout(
    data: LogoutRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Logout and revoke refresh token.
    
    - **refresh_token**: Optional refresh token to revoke
    
    If no refresh token provided, revokes all user's refresh tokens.
    """
    if data.refresh_token:
        # Revoke specific token
        import hashlib
        token_hash = hashlib.sha256(data.refresh_token.encode()).hexdigest()
        
        query = select(RefreshToken).where(
            and_(
                RefreshToken.token_hash == token_hash,
                RefreshToken.user_id == current_user.id
            )
        )
        result = await db.execute(query)
        stored_token = result.scalar_one_or_none()
        
        if stored_token:
            stored_token.revoke()
    else:
        # Revoke all user's refresh tokens
        query = select(RefreshToken).where(
            and_(
                RefreshToken.user_id == current_user.id,
                RefreshToken.is_revoked == False
            )
        )
        result = await db.execute(query)
        tokens = result.scalars().all()
        
        for token in tokens:
            token.revoke()
    
    await db.commit()
    
    return MessageResponse(message="Successfully logged out")


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user"
)
async def get_me(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user info.
    
    Requires valid JWT access token in Authorization header.
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        workspace_id=current_user.workspace_id,
        created_at=current_user.created_at,
        last_login_at=current_user.last_login_at
    )
