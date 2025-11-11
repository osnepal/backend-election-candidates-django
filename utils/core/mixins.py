from rest_framework.response import Response
from .pagination import StandardResultsSetPagination
from rest_framework.pagination import PageNumberPagination


class PaginatedAPIMixin:
    """
    Mixin to add pagination support to API views.
    Usage: Include this mixin in your view and call paginate_queryset()
    """

    pagination_class = StandardResultsSetPagination

    def paginate_queryset(self, queryset):
        """
        Paginate a queryset and return paginated data
        """
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, self.request)
        return paginated_queryset, paginator

    def get_paginated_response(self, serializer_data, paginator: PageNumberPagination):
        """
        Return paginated response
        """
        return paginator.get_paginated_response(serializer_data)


class FilteredAPIMixin:
    """
    Mixin to add filtering support to API views.
    Define filter_serializer_class in your view
    """

    filter_serializer_class = None

    def get_filter_params(self):
        """
        Validate and return filter parameters
        """
        if not self.filter_serializer_class:
            return {}

        # serializer.data will result in {"is_active": False}.
        # is_active is serializers.BooleanField(required=False). And if empty QueryDict is passed, serializer automatically sets it to False for some reason.
        # As it turns out, it happens even with HTML data?
        # See: https://stackoverflow.com/questions/68863717/django-drf-serializers-booleanfield-receive-false-by-default-but-need-none
        # https://github.com/encode/django-rest-framework/issues/3811
        # https://github.com/encode/django-rest-framework/issues/2776
        # from django.http import QueryDict
        # q = QueryDict(mutable=True)
        # serializer = ProductFilterSerializer(data=q)

        serializer = self.filter_serializer_class(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    def apply_ordering(self, queryset, ordering):
        """
        Apply ordering to queryset
        """
        if ordering:
            # Support multiple orderings: ?ordering=-created_at,name
            order_fields = [f.strip() for f in ordering.split(",")]
            queryset = queryset.order_by(*order_fields)
        return queryset
