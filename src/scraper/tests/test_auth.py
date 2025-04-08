import unittest
from unittest.mock import MagicMock, patch

from requests.exceptions import RequestException

from scraper.auth.authentication import QuoteScraperAuth


class TestQuoteScraperAuth(unittest.TestCase):
    def setUp(self):
        self.auth = QuoteScraperAuth()
        self.username = "test_user"
        self.password = "test_password"

    @patch("scraper.auth.authentication.Session.get")
    @patch("scraper.auth.authentication.Session.post")
    def test_login_successful(self, mock_post, mock_get):
        # Mock the GET request to fetch the login page
        mock_get.return_value = MagicMock(
            status_code=200,
            text='<input name="csrf_token" value="test_csrf_token">'
        )

        # Mock the POST request to submit the login form
        mock_post.return_value = MagicMock(
            status_code=200,
            text="Logout"  # Simulate a successful login
        )

        result = self.auth.login(self.username, self.password)

        # Assertions
        self.assertTrue(result)
        mock_get.assert_called_once_with(self.auth.login_url)
        mock_post.assert_called_once_with(
            self.auth.login_url,
            data={
                "csrf_token": "test_csrf_token",
                "username": self.username,
                "password": self.password,
            },
        )

    @patch("scraper.auth.authentication.Session.get")
    @patch("scraper.auth.authentication.Session.post")
    def test_login_failed(self, mock_post, mock_get):
        # Mock the GET request to fetch the login page
        mock_get.return_value = MagicMock(
            status_code=200,
            text='<input name="csrf_token" value="test_csrf_token">'
        )

        # Mock the POST request to submit the login form
        mock_post.return_value = MagicMock(
            status_code=200,
            text="Login"  # Simulate a failed login
        )

        result = self.auth.login(self.username, self.password)

        # Assertions
        self.assertFalse(result)
        mock_get.assert_called_once_with(self.auth.login_url)
        mock_post.assert_called_once_with(
            self.auth.login_url,
            data={
                "csrf_token": "test_csrf_token",
                "username": self.username,
                "password": self.password,
            },
        )

    @patch("scraper.auth.authentication.Session.get")
    def test_is_authenticated_true(self, mock_get):
        # Mock the GET request to check authentication
        mock_get.return_value = MagicMock(
            status_code=200,
            text="Logout"  # Simulate an authenticated session
        )

        result = self.auth.is_authenticated()

        # Assertions
        self.assertTrue(result)
        mock_get.assert_called_once_with(self.auth.base_url)

    @patch("scraper.auth.authentication.Session.get")
    def test_is_authenticated_false(self, mock_get):
        # Mock the GET request to check authentication
        mock_get.return_value = MagicMock(
            status_code=200,
            text="Login"  # Simulate an unauthenticated session
        )

        result = self.auth.is_authenticated()

        # Assertions
        self.assertFalse(result)
        mock_get.assert_called_once_with(self.auth.base_url)

    @patch("scraper.auth.authentication.Session.get")
    def test_login_retry_on_failure(self, mock_get):
        # Mock the GET request to simulate a failure and then success
        mock_get.side_effect = [
            RequestException("Temporary failure"),  # First attempt fails
            MagicMock(
                status_code=200,
                text='<input name="csrf_token" value="test_csrf_token">'
            ),  # Second attempt succeeds
        ]

        with patch("scraper.auth.authentication.Session.post") as mock_post:
            mock_post.return_value = MagicMock(
                status_code=200,
                text="Logout"  # Simulate a successful login
            )

            result = self.auth.login(self.username, self.password)

            # Assertions
            self.assertTrue(result)
            self.assertEqual(mock_get.call_count, 2)  # Two GET attempts
            mock_post.assert_called_once_with(
                self.auth.login_url,
                data={
                    "csrf_token": "test_csrf_token",
                    "username": self.username,
                    "password": self.password,
                },
            )
