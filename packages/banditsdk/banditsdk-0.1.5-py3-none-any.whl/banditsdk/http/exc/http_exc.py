from typing import Any, Dict, Optional


class BaseHTTPException(Exception):
    def __init__(
        self,
        status_code: int,
        detail: Optional[str] = None,
        headers: Optional[dict] = None,
    ) -> None:
        self.status_code = status_code
        self.detail = detail
        self.headers = headers

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, detail={self.detail!r})"


class BaseWebSocketException(Exception):
    def __init__(self, code: int, reason: Optional[str] = None) -> None:
        self.code = code
        self.reason = reason or ""

    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        return f"{cls_name}(code={self.code!r}, reason={self.reason!r})"


class HTTPException(BaseHTTPException):
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class WSException(BaseWebSocketException):
    def __init__(self, code: int, reason: Optional[str] = None) -> None:
        super().__init__(code=code, reason=reason)
