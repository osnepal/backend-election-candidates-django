from apps.political_party.models import PoliticalParty
from rest_framework import serializers


class CreatePoliticalPartySerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliticalParty
        fields = [
            "name",
            "description",
            # Slug will be created automatically
            # "slug",
            "abbreviation",
            "founded_date",
            "ideology",
            "hq_location",
            "website",
            "logo_url",
        ]

        # require all fields from FE, but allow them to be set as black or null as required
        extra_kwargs = {
            "name": {"required": True},
            "description": {"required": True, "allow_blank": False},
            "abbreviation": {"required": True, "allow_blank": False},
            "founded_date": {
                "required": True,
                "allow_null": False,
            },
            "ideology": {"required": True, "allow_blank": False},
            "hq_location": {"required": True, "allow_blank": False},
            "website": {"required": True, "allow_blank": True},
            "logo_url": {"required": True, "allow_blank": False},
        }


class UpdatePoliticalPartySerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliticalParty
        fields = [
            "name",
            "description",
            "abbreviation",
            "founded_date",
            "ideology",
            "hq_location",
            "website",
            "logo_url",
        ]

        # require all fields from FE, but allow them to be set as black or null as required
        # NOTE: we'll be using partial=True so the required fields will be optional
        extra_kwargs = {
            "name": {"required": True},
            "description": {"required": True, "allow_blank": False},
            "abbreviation": {"required": True, "allow_blank": False},
            "founded_date": {
                "required": True,
                "allow_null": False,
            },
            "ideology": {"required": True, "allow_blank": False},
            "hq_location": {"required": True, "allow_blank": False},
            "website": {"required": True, "allow_blank": True},
            "logo_url": {"required": True, "allow_blank": False},
        }


class GetPoliticalPartyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliticalParty
        fields = [
            "id",
            "slug",
            "name",
            "abbreviation",
            "description",
            "founded_date",
            "ideology",
            "hq_location",
            "website",
            "logo_url",
            "created_at",
            "updated_at",
        ]
        ref_name = "GetPoliticalPartyDetailSerializer"
