import logging
from typing import Any, Dict, List, Tuple

from bs4 import BeautifulSoup

from scraper.auth.quote_scraper_auth import QuoteScraperAuth
from scraper.parsers.base_parser import BaseParser
from scraper.utils import retry_with_backoff

logger = logging.getLogger(__name__)


class QuoteParser(BaseParser):
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

    def get_quote_text(self, quote_element: BeautifulSoup) -> str:
        """
        Extract the text of the quote.

        Args:
            quote_element: BeautifulSoup element containing quote data.

        Returns:
            The text of the quote.
        """
        text_element = quote_element.find("span", class_="text")
        return text_element.get_text(strip=True) if text_element else ""

    def get_quote_author(self, quote_element: BeautifulSoup) -> str:
        """
        Extract the author of the quote.

        Args:
            quote_element: BeautifulSoup element containing quote data.

        Returns:
            The author of the quote.
        """
        author_element = quote_element.find("small", class_="author")
        return author_element.get_text(strip=True) if author_element else ""

    def get_author_url(self, quote_element: BeautifulSoup) -> str:
        """
        Extract the URL of the author.

        Args:
            quote_element: BeautifulSoup element containing quote data.

        Returns:
            The URL of the author.
        """
        author_link = quote_element.find("small", class_="author").find_next("a")
        return f"{self.auth.base_url}{author_link['href']}" if author_link else ""

    def get_quote_tags(self, quote_element: BeautifulSoup) -> List[Dict[str, str]]:
        """
        Extract the tags associated with the quote.

        Args:
            quote_element: BeautifulSoup element containing quote data.

        Returns:
            A list of dictionaries, each containing the tag name and its URL.
        """
        tag_elements = quote_element.find_all("a", class_="tag")
        return [
            {
                "name": tag.get_text(strip=True),
                "url": f"{self.auth.base_url}{tag['href']}"
            }
            for tag in tag_elements
        ]

    def get_goodreads_link(self, quote_element: BeautifulSoup) -> str:
        """
        Extract the Goodreads link for the author, if available.

        Args:
            quote_element: BeautifulSoup element containing quote data.

        Returns:
            The Goodreads link for the author.
        """
        author_link = quote_element.find("a", href=True)
        if not author_link or "goodreads.com" not in author_link["href"]:
            return None

        return author_link["href"]

    def parse_item(self, quote_element: BeautifulSoup) -> Dict[str, Any]:
        """
        Parse a single quote element into a structured dictionary.

        Args:
            quote_element: BeautifulSoup element containing quote data

        Returns:
            Dict containing structured quote data
        """
        try:
            text = self.get_quote_text(quote_element)
            author = self.get_quote_author(quote_element)
            tags = self.get_quote_tags(quote_element)
            author_url = self.get_author_url(quote_element)
            goodreads_link = self.get_goodreads_link(quote_element)

            # Ensure required fields are present
            if not text or not author or not author_url:
                raise ValueError("Missing required fields in quote element")

            return {
                "text": text,
                "author": author,
                "author_url": author_url,
                "tags": tags,
                "goodreads_link": goodreads_link,
            }
        except Exception as e:
            # In a real-world application, we would want to have better error
            # handling when the structure of the target website changes
            logger.error(f"Error parsing quote element: {e}")
            return {}

    def parse_page(self, page_url: str) -> Tuple[List[Dict[str, Any]], str]:
        """
        Parse all quotes from a given page.

        Args:
            page_url: URL of the page to parse

        Returns:
            List of parsed quote dictionaries and the next page to parse
        """
        try:
            # Fetch the page content using the helper method
            soup = self.fetch_page(page_url)

            # Find all quote elements
            quote_elements = soup.find_all("div", class_="quote")
            quotes = [
                self.parse_item(quote_element) for quote_element in quote_elements
            ]

            # Filter out empty dictionaries (invalid quotes)
            valid_quotes = [quote for quote in quotes if quote]

            # Find the "Next" button and extract its URL
            next_page_link = soup.find("li", class_="next")
            next_page_url = (
                f"{self.auth.base_url}{next_page_link.find('a')['href']}"
                if next_page_link
                else None
            )

            # Return the parsed quotes and the next page URL
            return valid_quotes, next_page_url
        except Exception as e:
            # Log the error and return an empty list
            logger.error(f"Error parsing page {page_url}: {e}")
            return [], None
