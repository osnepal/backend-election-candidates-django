from utils.core.filters import BaseFilterSerializer
from rest_framework import serializers


class PoliticalFigureFilterSerializer(BaseFilterSerializer):
    """Political Figure specific filters"""

    # override to provide specific choices
    ordering = serializers.ChoiceField(
        choices=[("full_name", "full_name asc"), ("-full_name", "full_name desc")],
        required=False,
    )
    # Override to provide search help text in drf-spectacular
    search = serializers.CharField(
        required=False, help_text="Search by full_name, biography"
    )  # search query
