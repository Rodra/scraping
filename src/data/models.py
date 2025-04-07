from django.db import models


class Tag(models.Model):
    """
    Represents a quote tag.
    Attributes:
        name (str): The name of the tag.
        url (str): URL to the tag's page.
    """

    name = models.CharField(max_length=255, unique=True)
    url = models.URLField()

    def __str__(self):
        return self.name


class Quote(models.Model):
    """
    Represents a quote with its metadata.
    Attributes:
        text (str): The text of the quote.
        author (str): The author of the quote.
        author_url (str): URL to the author's profile.
        goodreads_url (str): URL to the author's Goodreads profile (optional).
        tags (list): A list of tags associated with the quote.
    """

    text = models.TextField()
    author = models.CharField(max_length=255)
    author_url = models.URLField()
    goodreads_url = models.URLField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name="quotes")

    def __str__(self):
        return f'"{self.text}" by {self.author}'
