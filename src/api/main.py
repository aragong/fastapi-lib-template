import logging
from api.__version__ import __api_name__, __description__, __version__
from api.config.env import env
from api.core.middelware import LoggingMiddleware
from api.core.telemetry import setup_opentelemetry
from api.core.utils import generate_root_html
from api.routers.test import test_router
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from pathlib import Path

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application lifespan events."""
    # Setup OpenTelemetry FIRST - before any logging
    try:
        setup_opentelemetry()
    except Exception as e:
        print(f"⚠️ OpenTelemetry setup failed: {e}")

    # Startup
    with trace.get_tracer(__name__).start_as_current_span("app_startup"):
        logger.info(f"🚀 Starting {__api_name__} v{__version__}")
        logger.info("🔧 Environment validation...")
        env.validate()
        logger.info("✅ Application startup completed")

    yield

    # Shutdown
    with trace.get_tracer(__name__).start_as_current_span("app_shutdown"):
        logger.info("🔄 Shutting down application...")
        # Add any necessary cleanup tasks here
        logger.info("✅ Application shutdown completed")


app = FastAPI(
    title=__api_name__,
    description=__description__,
    version=__version__,
    contact={
        "name": "| Germán Aragón 👨‍💻 @ IHCantabria 🏢",
        "email": "german.aragon@unican.es",
    },
    license_info={"name": "CC-BY-NC-ND-4.0", "identifier": "CC-BY-NC-ND-4.0"},
    docs_url=None,
    # redoc_url=None,
    lifespan=lifespan,
    root_path=env.API_ROOT_PATH,
)

if not env.EXPORT_TRACES:
    logger.warning("⚠️ Trace export disabled by configuration.")
    logger.info("🔍 Enabling LoggingMiddleware for API request logging.")
    app.add_middleware(LoggingMiddleware)

# Instrument FastAPI app for automatic tracing (must be after app creation)
FastAPIInstrumentor.instrument_app(app)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Add CORS middleware first
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=Path("src/api/static").resolve()), name="static")


@app.get("/docs", include_in_schema=False)
async def swagger_ui_html() -> HTMLResponse:
    """Swagger UI for API documentation."""

    return get_swagger_ui_html(
        openapi_url=f"{env.API_ROOT_PATH}/openapi.json",
        title=app.title,
        swagger_favicon_url=(f"{env.API_ROOT_PATH}/static/favicon.ico"),
    )


@app.get("/")
async def root() -> HTMLResponse:
    """Root endpoint API homepage with general information."""

    html_content = generate_root_html(
        api_name=__api_name__,
        description=__description__,
        version=__version__,
    )
    return HTMLResponse(content=html_content)


# Include routers
app.include_router(test_router)  # Test router first


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api.main:app", reload=True)
