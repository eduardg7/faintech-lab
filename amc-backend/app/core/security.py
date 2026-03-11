"""Security utilities for JWT authentication and password hashing."""
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import jwt, JWTError
import bcrypt
import secrets
import hashlib

from config import settings


# Password hashing functions
def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    # Truncate to 72 bytes for bcrypt
    password_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    password_bytes = plain_password.encode('utf-8')[:72]
    hashed_bytes = hashed_password.encode('utf-8')
    try:
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        return False


# JWT Configuration
JWT_SECRET_KEY = secrets.token_urlsafe(32)  # Generate on startup
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30
JWT_REFRESH_TOKEN_EXPIRE_DAYS = 7


def create_access_token(
    subject: str,
    workspace_id: str,
    email: str,
    expires_delta: Optional[timedelta] = None,
    additional_claims: Optional[Dict[str, Any]] = None
) -> str:
    """
    Create a JWT access token.
    
    Args:
        subject: User ID
        workspace_id: Workspace ID for multi-tenancy
        email: User email
        expires_delta: Custom expiration time
        additional_claims: Extra claims to include
    
    Returns:
        JWT access token string
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "sub": str(subject),
        "workspace_id": str(workspace_id),
        "email": email,
        "type": "access",
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "jti": secrets.token_urlsafe(16)  # JWT ID for revocation
    }
    
    if additional_claims:
        to_encode.update(additional_claims)
    
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    subject: str,
    workspace_id: str,
    expires_delta: Optional[timedelta] = None
) -> tuple[str, str, datetime]:
    """
    Create a JWT refresh token.
    
    Args:
        subject: User ID
        workspace_id: Workspace ID
        expires_delta: Custom expiration time
    
    Returns:
        Tuple of (token, token_hash, expires_at)
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    
    jti = secrets.token_urlsafe(32)
    
    to_encode = {
        "sub": str(subject),
        "workspace_id": str(workspace_id),
        "type": "refresh",
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "jti": jti
    }
    
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    
    # Hash for storage (we don't store raw tokens)
    token_hash = hashlib.sha256(encoded_jwt.encode()).hexdigest()
    
    return encoded_jwt, token_hash, expire


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and validate a JWT token.
    
    Args:
        token: JWT token string
    
    Returns:
        Decoded payload or None if invalid
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None


def verify_token(token: str, expected_type: str = "access") -> Optional[Dict[str, Any]]:
    """
    Verify a JWT token and check its type.
    
    Args:
        token: JWT token string
        expected_type: Expected token type ('access' or 'refresh')
    
    Returns:
        Decoded payload or None if invalid
    """
    payload = decode_token(token)
    
    if not payload:
        return None
    
    # Check token type
    if payload.get("type") != expected_type:
        return None
    
    # Check expiration
    exp = payload.get("exp")
    if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
        return None
    
    return payload


class TokenData:
    """Data extracted from a validated JWT token."""
    
    def __init__(self, payload: Dict[str, Any]):
        self.user_id: str = payload.get("sub", "")
        self.workspace_id: str = payload.get("workspace_id", "")
        self.email: str = payload.get("email", "")
        self.token_type: str = payload.get("type", "")
        self.jti: str = payload.get("jti", "")
        self.exp: Optional[datetime] = None
        
        exp_timestamp = payload.get("exp")
        if exp_timestamp:
            self.exp = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
    
    @classmethod
    def from_token(cls, token: str, expected_type: str = "access") -> Optional["TokenData"]:
        """Create TokenData from a JWT token."""
        payload = verify_token(token, expected_type)
        if not payload:
            return None
        return cls(payload)
    
    def __repr__(self) -> str:
        return f"<TokenData(user_id={self.user_id}, workspace_id={self.workspace_id}, type={self.token_type})>"
