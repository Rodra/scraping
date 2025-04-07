import logging
from typing import List, Tuple

from scraper.auth import QuoteScraperAuth
from scraper.parser import QuoteParser

logger = logging.getLogger(__name__)


class QuoteScraperJob:
    """Handles the scraping of quotes."""

    def __init__(self, username: str, password: str):
        self.auth = QuoteScraperAuth()
        self.parser = QuoteParser(self.auth)
        self.username = username
        self.password = password

    def _attempt_login(self) -> bool:
        """
        Attempt to log in to the website.

        Returns:
            bool: True if login was successful, False otherwise.
        """
        try:
            if not self.auth.login(self.username, self.password):
                logger.error("Login failed. Cannot proceed with scraping.")
                return False
            logger.info("Login successful.")
            return True
        except Exception as e:
            logger.error(f"An error occurred during login: {e}")
            return False

    def _scrape_page(self, page_url: str) -> Tuple[List[dict], str]:
        """
        Scrape a single page and return the quotes and the next page URL.

        Args:
            page_url (str): The URL of the page to scrape.

        Returns:
            Tuple[List[dict], str]: A tuple containing the list of quotes and the next page URL.
        """
        try:
            logger.info(f"Scraping page: {page_url}")
            quotes, next_page_url = self.parser.parse_page(page_url)
            logger.info(f"Scraped {len(quotes)} quotes from {page_url}")
            return quotes, next_page_url
        except Exception as e:
            logger.error(f"Error scraping page {page_url}: {e}")
            return [], None

    def _scrape_all_pages(self) -> List[dict]:
        """
        Scrape all pages starting from the first page.

        Returns:
            List[dict]: A list of all quotes scraped from the website.
        """
        current_page_url = f"{self.auth.base_url}/page/1/"
        all_quotes = []

        while current_page_url:
            quotes, current_page_url = self._scrape_page(current_page_url)
            all_quotes.extend(quotes)

        return all_quotes

    def scrape(self) -> List[dict]:
        """
        Main method to scrape all quotes from the website.
        """
        if not self._attempt_login():
            return []

        logger.info("Starting the scraping process...")
        all_quotes = self._scrape_all_pages()
        logger.info(f"Scraping completed. Total quotes scraped: {len(all_quotes)}")
        return all_quotes
