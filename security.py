import re
import time
from typing import Dict, Tuple

MALICIOUS_DOMAINS = [
    # very small heuristic list for hackathon use
    "localhost@",  # obsfucated email-style
    "127.0.0.1@",
]

SUSPICIOUS_PATTERNS = [
    r"(?i)javascript:\s*",  # javascript: URLs
    r"(?i)data:\s*",        # data: URLs
    r"(?i)file:\\|file://",  # file protocol
]


def is_url_safe(url: str) -> Tuple[bool, str]:
    """Basic screening to reject obviously unsafe or unsupported URLs.
    Returns (is_safe, reason_if_not)."""
    if not url:
        return False, "Empty URL"
    trimmed = url.strip()
    # Reject dangerous schemes
    if re.match(r"^(?i)(javascript:|data:|file:)", trimmed):
        return False, "Unsupported URL scheme"
    # Reject embedded creds pattern like http://user:pass@host
    if re.search(r"://[^/]*?:[^/@]*?@", trimmed):
        return False, "Embedded credentials are not allowed"
    # Heuristic patterns
    for pat in SUSPICIOUS_PATTERNS:
        if re.search(pat, trimmed):
            return False, "Suspicious URL pattern"
    for token in MALICIOUS_DOMAINS:
        if token in trimmed:
            return False, "Suspicious host"
    return True, ""


def sanitize_text_for_llm(text: str, max_len: int = 8000) -> str:
    """Remove obvious secrets and truncate before sending to LLM."""
    if not text:
        return text
    scrubbed = text
    # mask typical secret patterns
    scrubbed = re.sub(r"(?i)(api[_-]?key\s*[:=]\s*)([\w\-]{16,})", r"\1[REDACTED]", scrubbed)
    scrubbed = re.sub(r"(?i)(secret[_-]?key\s*[:=]\s*)([\w\+/]{16,})", r"\1[REDACTED]", scrubbed)
    scrubbed = re.sub(r"(?i)(password\s*[:=]\s*)([^\s'\"]{6,})", r"\1[REDACTED]", scrubbed)
    # hard truncate
    if len(scrubbed) > max_len:
        scrubbed = scrubbed[:max_len] + "\n[TRUNCATED]"
    return scrubbed


def mask_sensitive_in_text(text: str) -> str:
    """Mask tokens/keys/long IDs in text for reports/logs."""
    if not text:
        return text
    masked = re.sub(r"([A-Za-z0-9_\-]{24,})", "[REDACTED]", text)
    masked = re.sub(r"(?i)(bearer\s+)[A-Za-z0-9_\-\.]+", r"\1[REDACTED]", masked)
    return masked


class SimpleRateLimiter:
    """Very basic in-memory rate limiter keyed by identifier (e.g., IP)."""
    def __init__(self, limit: int, window_seconds: int):
        self.limit = limit
        self.window = window_seconds
        self._store: Dict[str, list] = {}

    def allow(self, key: str) -> bool:
        now = time.time()
        bucket = self._store.setdefault(key, [])
        # drop expired
        cutoff = now - self.window
        self._store[key] = [t for t in bucket if t >= cutoff]
        if len(self._store[key]) >= self.limit:
            return False
        self._store[key].append(now)
        return True


