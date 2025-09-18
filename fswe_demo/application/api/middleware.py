from collections.abc import Awaitable, Callable
from time import time

from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import Message


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        start_time = time()

        # ---- Read/prepare body safely ----
        if request.method in {"GET", "DELETE"}:
            logged_body = None
            logged_query = dict(request.query_params)
            req_for_downstream = request
        else:
            raw_body = await request.body()

            # Re-inject the body so downstream handlers can still read it
            async def receive() -> Message:
                return {"type": "http.request", "body": raw_body, "more_body": False}

            req_for_downstream = Request(request.scope, receive)

            try:
                logged_body = raw_body.decode("utf-8") if raw_body else None
            except UnicodeDecodeError:
                logged_body = "<binary body>"
            logged_query = dict(request.query_params)

        # ---- Log request ----
        logger.info(
            f"Incoming request | method={request.method} "
            f"url={request.url} "
            f"query={logged_query} "
            f"body={logged_body}",
        )

        # ---- Call endpoint ----
        response = await call_next(req_for_downstream)

        # ---- Log completion ----
        process_time = time() - start_time
        logger.info(
            f"Completed in {process_time:.3f}s with status {response.status_code}",
        )

        return response
