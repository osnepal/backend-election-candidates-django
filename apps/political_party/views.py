from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from drf_spectacular.utils import extend_schema

from apps.political_party.filters import PoliticalPartyFilterSerializer
from apps.political_party.models import PoliticalParty
from apps.political_party.serializers import GetPoliticalPartyDetailSerializer
from utils.core.base_views import PublicAPIView
from utils.core.mixins import FilteredAPIMixin, PaginatedAPIMixin
from utils.core.response_wrappers import OKResponse, NoContentResponse
from utils.political_party.core import PoliticalPartyUtil
from django.db.models import Q


# ---------------------------------------------------------------------
# List + Create
# ---------------------------------------------------------------------
class PoliticalPartyListCreateAPI(PublicAPIView, PaginatedAPIMixin, FilteredAPIMixin):
    """
    GET: List all political parties
    POST: Create a new political party
    """

    parser_classes = [JSONParser, MultiPartParser, FormParser]
    output_serializer = GetPoliticalPartyDetailSerializer
    filter_serializer_class = PoliticalPartyFilterSerializer

    @extend_schema(
        responses=output_serializer(many=True),
        parameters=[
            filter_serializer_class,
        ],
    )
    def get(self, request):
        """
        GET: List all political parties
        """
        # Get validated filter params
        filters = self.get_filter_params()

        # Build base queryset
        political_parties = PoliticalParty.objects.all()

        # Apply search if provided
        search = filters.get("search")

        if search:
            q_object = Q()
            q_object |= Q(name__icontains=search)
            q_object |= Q(description__icontains=search)
            political_parties = political_parties.filter(q_object)

        # apply filters
        if filters.get("is_active") is not None:
            is_active = filters["is_active"]
            temp_filter = {"dissolved_date__isnull": True}
            if not is_active:
                temp_filter["dissolved_date__isnull"] = False

            political_parties = political_parties.filter(**temp_filter)

        # Apply ordering
        ordering = filters.get("ordering", "-created_at")
        political_parties = self.apply_ordering(political_parties, ordering)

        # Paginate
        paginated_political_parties, paginator = self.paginate_queryset(
            political_parties
        )

        # Serialize
        serializer = self.output_serializer(paginated_political_parties, many=True)

        # Return paginated response
        return self.get_paginated_response(serializer.data, paginator)

    @extend_schema(
        request=PoliticalPartyUtil.create_serializer,
        responses=output_serializer,
    )
    def post(self, request):
        """
        POST: Create a new political party
        """
        instance = PoliticalPartyUtil.create_political_party(request.data)
        serializer = self.output_serializer(instance)
        return OKResponse(
            data=serializer.data, message="Political Party created successfully"
        )


# ---------------------------------------------------------------------
# Retrieve + Update + Delete
# ---------------------------------------------------------------------
class PoliticalPartyRetrieveUpdateDeleteAPI(PublicAPIView):
    """
    GET: Retrieve
    PATCH: Update
    DELETE: Delete
    """

    parser_classes = [JSONParser, MultiPartParser, FormParser]
    output_serializer = GetPoliticalPartyDetailSerializer

    def get_object(self, pk):
        return get_object_or_404(PoliticalParty, pk=pk)

    @extend_schema(responses=output_serializer)
    def get(self, request, pk):
        """
        GET: Retrieve political party
        """
        instance = self.get_object(pk)
        serializer = self.output_serializer(instance)
        return OKResponse(data=serializer.data)

    @extend_schema(
        request=PoliticalPartyUtil.update_serializer,
        responses=output_serializer,
    )
    def patch(self, request, pk):
        """
        PATCH: Update political party
        """
        instance = self.get_object(pk)
        PoliticalPartyUtil.update_political_party(instance, request.data)

        updated_instance = self.get_object(pk)
        serializer = self.output_serializer(updated_instance)
        return OKResponse(
            data=serializer.data, message="Political Party updated successfully"
        )

    @extend_schema(responses=None)
    def delete(self, request, pk):
        """
        DELETE: Delete political party
        """
        instance = self.get_object(pk)
        PoliticalPartyUtil.delete_political_party(instance)
        return NoContentResponse(message="Political Party deleted successfully")
