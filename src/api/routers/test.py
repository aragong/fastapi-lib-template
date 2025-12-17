"""Test router with OpenTelemetry tracing and logging."""

import asyncio
import httpx
import logging
import time
from fastapi import APIRouter, HTTPException, status
from opentelemetry import trace
from src.api.config.env import env

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)
test_router = APIRouter(tags=["Test"], prefix=env.API_PREFIX + "/test")


@test_router.get("/healthcheck")
async def basic_test() -> dict:
    """Test endpoint to verify service is running."""
    logger.info("🔍 Basic test endpoint called")
    return {"status": "ok", "message": "Service is running"}


@test_router.get("/error")
async def error_test() -> float:
    """Test error handling and logging with a critical error (division by zero)."""
    try:
        return 100 / 0
    except Exception as e:
        logger.critical("💀 Testing error handling", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error. {e}"
        ) from e


@test_router.get("/logs-test")
async def logs_test() -> dict:
    """Test different log levels for Seq visualization."""
    logger.debug("🐛 Debug message - detailed debugging info")
    logger.info("ℹ️ Info message - general information")
    logger.warning("⚠️ Warning message - something might be wrong")

    # Simulamos alguna lógica de negocio
    logger.info("📊 Processing test data...")
    time.sleep(0.1)  # Simular trabajo
    logger.info("✅ Test data processed successfully")

    return {
        "status": "ok",
        "message": "Log test completed - check Seq for trace correlation",
        "logs_sent": ["debug", "info", "warning"],
    }


@test_router.get("/external-api-test")
async def external_api_test() -> dict:
    """Test external API calls with tracing."""
    logger.info("🌐 Testing external API calls")

    try:
        # Hacer una llamada HTTP externa que será instrumentada automáticamente
        async with httpx.AsyncClient() as client:
            response = await client.get("https://httpbin.org/json", timeout=5)

        logger.info(f"🎉 External API response received: {response.status_code}")
        return {"status": "ok", "message": "External API call successful", "external_status": response.status_code}
    except Exception as e:
        logger.exception("❌ External API call failed")
        raise HTTPException(status_code=503, detail="External API unavailable") from e


@test_router.get("/nested-operations")
async def nested_operations() -> dict:
    """Test nested operations with detailed tracing."""
    logger.info("🔄 Starting nested operations test")

    # Operación 1
    logger.info("📝 Step 1: Data validation")
    await _validate_data()

    # Operación 2
    logger.info("⚙️ Step 2: Processing data")
    result = await _process_data()

    # Operación 3
    logger.info("💾 Step 3: Saving results")
    await _save_results(result)

    logger.info("🎯 Nested operations completed successfully")
    return {"status": "ok", "message": "Nested operations completed", "result": result}


async def _validate_data() -> None:
    """Simulate data validation."""
    logger.debug("🔍 Validating input data...")
    time.sleep(0.05)
    logger.debug("✅ Data validation passed")


async def _process_data() -> dict:
    """Simulate data processing."""
    logger.debug("⚡ Processing business logic...")
    time.sleep(0.1)
    result = {"processed": True, "items": 42}
    logger.debug(f"📊 Processing result: {result}")
    return result


async def _save_results(result: dict) -> None:
    """Simulate saving results."""
    logger.debug(f"💾 Saving result: {result}")
    time.sleep(0.03)
    logger.debug("✅ Results saved successfully")


@test_router.get("/telemetry-debug")
async def telemetry_debug():
    """Debug endpoint to verify telemetry export and Seq connectivity."""
    with tracer.start_as_current_span("telemetry_debug") as span:
        span.set_attribute("debug_type", "telemetry_verification")
        span.set_attribute("timestamp", time.time())

        # Add multiple events
        span.add_event("debug_start", {"message": "Starting telemetry debug"})

        # Force immediate export by creating and ending multiple spans
        for i in range(3):
            with tracer.start_as_current_span(f"debug_span_{i}") as debug_span:
                debug_span.set_attribute("span_index", i)
                debug_span.add_event(f"debug_event_{i}", {"index": i, "message": f"Debug event {i}"})
                await asyncio.sleep(0.01)

        span.add_event("debug_end", {"message": "Telemetry debug completed"})

        logger.info(f"🔍 Telemetry debug completed - Trace ID: {format(span.get_span_context().trace_id, '032x')}")

        return {
            "message": "Telemetry debug completed",
            "trace_id": format(span.get_span_context().trace_id, "032x"),
            "spans_created": 4,  # 1 main + 3 debug spans
            "check_seq": "Should appear in Seq within 1-2 seconds",
        }
