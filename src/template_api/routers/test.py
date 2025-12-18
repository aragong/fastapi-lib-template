"""Test router with OpenTelemetry tracing and logging."""

import httpx
import logging
from fastapi import APIRouter, HTTPException, status
from opentelemetry import trace
from template_api.config.env import env
from template_lib.services.processing import fake_processing_task

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)
test_router = APIRouter(tags=["test"], prefix=env.API_PREFIX + "/test")


@test_router.get("/healthcheck")
async def healthcheck() -> dict:
    """Service health check.

    Simple endpoint to verify the service is running and responsive.
    """
    logger.info("🔍 Health check called")
    return {"status": "ok", "service": "template-api"}


@test_router.get("/error")
async def error_example() -> float:
    """Error handling demonstration.

    Intentionally triggers an error to demonstrate exception handling,
    logging with traceback, and error response format.
    """
    try:
        result = 100 / 0
        return result
    except ZeroDivisionError as e:
        logger.exception("💀 Demonstrating error handling with traceback")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Intentional error for testing: {type(e).__name__}: {e!s}",
        ) from e


@test_router.get("/external-call")
async def external_call_example() -> dict:
    """External HTTP call with automatic tracing.

    Demonstrates how OpenTelemetry automatically instruments external HTTP calls
    and propagates trace context across service boundaries.
    """
    logger.info("🌐 Making external HTTP call")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://httpbin.org/json", timeout=5)

        logger.info(f"✅ External call successful: {response.status_code}")
        return {"status": "ok", "message": "External API call successful", "external_status": response.status_code}
    except Exception as e:
        logger.exception("❌ External API call failed")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"External API call failed: {e!s}"
        ) from e


@test_router.get("/processing")
async def processing_example() -> dict:
    """Nested operations with library function call.

    Demonstrates:
    - Nested trace spans for multi-step operations
    - Calling functions from template_lib package
    - Logging at different stages of processing
    """
    logger.info("🔄 Starting processing workflow")

    with tracer.start_as_current_span("data_validation"):
        logger.debug("🔍 Validating input data")
        # Simulate validation

    with tracer.start_as_current_span("data_processing"):
        logger.info("⚙️ Processing data with library function")
        # Call library function
        result = fake_processing_task("sample data")
        logger.debug(f"📊 Processing complete: {result}")

    with tracer.start_as_current_span("save_results"):
        logger.debug("💾 Saving results")
        # Simulate save operation

    logger.info("✅ Processing workflow completed successfully")
    return {"status": "ok", "message": "Processing completed", "result": result}
