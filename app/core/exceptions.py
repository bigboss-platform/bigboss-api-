from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.shared.exceptions import BigBossException


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(BigBossException)
    async def bigboss_exception_handler(
        request: Request, exc: BigBossException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "type": f"https://bigboss.io/errors/{exc.error_type}",
                "title": exc.title,
                "status": exc.status_code,
                "detail": exc.detail,
                "instance": str(request.url.path),
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={
                "type": "https://bigboss.io/errors/internal-error",
                "title": "Internal Server Error",
                "status": 500,
                "detail": "An unexpected error occurred.",
                "instance": str(request.url.path),
            },
        )
