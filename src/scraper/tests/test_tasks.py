from django.test import TestCase
from unittest.mock import patch
from data.models import Quote, Tag
from scraper.tasks import scrape_quotes_task


class ScrapeQuotesTaskTestCase(TestCase):
    @patch("scraper.tasks.QuoteScraperJob")
    def test_no_quotes_scraped(self, mock_scraper_job):
        """
        Test the task when no quotes are scraped.
        """
        # Mock the scraper to return no quotes
        mock_scraper_job.return_value.scrape.return_value = []

        result = scrape_quotes_task("username", "password")

        self.assertEqual(result, "No quotes found to scrape.")

    @patch("scraper.tasks.QuoteScraperJob")
    def test_quotes_with_new_tags(self, mock_scraper_job):
        """
        Test the task when quotes with new tags are scraped.
        """
        # Mock the scraper to return quotes with new tags
        mock_scraper_job.return_value.scrape.return_value = [
            {
                "text": "Life is what happens when you're busy making other plans.",
                "author": "John Lennon",
                "author_url": "https://quotes.toscrape.com/author/John-Lennon",
                "goodreads_url": None,
                "tags": [
                    {"name": "life", "url": "https://quotes.toscrape.com/tag/life/"},
                    {"name": "plans", "url": "https://quotes.toscrape.com/tag/plans/"},
                ],
            }
        ]

        result = scrape_quotes_task("username", "password")

        # Assert the quote and tags are created
        self.assertEqual(Quote.objects.count(), 1)
        self.assertEqual(Tag.objects.count(), 2)
        self.assertEqual(result, "Scraped 1 quotes successfully.")

    @patch("scraper.tasks.QuoteScraperJob")
    def test_quotes_with_existing_tags(self, mock_scraper_job):
        """
        Test the task when quotes with existing tags are scraped.
        """
        # Create existing tags
        Tag.objects.create(name="life", url="https://quotes.toscrape.com/tag/life/")
        Tag.objects.create(name="plans", url="https://quotes.toscrape.com/tag/plans/")

        # Mock the scraper to return quotes with existing tags
        mock_scraper_job.return_value.scrape.return_value = [
            {
                "text": "Life is what happens when you're busy making other plans.",
                "author": "John Lennon",
                "author_url": "https://quotes.toscrape.com/author/John-Lennon",
                "goodreads_url": None,
                "tags": [
                    {"name": "life", "url": "https://quotes.toscrape.com/tag/life/"},
                    {"name": "plans", "url": "https://quotes.toscrape.com/tag/plans/"},
                ],
            }
        ]

        result = scrape_quotes_task("username", "password")

        # Assert the quote is created and tags are reused
        self.assertEqual(Quote.objects.count(), 1)
        self.assertEqual(Tag.objects.count(), 2)  # No new tags should be created
        self.assertEqual(result, "Scraped 1 quotes successfully.")

    @patch("scraper.tasks.QuoteScraperJob")
    def test_error_during_quote_saving(self, mock_scraper_job):
        """
        Test the task when an error occurs during quote saving.
        """
        # Mock the scraper to return invalid quote data
        mock_scraper_job.return_value.scrape.return_value = [
            {
                "text": "",
                "author": "John Lennon",
                "author_url": "https://quotes.toscrape.com/author/John-Lennon",
                "goodreads_url": None,
                "tags": [
                    {"name": "life", "url": "https://quotes.toscrape.com/tag/life/"},
                ],
            }
        ]

        result = scrape_quotes_task("username", "password")

        # Assert no quotes are created
        self.assertEqual(Quote.objects.count(), 0)
        self.assertEqual(Tag.objects.count(), 0)
        self.assertEqual(result, "Scraped 1 quotes successfully.")  # Task still completes
