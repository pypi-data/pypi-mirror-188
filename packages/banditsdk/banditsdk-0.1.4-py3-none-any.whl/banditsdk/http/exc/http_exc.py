import http
from typing import Any, Dict, Optional, Sequence, Type

from pydantic import BaseModel, ValidationError, create_model
from pydantic.error_wrappers import ErrorList


class BaseHTTPException(Exception):
    def __init__(
        self,
        status_code: int,
        detail: Optional[str] = None,
        headers: Optional[dict] = None,
    ) -> None:
        if detail is None:
            detail = http.HTTPStatus(status_code).phrase
        self.status_code = status_code
        self.detail = detail
        self.headers = headers

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, detail={self.detail!r})"


class WebSocketException(Exception):
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


RequestErrorModel: Type[BaseModel] = create_model("Request")
WebSocketErrorModel: Type[BaseModel] = create_model("WebSocket")


class RequestValidationError(ValidationError):
    def __init__(self, errors: Sequence[ErrorList], *, body: Any = None) -> None:
        self.body = body
        super().__init__(errors, RequestErrorModel)


class WebSocketRequestValidationError(ValidationError):
    def __init__(self, errors: Sequence[ErrorList]) -> None:
        super().__init__(errors, WebSocketErrorModel)

