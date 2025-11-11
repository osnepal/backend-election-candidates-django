from django.shortcuts import get_object_or_404
from apps.political_figure.filters import PoliticalFigureFilterSerializer
from apps.political_figure.models import PoliticalFigure
from apps.political_figure.serializers import GetPoliticalFigureDetailSerializer
from apps.political_party.filters import PoliticalPartyFilterSerializer
from utils.core.base_views import PublicAPIView
from utils.core.mixins import FilteredAPIMixin, PaginatedAPIMixin
from utils.core.response_wrappers import NoContentResponse, OKResponse
from utils.political_figure.core import PoliticalFigureUtil
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from drf_spectacular.utils import extend_schema

from django.db.models import Q


# ---------------------------------------------------------------------
# Serializer (same as before)
# ---------------------------------------------------------------------
class PoliticalFigureListCreateAPI(PublicAPIView, PaginatedAPIMixin, FilteredAPIMixin):
    """
    GET: List all political figures
    POST: Create a new political figure
    """

    # NOTE: we need the multipart parser and form parser for file upload
    # But also allow JSONParser so that user can create using drf-spectacular's swagger ui.
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    output_serializer = GetPoliticalFigureDetailSerializer
    filter_serializer_class = PoliticalFigureFilterSerializer

    @extend_schema(
        responses=output_serializer(many=True), parameters=[filter_serializer_class]
    )
    def get(self, request):
        """
        GET: List all political figures

        """

        # Get validated filter params
        filters = self.get_filter_params()

        # build base queryset
        queryset = PoliticalFigure.objects.all().prefetch_related(
            "home_address", "current_address"
        )

        # apply search if provided
        search = filters.get("search")

        if search:
            q_object = Q()
            q_object |= Q(full_name__icontains=search)
            q_object |= Q(biography__icontains=search)
            queryset = queryset.filter(q_object)

        # apply filters; no filters are available right now

        # apply ordering
        ordering = filters.get("ordering", "-created_at")
        queryset = self.apply_ordering(queryset, ordering)

        # apply pagination
        queryset, paginator = self.paginate_queryset(queryset)

        # serialize
        serializer = self.output_serializer(queryset, many=True)

        # Return paginated response
        return self.get_paginated_response(serializer.data, paginator)

    @extend_schema(
        request=PoliticalFigureUtil.create_serializer,
        responses=output_serializer,
    )
    def post(self, request):
        """
        POST: Create a new political figure
        """
        political_figure = PoliticalFigureUtil.create_political_figure(request.data)
        output_data = self.output_serializer(political_figure).data
        return OKResponse(data=output_data)


# ---------------------------------------------------------------------
# Retrieve + Update + Delete
# ---------------------------------------------------------------------
class PoliticalFigureRetrieveUpdateDeleteAPI(PublicAPIView):
    """
    GET: Retrieve
    PATCH: Update
    DELETE: Delete
    """

    # NOTE: we need the multipart parser and form parser for file upload
    # But also allow JSONParser so that user can create using drf-spectacular's swagger ui.
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    output_serializer = GetPoliticalFigureDetailSerializer

    def get_object(self, pk):
        return get_object_or_404(
            PoliticalFigure.objects.prefetch_related("home_address", "current_address"),
            pk=pk,
        )

    @extend_schema(responses=output_serializer)
    def get(self, request, pk):
        instance = self.get_object(pk)
        serializer = self.output_serializer(instance)
        return OKResponse(data=serializer.data)

    @extend_schema(
        request=PoliticalFigureUtil.update_serializer,
        responses=output_serializer,
    )
    def patch(self, request, pk):
        """
        Update political figure.
        For updating via drf-spectacular form, send `null` wherever a file is expected, and empty string wherever a string `""` is expected and value is optional.
        Don't send the fields that you don't want to update cause this is a patch update.
        """
        instance = self.get_object(pk)
        PoliticalFigureUtil.update_political_figure(instance, request.data)

        # fetch again since photo sometimes somehow becomes null in instance after update
        updated_instance = self.get_object(pk)
        serializer = self.output_serializer(updated_instance)
        return OKResponse(data=serializer.data)

    @extend_schema(responses=None)
    def delete(self, request, pk):
        """Delete political figure"""
        instance = self.get_object(pk)
        PoliticalFigureUtil.delete_political_figure(political_figure=instance)
        return NoContentResponse()
