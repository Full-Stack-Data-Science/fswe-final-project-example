from time import time

from fastapi import Request, Response
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        start_time = time()

        # Log request info
        body = await request.body()
        logger.info(
            "Incoming request",
            extra={
                "method": request.method,
                "url": str(request.url),
                "headers": dict(request.headers),
                "body": body.decode("utf-8") if body else None,
            },
        )

        response = await call_next(request)

        # Add processing time
        process_time = time() - start_time
        logger.info(
            f"Completed in {process_time:.3f}s with status {response.status_code}",
        )
        return response
