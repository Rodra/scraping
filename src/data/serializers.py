from rest_framework import serializers
from .models import Quote, Tag


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for the Tag model.
    """

    class Meta:
        model = Tag
        fields = ["id", "name", "url"]


class QuoteSerializer(serializers.ModelSerializer):
    """
    Serializer for the Quote model.
    """
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Quote
        fields = ["id", "text", "author", "author_url", "goodreads_url", "tags"]
