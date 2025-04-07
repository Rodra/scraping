import logging
from typing import List

from scraper.auth import QuoteScraperAuth
from scraper.parser import QuoteParser

# Configure logging to output to the console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


class QuoteScraperJob:
    """Handles the scraping of quotes."""

    def __init__(self, username: str, password: str):
        self.auth = QuoteScraperAuth()
        self.parser = QuoteParser(self.auth)
        self.username = username
        self.password = password

    def scrape(self):
        """
        Scrape all quotes from the website.
        """
        if not self.auth.login(self.username, self.password):
            logger.error("Login failed. Cannot proceed with scraping.")
            return

        logger.info("Starting the scraping process...")
        current_page_url = f"{self.auth.base_url}/page/1/"
        all_quotes = []

        while current_page_url:
            logger.info(f"Scraping page: {current_page_url}")
            try:
                # Parse quotes from the current page
                quotes = self.parser.parse_page(current_page_url)
                all_quotes.extend(quotes)

                # Get the next page URL
                current_page_url = self.parser.get_next_page_url(current_page_url)
            except Exception as e:
                logger.error(f"Error scraping page {current_page_url}: {e}")
                break

        logger.info(f"Scraping completed. Total quotes scraped: {len(all_quotes)}")

        # Save the quotes to the database
        self.save_to_database(all_quotes)

    def save_to_database(self, quotes: List[dict]):
        """
        Save the scraped quotes to the database.

        Args:
            quotes: List of dictionaries containing quote data.
        """
        for quote_data in quotes:
            try:
                # TODO: Save the quote_data to the database
                logger.info(f"Saving quote: {quote_data['text']} by {quote_data['author']}")

            except Exception as e:
                logger.error(f"Error saving quote: {quote_data}. Error: {e}")