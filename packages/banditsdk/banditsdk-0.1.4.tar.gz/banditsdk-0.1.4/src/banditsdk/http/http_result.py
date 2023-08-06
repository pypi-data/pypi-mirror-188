from enum import Enum
from typing import TypeVar, Generic, Optional
from pydantic import BaseModel

from .exc.http_exc import HTTPException


class ActionStatus(str, Enum):
    success = "success"
    failure = "failure"


T = TypeVar("T")


class HttpResult(BaseModel, Generic[T]):
    """
    Factory either http-result or ws-result class.
    Has status, data, error fields.
    Used for general definition of function`s result.
    You also can import http_status (int, enum) from common.http.status
    and use it status.404_NOT_FOUND.value.
    Example:
    def send_data_to_remote(data, url):
    	response = post(url, data=data)
    	try:
	    if response.status == 200:
	        return Result.success(data=response.json)
	    else:
	        return Result.failure(exc=HTTPException(status=400, detail="Bad request.")
	except Exception as error:
	    return Result.server_error(exc=HTTPException(status=500, detail="Internal server error.")
    """
    status: ActionStatus
    data: Optional[T]
    exc: Exception
    detail: Optional[str]

    class Config:
        use_enum_values = True

    def is_success(self):
        return self.status == ActionStatus.success

    def is_failure(self):
        return not self.is_success()

    @classmethod
    def success(cls, data: Optional[T] = None, detail: Optional[str] = None):
        return HttpResult(status=ActionStatus.success, data=data, detail=detail)

    @classmethod
    def failure(cls, exc: Exception):
        return HttpResult(status=ActionStatus.failure, exc=exc)

    @classmethod
    def server_error(
        cls,
        exc: Exception = HTTPException(status_code=500, detail="Internal server error")
    ):
        return HttpResult(status=ActionStatus.failure, exc=exc)
