"""Secrets detection for memory system to prevent accidental credential leakage."""

import re
import time
import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import List, Optional, Tuple


class SecretType(str, Enum):
    """Types of secrets that can be detected."""
    API_KEY = "api_key"
    BEARER_TOKEN = "bearer_token"
    JWT = "jwt_token"
    OAUTH_TOKEN = "oauth_token"
    PASSWORD = "password"
    AWS_ACCESS_KEY = "aws_access_key"
    AWS_SECRET_KEY = "aws_secret_key"
    PRIVATE_KEY = "private_key"
    DATABASE_URL = "database_url"
    GENERIC_SECRET = "generic_secret"


@dataclass
class DetectedSecret:
    """Information about a detected secret."""
    secret_type: SecretType
    pattern_name: str
    matched_text: str
    start_pos: int
    end_pos: int
    masked_preview: str
    
    def to_dict(self):
        return {
            "secret_type": self.secret_type.value,
            "pattern_name": self.pattern_name,
            "masked_preview": self.masked_preview,
            "start_pos": self.start_pos,
            "end_pos": self.end_pos
        }


class SecurityError(Exception):
    """Raised when secrets are detected in memory content."""
    
    def __init__(self, message: str, detected_secrets: List[DetectedSecret]):
        super().__init__(message)
        self.detected_secrets = detected_secrets
        self.message = message
    
    def to_dict(self):
        return {
            "error": "SecurityError",
            "message": self.message,
            "detected_secrets": [s.to_dict() for s in self.detected_secrets]
        }


# Secret detection patterns with entropy and keyword pre-filtering
# Format: (pattern_regex, secret_type, pattern_name)
SECRET_PATTERNS = [
    # OpenAI API keys (sk-...) - allow hyphens in key body
    (r'\bsk-[a-zA-Z0-9]{20,}T3BlbkFJ[a-zA-Z0-9]{10,}\b', SecretType.API_KEY, "openai_api_key"),
    (r'\bsk-[a-zA-Z0-9-]{48,}\b', SecretType.API_KEY, "openai_api_key_v2"),
    
    # Generic API keys with common prefixes
    (r'\b(?:api[_-]?key|apikey|api[_-]?token)\W*[\"\']?([a-zA-Z0-9_-]{20,})[\"\']?', SecretType.API_KEY, "generic_api_key"),
    (r'\bx-api-key\W*[\"\']?([a-zA-Z0-9_-]{20,})[\"\']?', SecretType.API_KEY, "x_api_key_header"),
    
    # Bearer tokens
    (r'\bBearer\s+[a-zA-Z0-9._-]{20,}', SecretType.BEARER_TOKEN, "bearer_token"),
    (r'\bbearer\s+[a-zA-Z0-9._-]{20,}', SecretType.BEARER_TOKEN, "bearer_token_lower"),
    
    # JWT tokens (three base64 parts separated by dots)
    (r'\beyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*\b', SecretType.JWT, "jwt_token"),
    
    # OAuth tokens
    (r'\b(?:oauth[_-]?token|access[_-]?token)\W*[\"\']?([a-zA-Z0-9._-]{20,})[\"\']?', SecretType.OAUTH_TOKEN, "oauth_token"),
    
    # Password patterns
    (r'\b(?:password|passwd|pwd)\W*[\"\']?([^\s"\']{8,})[\"\']?', SecretType.PASSWORD, "password_assignment"),
    
    # AWS Access Key ID
    (r'\bAKIA[0-9A-Z]{16}\b', SecretType.AWS_ACCESS_KEY, "aws_access_key_id"),
    
    # AWS Secret Access Key (40 character base64-like string after keyword)
    (r'\b(?:aws[_-]?secret[_-]?access[_-]?key|aws[_-]?secret[_-]?key|secret[_-]?access[_-]?key)\W*[\"\']?([a-zA-Z0-9/+=]{40})[\"\']?', SecretType.AWS_SECRET_KEY, "aws_secret_key"),
    
    # Private key markers
    (r'-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----', SecretType.PRIVATE_KEY, "private_key_pem"),
    (r'-----BEGIN\s+OPENSSH\s+PRIVATE\s+KEY-----', SecretType.PRIVATE_KEY, "private_key_openssh"),
    
    # Database URLs with credentials
    (r'\b(?:postgres|mysql|mongodb|redis)://[^:]+:[^@]+@[^\s]+', SecretType.DATABASE_URL, "database_url_with_creds"),
    
    # Generic secret patterns with high entropy indicators
    (r'\b(?:secret|token|auth)[_-]?(?:key|token)?\W*[\"\']?([a-zA-Z0-9_/-]{32,})[\"\']?', SecretType.GENERIC_SECRET, "generic_secret"),
]

# Keywords that trigger deeper scanning (pre-filter optimization)
TRIGGER_KEYWORDS = [
    'sk-', 'apikey', 'api_key', 'api-key', 'x-api-key',
    'bearer', 'jwt', 'oauth', 'token',
    'password', 'passwd', 'pwd',
    'akia', 'aws', 'secret',
    'private_key', 'private-key',
    'postgres://', 'mysql://', 'mongodb://', 'redis://',
]

# Paths/patterns to skip (allowlist for known safe content)
ALLOWLIST_PATTERNS = [
    r'\btest[_-]?(?:api[_-]?key|token|password)\b',  # Test fixtures
    r'\b(?:example|sample|dummy|placeholder)\b',  # Example values
    r'\bxxx+\b',  # Redacted placeholders (xxx, xxxx, etc.)
    r'\bredacted\b',
    r'\b\[REDACTED\]\b',
]


def _contains_trigger_keyword(content: str) -> bool:
    """Check if content contains any trigger keyword (pre-filter optimization)."""
    if not content:
        return False
    content_lower = content.lower()
    return any(keyword in content_lower for keyword in TRIGGER_KEYWORDS)


def _is_allowlisted(content: str, match_start: int, match_end: int) -> bool:
    """Check if a match is in the allowlist (known safe patterns)."""
    # Get surrounding context (50 chars before and after)
    context_start = max(0, match_start - 50)
    context_end = min(len(content), match_end + 50)
    context = content[context_start:context_end].lower()
    
    return any(re.search(pattern, context, re.IGNORECASE) for pattern in ALLOWLIST_PATTERNS)


def _mask_secret(text: str) -> str:
    """Create a masked preview of a secret for safe logging."""
    if len(text) <= 8:
        return '*' * len(text)
    
    # Show first 4 and last 4 characters
    return f"{text[:4]}...{text[-4:]}"


def _calculate_entropy(text: str) -> float:
    """Calculate Shannon entropy of a string (higher = more random = likely secret)."""
    if not text:
        return 0.0
    
    import math
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    
    entropy = 0.0
    for count in freq.values():
        p = count / len(text)
        entropy -= p * math.log2(p)
    
    return entropy


def detect_secrets(content: str, min_entropy: float = 3.5) -> List[DetectedSecret]:
    """
    Scan content for potential secrets and sensitive data.
    
    Args:
        content: Text content to scan
        min_entropy: Minimum entropy threshold for generic secret detection
        
    Returns:
        List of DetectedSecret objects found in content
        
    Performance:
        Optimized with keyword pre-filtering. Typical <5ms for 1KB content.
    """
    start_time = time.time()
    detected: List[DetectedSecret] = []
    
    # Optimization: Skip if no trigger keywords found
    if not _contains_trigger_keyword(content):
        return detected
    
    # Scan for each pattern
    for pattern_regex, secret_type, pattern_name in SECRET_PATTERNS:
        try:
            for match in re.finditer(pattern_regex, content, re.IGNORECASE):
                match_text = match.group(0)
                match_start = match.start()
                match_end = match.end()
                
                # Skip if allowlisted
                if _is_allowlisted(content, match_start, match_end):
                    continue
                
                # For generic secrets, verify entropy
                if secret_type == SecretType.GENERIC_SECRET:
                    entropy = _calculate_entropy(match_text)
                    if entropy < min_entropy:
                        continue
                
                detected.append(DetectedSecret(
                    secret_type=secret_type,
                    pattern_name=pattern_name,
                    matched_text=match_text,
                    start_pos=match_start,
                    end_pos=match_end,
                    masked_preview=_mask_secret(match_text)
                ))
        except re.error:
            # Skip invalid regex patterns
            continue
    
    # Log performance if slow
    elapsed_ms = (time.time() - start_time) * 1000
    if elapsed_ms > 10:
        import warnings
        warnings.warn(f"Secrets detection took {elapsed_ms:.1f}ms (content length: {len(content)})")
    
    return detected


def scan_and_validate(content: str, agent_id: str = "unknown", log_blocked: bool = True) -> Tuple[bool, List[DetectedSecret]]:
    """
    Scan content for secrets and validate if safe to write.
    
    Args:
        content: Text content to scan
        agent_id: Agent ID attempting the write (for logging)
        log_blocked: Whether to log blocked attempts to security.log
        
    Returns:
        Tuple of (is_safe, detected_secrets)
        
    Raises:
        SecurityError: If secrets are detected (blocking the write)
    """
    detected = detect_secrets(content)
    
    if detected:
        # Log the blocked attempt
        if log_blocked:
            _log_blocked_attempt(agent_id, detected, content[:200])
        
        # Raise security error
        error_msg = f"Blocked write: {len(detected)} secret(s) detected in content"
        raise SecurityError(error_msg, detected)
    
    return True, detected


def _log_blocked_attempt(agent_id: str, secrets: List[DetectedSecret], content_preview: str):
    """
    Log blocked write attempts to security log.
    
    Log path: ~/.agent-memory/security.log
    Format: JSONL with timestamp, agent_id, pattern types, and masked preview
    """
    log_path = Path.home() / ".agent-memory" / "security.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        "event": "blocked_write",
        "agent_id": agent_id,
        "secrets_detected": len(secrets),
        "secret_types": list(set(s.secret_type.value for s in secrets)),
        "patterns": [s.pattern_name for s in secrets],
        "masked_previews": [s.masked_preview for s in secrets],
        "content_preview": content_preview[:100] + "..." if len(content_preview) > 100 else content_preview
    }
    
    import json
    with open(log_path, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')


# Convenience function for integration with MemoryStore
def check_content_safe(content: str, agent_id: str = "unknown") -> str:
    """
    Check if content is safe to write to memory.
    
    Args:
        content: Content to check
        agent_id: Agent ID for logging
        
    Returns:
        Original content if safe
        
    Raises:
        SecurityError: If secrets detected
    """
    scan_and_validate(content, agent_id)
    return content
