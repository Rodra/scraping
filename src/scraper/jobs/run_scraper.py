import sys
from pathlib import Path

# Add the `src` directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from scraper.jobs.scrape_quotes import QuoteScraperJob

if __name__ == "__main__":
    # Replace these with your actual credentials
    username = "your_username"
    password = "your_password"

    # Initialize the scraper job
    scraper_job = QuoteScraperJob(username, password)

    # Run the scrape method
    scraper_job.scrape()