from utils.core.filters import BaseFilterSerializer
from rest_framework import serializers


class PoliticalPartyFilterSerializer(BaseFilterSerializer):
    """Political Party specific filters"""

    # override to provide specific choices
    ordering = serializers.ChoiceField(
        choices=[
            ("name", "name asc"),
            ("-name", "name desc"),
            ("founded_date", "founded_date asc"),
            ("-founded_date", "founded_date desc"),
        ],
        required=False,
    )

    # Override to provide search help text
    search = serializers.CharField(
        required=False, help_text="Search by name, description"
    )  # search query

    # set allow_null=True for any boolean field
    is_active = serializers.BooleanField(required=False, allow_null=True)

    # For explanation:
    # serializer.data will result in {"is_active": False}.
    # is_active is serializers.BooleanField(required=False). And if empty QueryDict is passed, serializer automatically sets it to False for some reason.
    # As it turns out, it happens even with HTML data?
    # See: https://stackoverflow.com/questions/68863717/django-drf-serializers-booleanfield-receive-false-by-default-but-need-none
    # https://github.com/encode/django-rest-framework/issues/3811
    # https://github.com/encode/django-rest-framework/issues/2776
    # from django.http import QueryDict
    # q = QueryDict(mutable=True)
    # serializer = ProductFilterSerializer(data=q)
