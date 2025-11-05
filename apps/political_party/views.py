from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from drf_spectacular.utils import extend_schema

from apps.political_party.models import PoliticalParty
from apps.political_party.serializers import GetPoliticalPartyDetailSerializer
from utils.core.base_views import PublicAPIView
from utils.core.response_wrappers import OKResponse, NoContentResponse
from utils.political_party.core import PoliticalPartyUtil


# ---------------------------------------------------------------------
# List + Create
# ---------------------------------------------------------------------
class PoliticalPartyListCreateAPI(PublicAPIView):
    """
    GET: List all political parties
    POST: Create a new political party
    """

    parser_classes = [JSONParser, MultiPartParser, FormParser]
    output_serializer = GetPoliticalPartyDetailSerializer

    @extend_schema(responses=output_serializer(many=True))
    def get(self, request):
        """
        GET: List all political parties
        """
        queryset = PoliticalParty.objects.all().order_by("-created_at")
        serializer = self.output_serializer(queryset, many=True)
        return OKResponse(data=serializer.data)

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
