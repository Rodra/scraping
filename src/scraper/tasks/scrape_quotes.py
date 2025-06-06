import logging

from celery import shared_task
from rest_framework.exceptions import ValidationError

from data.models import Tag
from data.serializers import QuoteSerializer, TagSerializer
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

            # Validate the quote data first
            quote_serializer = QuoteSerializer(data=quote_data)
            quote_serializer.is_valid(raise_exception=True)

            #  Process tags only after the quote is validated
            tags_data = quote_data.pop("tags", [])
            tag_instances = []
            for tag_data in tags_data:
                tag = Tag.objects.filter(name=tag_data["name"]).first()
                if not tag:
                    logger.info(f"Saving tag: {tag_data['name']}")
                    tag_serializer = TagSerializer(data=tag_data)
                    tag_serializer.is_valid(raise_exception=True)
                    tag = tag_serializer.save()
                logger.info(f"Tag found: {tag_data['name']}")
                tag_instances.append(tag)

            # Save the quote
            quote = quote_serializer.save()

            # Associate tags with the quote
            quote.tags.set(tag_instances)

        # In real-world applications, we could handle this errors with a more complex
        # retry logic or error handling mechanism just for quotes that we couldn't save.
        # For now, we will just log the error and continue with the next quote.
        except ValidationError as e:
            logger.error(f"Validation error saving quote: {quote_data}. Error: {e}")
        except Exception as e:
            logger.error(f"Error saving quote: {quote_data}. Error: {e}")

    return f"Scraped {len(quotes)} quotes successfully."
