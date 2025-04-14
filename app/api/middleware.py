from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions import AppException
from app.schemas.jsonapi import JsonApiError, JsonApiErrorResponse

async def error_handler(request: Request, call_next):
    try:
        return await call_next(request)
    except AppException as exc:
        error = JsonApiError(
            status=str(exc.status_code),
            code=exc.code,
            title=exc.detail,
            meta=exc.meta
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=JsonApiErrorResponse(errors=[error]).dict(exclude_none=True)
        )
    except Exception as exc:
        error = JsonApiError(
            status="500",
            title=str(exc),
        )
        return JSONResponse(
            status_code=500,
            content=JsonApiErrorResponse(errors=[error]).dict(exclude_none=True)
        )
