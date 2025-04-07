import logging

from celery import shared_task
from rest_framework.exceptions import ValidationError

from data.serializers import QuoteSerializer
from scraper.jobs.scrape_quotes import QuoteScraperJob

logger = logging.getLogger(__name__)

@shared_task
def scrape_quotes_task(username: str, password: str):
    """
    Celery task to scrape quotes from the portal and save them to the database.
    """
    # In a real-world application, we could create more celery tasks for different portals.
    # For now, we will just use one task for scraping quotes.
    scraper_job = QuoteScraperJob(username, password)
    quotes = scraper_job.scrape()

    if not quotes:
        logger.warning("No quotes were scraped.")
        return "No quotes found to scrape."

    # Save quotes to the database
    for quote_data in quotes:
        try:
            logger.info(f"Saving quote: {quote_data['text']} by {quote_data['author']}")

            # Use the QuoteSerializer to validate and save the quote
            serializer = QuoteSerializer(data=quote_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ValidationError as e:
            logger.error(f"Validation error saving quote: {quote_data}. Error: {e}")
        except Exception as e:
            logger.error(f"Error saving quote: {quote_data}. Error: {e}")

    return f"Scraped {len(quotes)} quotes successfully."
