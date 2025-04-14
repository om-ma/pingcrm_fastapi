from typing import Any, Dict, Optional

class AppException(Exception):
    """Base exception for application."""
    def __init__(
        self,
        status_code: int,
        detail: str,
        code: Optional[str] = None,
        meta: Optional[Dict[str, Any]] = None
    ) -> None:
        self.status_code = status_code
        self.detail = detail
        self.code = code
        self.meta = meta or {}

class NotFoundException(AppException):
    """Resource not found exception."""
    def __init__(
        self,
        detail: str = "Resource not found",
        code: Optional[str] = None,
        meta: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(404, detail, code, meta)

class ValidationException(AppException):
    """Validation error exception."""
    def __init__(
        self,
        detail: str = "Validation error",
        code: Optional[str] = None,
        meta: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(400, detail, code, meta)

class UnauthorizedException(AppException):
    """Unauthorized exception."""
    def __init__(
        self,
        detail: str = "Unauthorized",
        code: Optional[str] = None,
        meta: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(401, detail, code, meta)

class ForbiddenException(AppException):
    """Forbidden exception."""
    def __init__(
        self,
        detail: str = "Forbidden",
        code: Optional[str] = None,
        meta: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(403, detail, code, meta)
