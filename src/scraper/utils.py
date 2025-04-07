import random
import time
from typing import Optional

from requests.exceptions import RequestException


def exponential_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 10.0,
) -> float:
    """
    Calculate delay for exponential backoff with jitter.

    Args:
        max_retries: Maximum number of retries
        base_delay: Base delay in seconds
        max_delay: Maximum delay in seconds

    Returns:
        Calculated delay in seconds
    """
    delay = min(base_delay * (2 ** max_retries), max_delay)
    jitter = random.uniform(0, delay * 0.1)
    return delay + jitter


def handle_request_exception(
    exception: RequestException,
    retry_count: int,
    max_retries: int = 3,
) -> Optional[float]:
    """
    Handle request exceptions and determine if retry is needed.

    Args:
        exception: The exception that occurred
        retry_count: Current retry count
        max_retries: Maximum number of retries

    Returns:
        Delay in seconds if retry is needed, None otherwise
    """
    if retry_count >= max_retries:
        return None

    if isinstance(exception, (RequestException,)):
        return exponential_backoff(retry_count)

    return None
