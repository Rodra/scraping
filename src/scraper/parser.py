import logging
import time
from typing import Any, Dict, List

from bs4 import BeautifulSoup
from requests.exceptions import RequestException

from .auth import QuoteScraperAuth
from .utils import handle_request_exception

logger = logging.getLogger(__name__)


class QuoteParser:
    """Handles parsing of quote data from the website."""

    def __init__(self, auth: QuoteScraperAuth):
        self.auth = auth

    def fetch_page(self, url: str) -> BeautifulSoup:
        """
        Fetch the content of a page with retry logic.

        Args:
            url: The URL of the page to fetch.

        Returns:
            BeautifulSoup object containing the page content.
        """
        retry_count = 0
        max_retries = 3

        while retry_count <= max_retries:
            try:
                # Check if the session is authenticated
                if not self.auth.is_authenticated():
                    raise Exception("Session is not authenticated. Please log in first.")

                # Fetch the page content
                response = self.auth.session.get(url)
                response.raise_for_status()
                return BeautifulSoup(response.text, "html.parser")

            except RequestException as e:
                # Handle the exception and determine if a retry is needed
                delay = handle_request_exception(e, retry_count, max_retries)
                if delay is None:
                    raise Exception(f"Failed to fetch page {url} after {max_retries} retries.") from e

                retry_count += 1
                time.sleep(delay)

    def parse_quote(self, quote_element: BeautifulSoup) -> Dict[str, Any]:
        """
        Parse a single quote element into a structured dictionary.

        Args:
            quote_element: BeautifulSoup element containing quote data

        Returns:
            Dict containing structured quote data
        """
        try:
            text = quote_element.find("span", class_="text")
            author = quote_element.find("small", class_="author")

            # In real-world applications, we would want to implement a more robust data check.
            if not text or not author:
                return {}

            tags = [tag.get_text() for tag in quote_element.find_all("a", class_="tag")]

            # Extract goodreads.com reference if available
            goodreads_link = None
            author_link = quote_element.find("a", href=True)
            if author_link and "goodreads.com" in author_link["href"]:
                goodreads_link = author_link["href"]

            return {
                "text": text.get_text(),
                "author": author.get_text(),
                "tags": tags,
                "goodreads_link": goodreads_link,
            }
        except Exception as e:
            # In real-world applications, we would want to have better error
            # handling when the structure of the target website changes
            logger.error(f"Error parsing quote element: {e}")
            return {}

    def parse_page(self, page_url: str) -> List[Dict[str, Any]]:
        """
        Parse all quotes from a given page.

        Args:
            page_url: URL of the page to parse

        Returns:
            List of parsed quote dictionaries
        """
        try:
            # Fetch the page content using the helper method
            soup = self.fetch_page(page_url)

            # Find all quote elements
            quote_elements = soup.find_all("div", class_="quote")
            quotes = [
                self.parse_quote(quote_element) for quote_element in quote_elements
            ]

            # Filter out empty dictionaries (invalid quotes)
            return [quote for quote in quotes if quote]
        except Exception as e:
            # Log the error and return an empty list
            logger.error(f"Error parsing page {page_url}: {e}")
            return []

    def get_next_page_url(self, current_page_url: str) -> str:
        """
        Get the URL of the next page if it exists.

        Args:
            current_page_url: URL of the current page

        Returns:
            URL of the next page or empty string if no next page
        """
        try:
            # Fetch the page content using the helper method
            soup = self.fetch_page(current_page_url)

            # Find the "Next" button and extract its URL
            next_page_link = soup.find("li", class_="next")
            if next_page_link:
                next_page_url = next_page_link.find("a")["href"]
                return f"{self.auth.base_url}{next_page_url}"
            return None
        except Exception as e:
            # Log the error and return an empty string
            logger.error(f"Error getting next page URL from {current_page_url}: {e}")
            return ""
