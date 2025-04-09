import logging
from abc import ABC, abstractmethod

from requests import Session

logger = logging.getLogger(__name__)


class BaseScraperAuth(ABC):
    """Abstract base class for scraper authentication."""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = Session()

    @abstractmethod
    def login(self, username: str, password: str) -> bool:
        """
        Authenticate with the target website.

        Args:
            username: The username to login with.
            password: The password to login with.

        Returns:
            bool: True if login was successful, False otherwise.
        """
        pass

    @abstractmethod
    def is_authenticated(self) -> bool:
        """
        Check if the current session is authenticated.

        Returns:
            bool: True if authenticated, False otherwise.
        """
        pass
