import logging
import random
import time
from typing import Optional

from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

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
    delay = min(base_delay * (2**max_retries), max_delay)
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

def retry_with_backoff(action, max_retries: int, action_name: str, *args, **kwargs):
    """
    Retry an action with exponential backoff.

    Args:
        action: The function to execute with retries.
        max_retries: Maximum number of retries.
        action_name: Name of the action for logging purposes.
        *args: Positional arguments to pass to the action.
        **kwargs: Keyword arguments to pass to the action.

    Returns:
        The result of the action if successful.

    Raises:
        Exception: If the action fails after the maximum number of retries.
    """
    retry_count = 0

    while retry_count <= max_retries:
        try:
            # Attempt to execute the action
            return action(*args, **kwargs)
        except Exception as e:
            logger.error(f"{action_name} attempt {retry_count + 1} failed: {e}")
            delay = handle_request_exception(e, retry_count, max_retries)
            if delay is None:
                logger.error(f"Failed to complete {action_name} after {max_retries} retries.")
                raise Exception(
                    f"Failed to complete {action_name} after {max_retries} retries."
                ) from e

            retry_count += 1
            logger.info(f"Retrying {action_name} in {delay} seconds (attempt {retry_count + 1})...")
            time.sleep(delay)
