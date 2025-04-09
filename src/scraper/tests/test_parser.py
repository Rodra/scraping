import unittest
from unittest.mock import MagicMock, patch

from bs4 import BeautifulSoup

from scraper.auth.quote_scraper_auth import QuoteScraperAuth
from scraper.parsers.quote_parser import QuoteParser


class TestQuoteParser(unittest.TestCase):
    def setUp(self):
        self.mock_auth = MagicMock(spec=QuoteScraperAuth)
        self.mock_auth.base_url = "https://quotes.toscrape.com"
        self.parser = QuoteParser(auth=self.mock_auth)

    @patch("scraper.parsers.quote_parser.QuoteParser.fetch_page")
    def test_parse_page(self, mock_fetch_page):
        # Mock the page content
        html = '''
        <div class="quote">
            <span class="text">"Life is what happens when you're busy making other plans."</span>
            <span>by <small class="author">John Lennon</small>
                <a href="/author/John-Lennon">(about)</a>
            </span>
            <div class="tags">
                <a class="tag" href="/tag/life/">life</a>
                <a class="tag" href="/tag/plans/">plans</a>
            </div>
        </div>
        <div class="quote">
            <span class="text">The greatest glory in living lies not in never falling, but in rising every time we fall.</span>
            <span>by <small class="author">Nelson Mandela</small>
                <a href="/author/Nelson-Mandela">(about)</a>
            </span>
            <div class="tags">
                <a class="tag" href="/tag/glory/">glory</a>
                <a class="tag" href="/tag/life/">life</a>
            </div>
        </div>
        <li class="next">
            <a href="/page/2/">Next</a>
        </li>
        '''
        soup = BeautifulSoup(html, "html.parser")
        mock_fetch_page.return_value = soup

        # Call the method
        quotes, next_page_url = self.parser.parse_page("https://quotes.toscrape.com/page/1/")

        # Assertions for quotes
        self.assertEqual(len(quotes), 2)
        self.assertEqual(quotes[0]["author"], "John Lennon")
        self.assertEqual(quotes[1]["author"], "Nelson Mandela")

        # Assertions for next page URL
        self.assertEqual(next_page_url, "https://quotes.toscrape.com/page/2/")

    @patch("scraper.parsers.quote_parser.QuoteParser.fetch_page")
    def test_parse_page_no_next(self, mock_fetch_page):
        # Mock the page content without a "Next" button
        html = '''
        <div class="quote">
            <span class="text">"Life is what happens when you're busy making other plans."</span>
            <span>by <small class="author">John Lennon</small>
                <a href="/author/John-Lennon">(about)</a>
            </span>
            <div class="tags">
                <a class="tag" href="/tag/life/">life</a>
                <a class="tag" href="/tag/plans/">plans</a>
            </div>
        </div>
        '''
        soup = BeautifulSoup(html, "html.parser")
        mock_fetch_page.return_value = soup

        # Call the method
        quotes, next_page_url = self.parser.parse_page("https://quotes.toscrape.com/page/1/")

        # Assertions for quotes
        self.assertEqual(len(quotes), 1)
        self.assertEqual(quotes[0]["author"], "John Lennon")

        # Assertions for next page URL
        self.assertIsNone(next_page_url)

    @patch("scraper.parsers.quote_parser.QuoteParser.fetch_page")
    def test_parse_page_with_invalid_quotes(self, mock_fetch_page):
        # Mock the page content with an invalid quote
        html = '''
        <div class="quote">
            <span class="text"></span>
            <small class="author"></small>
        </div>
        <li class="next">
            <a href="/page/2/">Next</a>
        </li>
        '''
        soup = BeautifulSoup(html, "html.parser")
        mock_fetch_page.return_value = soup

        # Call the method
        quotes, next_page_url = self.parser.parse_page("https://quotes.toscrape.com/page/1/")

        # Assertions for quotes
        self.assertEqual(len(quotes), 0)  # No valid quotes

        # Assertions for next page URL
        self.assertEqual(next_page_url, "https://quotes.toscrape.com/page/2/")
