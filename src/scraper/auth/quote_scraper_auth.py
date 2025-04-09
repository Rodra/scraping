import logging

from bs4 import BeautifulSoup
from requests import Session

from scraper.auth.base_scraper_auth import BaseScraperAuth
from scraper.utils import retry_with_backoff

logger = logging.getLogger(__name__)


class QuoteScraperAuth(BaseScraperAuth):
    """Handles authentication for the quotes.toscrape.com website."""

    # In real-world applications, this URL would be configurable by environment
    # variables, configuration files, or cloud secrets.
    PORTAL_URL = "https://quotes.toscrape.com"

    def __init__(self, base_url: str = PORTAL_URL):
        self.base_url = base_url
        self.login_url = f"{self.base_url}/login"
        self.session = Session()

    def login(self, username: str, password: str) -> bool:
        """
        Authenticate with the quotes website.

        Args:
            username: The username to login with.
            password: The password to login with.

        Returns:
            bool: True if login was successful, False otherwise.
        """
        def perform_login(username: str, password: str):
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

            logger.error("Login failed!")
            return False

        return retry_with_backoff(
            perform_login,
            max_retries=3,
            action_name="Login",
            username=username,
            password=password
        )

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
