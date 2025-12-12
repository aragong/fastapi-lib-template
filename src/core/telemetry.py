"""OpenTelemetry simplified setup for TESEO API."""

from __future__ import annotations

import logging
import os
from opentelemetry import _logs, trace
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from src.__version__ import __api_name__, __version__
from src.config.env import env
from uuid import uuid4

logger = logging.getLogger(__name__)


def setup_opentelemetry() -> None:
    """Set up OpenTelemetry programmatically - simplified version following official patterns."""
    try:
        # Get configuration from environment
        base_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
        if not base_endpoint:
            logger.warning("⚠️ No OTLP endpoint configured. Skipping OpenTelemetry setup.")
            return

        # Create resource
        resource = Resource.create(
            {
                "service.environment": env.APP_ENVIRONMENT,
                "service.name": __api_name__,  # No needed while OTEL_SERVICE_NAME is set as environment variable
                "service.version": __version__,
                "service.instance-uuid": str(uuid4()),
            }
        )

        # # --- TRACES SETUP (following official pattern) ---
        traces_setup(base_endpoint, resource) if env.EXPORT_TRACES else None

        # --- INSTRUMENTATIONS (automatic, like official examples) ---
        # NOTE: FastAPI instrumentation will be done after app creation in main.py
        instrumentations_setup()

        # --- LOGS SETUP (simplified) ---
        logs_setup(base_endpoint, resource)
        thirdparty_loglevels_setup()

        logger.info("🎉 OpenTelemetry setup completed!")
        logger.debug("🆔 Service name: %s", resource.attributes["service.name"])
        logger.debug("🏷️ Service version: %s", resource.attributes["service.version"])
        logger.debug("🆕 Service instance-UUID: %s", resource.attributes["service.instance-uuid"])
        logger.debug("🔗 OTLP base endpoint: %s", base_endpoint)
        logger.debug("Automated instrumentation (spans and traces) for FastAPI and other libraries set up.")

    except Exception:
        logger.exception("❌ OpenTelemetry setup failed")
        # Continue running without OpenTelemetry rather than crashing


def instrumentations_setup() -> None:
    """Set up other library instrumentors."""

    LoggingInstrumentor().instrument()
    logger.debug("📝 Logs should be exported to OTLP with trace correlation")

    HTTPXClientInstrumentor().instrument()
    RequestsInstrumentor().instrument()
    logger.debug("📡 HTTP traces will be automatically captured (httpx and requests)")


def traces_setup(base_endpoint: str, resource: Resource) -> None:
    """Set up trace instrumentation."""
    # FastAPI instrumentation will be done after app creation in main.py
    traces_endpoint = f"{base_endpoint.rstrip('/')}/traces"

    # Set up tracer provider (like the official example)
    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=traces_endpoint)))
    trace.set_tracer_provider(tracer_provider)


def logs_setup(base_endpoint: str, resource: Resource) -> None:
    """Set up log instrumentation."""
    logs_endpoint = f"{base_endpoint.rstrip('/')}/logs"

    # Set up logger provider (like the official example)
    logger_provider = LoggerProvider(resource=resource)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(OTLPLogExporter(endpoint=logs_endpoint)))
    _logs.set_logger_provider(logger_provider)

    # Configure logs without FastAPI automatic trace to be sent to OTLP aswell
    handler = LoggingHandler(logger_provider=logger_provider)
    logging.getLogger().addHandler(handler)


def thirdparty_loglevels_setup() -> None:
    """Set up third-party library instrumentors."""
    logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    logging.getLogger("botocore").setLevel(logging.WARNING)
    logging.getLogger("numba").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.INFO)
