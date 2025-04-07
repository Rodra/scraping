import logging
import time
from typing import Optional

from bs4 import BeautifulSoup
from requests import Session

from scraper.utils import handle_request_exception

logger = logging.getLogger(__name__)


class QuoteScraperAuth:
    """Handles authentication for the quotes.toscrape.com website."""

    def __init__(self, base_url: str = "https://quotes.toscrape.com"):
        self.base_url = base_url
        self.login_url = f"{self.base_url}/login"
        self.session = Session()

    def login(self, username: str, password: str) -> bool:
        """
        Authenticate with the quotes website.

        Args:
            username: The username to login with
            password: The password to login with

        Returns:
            bool: True if login was successful, False otherwise
        """
        retry_count = 0
        max_retries = 3

        while retry_count <= max_retries:
            try:
                # Fetch the login page to get the CSRF token
                response = self.session.get(self.login_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                csrf_token = soup.find("input", {"name": "csrf_token"})["value"]

                # Prepare the login payload
                payload = {
                    "csrf_token": csrf_token,
                    "username": username,
                    "password": password,
                }

                # Submit the login form
                login_response = self.session.post(self.login_url, data=payload)
                login_response.raise_for_status()

                # Check if login was successful
                if "Logout" in login_response.text:
                    logger.info("Login successful!")
                    return True
                else:
                    logger.error("Login failed!")
                    return False
            except Exception as e:
                # Handle the exception and determine if a retry is needed
                delay = handle_request_exception(e, retry_count, max_retries)
                if delay is None:
                    logger.error(f"Failed to log in after {max_retries} retries.")
                    return False

                retry_count += 1
                time.sleep(delay)

    def is_authenticated(self) -> bool:
        """
        Check if the current session is authenticated.

        Returns:
            bool: True if authenticated, False otherwise
        """
        try:
            response = self.session.get(self.base_url)
            response.raise_for_status()
            return "Logout" in response.text
        except Exception as e:
            logger.error(f"Error checking authentication: {e}")
            return False
