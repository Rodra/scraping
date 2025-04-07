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
    tags = TagSerializer(many=True)

    class Meta:
        model = Quote
        fields = ["id", "text", "author", "author_url", "goodreads_url", "tags"]

    def create(self, validated_data):
        """
        Custom create method to handle nested tags.
        """
        tags_data = validated_data.pop("tags", [])
        quote = Quote.objects.create(**validated_data)

        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(**tag_data)
            quote.tags.add(tag)

        return quote
