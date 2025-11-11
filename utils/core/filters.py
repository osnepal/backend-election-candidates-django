from django.db.models import Q
from rest_framework import serializers


class BaseFilterSerializer(serializers.Serializer):
    """Base filter serializer with common filtering fields"""

    page = serializers.IntegerField(required=False, min_value=1)
    page_size = serializers.IntegerField(required=False, min_value=1, max_value=100)
    ordering = serializers.CharField(required=False)
    search = serializers.CharField(required=False)  # search query
