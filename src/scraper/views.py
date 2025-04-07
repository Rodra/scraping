from celery.result import AsyncResult
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from data.models import Quote
from data.serializers import QuoteSerializer
from scraper.tasks import scrape_quotes_task


class ScrapeQuotesView(APIView):
    """API endpoint to trigger the scraping process."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Trigger the scraping process by enqueuing a Celery task.
        Args:
            request (Request): The HTTP request object.
        Returns:
            Response: A response indicating a task id for the scraping process.
        """
        # In a real-world application, we would use a more secure method to handle credentials.
        # For example, we might use OAuth or another secure authentication method.
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Enqueue the Celery task
        task = scrape_quotes_task.delay(username, password)
        return Response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)


class ScrapeStatusView(APIView):
    """API endpoint to check the status of a scraping task."""
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        """
        API endpoint to check the status of a scraping task.
        Args:
            task_id (str): The ID of the Celery task.
        Returns:
            Response: A response indicating the status of the task.
        """
        task_result = AsyncResult(task_id)
        if task_result.state == 'SUCCESS':
            return Response(
                {"status": task_result.state, "result": task_result.result},
                status=status.HTTP_200_OK
            )
        if task_result.state == 'PENDING':
            return Response(
                {"status": task_result.state},
                status=status.HTTP_200_OK
            )
        if task_result.state == 'FAILURE':
            return Response(
                {"status": task_result.state, "error": str(task_result.info)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response({"status": task_result.state}, status=status.HTTP_200_OK)


class ScrapedQuotesListView(ListAPIView):
    """API view to fetch all scraped quotes."""
    # In a real-world application, we might want to implement pagination
    # or filtering for the scraped quotes.
    permission_classes = [IsAuthenticated]
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
