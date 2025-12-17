# Middleware for logging API requests only when EXPORT_TRACES in disabled

import logging
import time
from src.api.config.env import env
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware para logging de API requests cuando EXPORT_TRACES está deshabilitado."""

    async def dispatch(self, request: Request, call_next) -> Response:
        # Captura información de la request
        start_time = time.time()
        method = request.method
        url = request.url.path

        logger.debug(f"➡️ Incoming request: {method} {url}") if _check_excluded_endpoint(
            request.url.path
        ) else logger.info(f"➡️ Incoming request: {method} {url}")

        # Ejecuta el endpoint
        response = await call_next(request)

        # Calcula duración
        duration = time.time() - start_time

        # Log con información relevante
        logger.debug(
            f"⬅️ Completed request: {method} {url} | Status: {response.status_code} | Duration: {duration:.3f}s"
        ) if _check_excluded_endpoint(request.url.path) else logger.info(
            f"⬅️ Completed request: {method} {url} | Status: {response.status_code} | Duration: {duration:.3f}s"
        )

        return response


def _check_excluded_endpoint(endpoint: str) -> bool:
    return any(var for var in env.OTEL_PYTHON_EXCLUDED_URLS if endpoint.replace(env.API_PREFIX, "") == var)
