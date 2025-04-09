import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple

from bs4 import BeautifulSoup

from scraper.auth.base_scraper_auth import BaseScraperAuth
from scraper.utils import retry_with_backoff

logger = logging.getLogger(__name__)


class BaseParser(ABC):
    """Abstract base class for all scrapers."""

    def __init__(self, auth: BaseScraperAuth):
        self.auth = auth

    def fetch_page(self, url: str) -> BeautifulSoup:
        """
        Fetch the content of a page with retry logic.

        Args:
            url: The URL of the page to fetch.

        Returns:
            BeautifulSoup object containing the page content.
        """
        def perform_fetch(url: str):
            # Check if the session is authenticated
            if not self.auth.is_authenticated():
                raise Exception("Session is not authenticated. Please log in first.")

            # Fetch the page content
            response = self.auth.session.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")

        return retry_with_backoff(
            perform_fetch,
            max_retries=3,
            action_name="Fetch Page",
            url=url
        )

    @abstractmethod
    def parse_page(self, page_url: str) -> Tuple[List[Dict[str, Any]], str]:
        """
        Parse all items from a given page.

        Args:
            page_url: URL of the page to parse.

        Returns:
            A tuple containing a list of parsed items and the next page URL.
        """
        pass

    @abstractmethod
    def parse_item(self, item_element: BeautifulSoup) -> Dict[str, Any]:
        """
        Parse a single item element into a structured dictionary.

        Args:
            item_element: BeautifulSoup element containing item data.

        Returns:
            A dictionary containing structured item data.
        """
        pass