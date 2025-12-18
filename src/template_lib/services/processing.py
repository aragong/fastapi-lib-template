import logging
import time

logger = logging.getLogger(__name__)


def fake_processing_task(data: str) -> str:
    """Fake processing task that simulates some work being done."""
    logger.debug("🔄 Starting fake processing task")
    time.sleep(2)  # Simulate a time-consuming task
    logger.debug("✅ Fake processing task completed")
    return data.upper()
