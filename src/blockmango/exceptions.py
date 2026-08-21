from __future__ import annotations


class BlockmangoError(Exception):
    def __init__(self, message: str, code: int | None = None, response: dict | None = None):
        super().__init__(message)
        self.code = code
        self.response = response


class AuthError(BlockmangoError):
    """Authentication failed: invalid credentials, expired token, or login required."""


class RateLimitError(BlockmangoError):
    """Rate limited or risk control triggered (codes 567, 100008)."""


class SignError(BlockmangoError):
    """Signature verification failed, typically due to time drift (code 100001)."""


class NotFoundError(BlockmangoError):
    """Requested resource not found (user, clan, group, etc.)."""


class NetworkError(BlockmangoError):
    """Transport-level failure: timeout, connection error, DNS, etc."""


class ValidationError(BlockmangoError):
    """Invalid parameters passed to an API method."""


class SessionError(BlockmangoError):
    """Session persistence or restoration failed."""


class CryptoError(BlockmangoError):
    """Cryptographic operation failed (RSA encrypt, missing pycryptodome)."""