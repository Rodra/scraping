from django.urls import path

from scraper.views import (ScrapedQuotesListView, ScrapeQuotesView,
                           ScrapeStatusView)

urlpatterns = [
    path('scrape/', ScrapeQuotesView.as_view(), name='scrape-quotes'),
    path('scrape/<str:task_id>/', ScrapeStatusView.as_view(), name='scrape-status'),
    path('quotes/', ScrapedQuotesListView.as_view(), name='scraped-quotes'),
]
