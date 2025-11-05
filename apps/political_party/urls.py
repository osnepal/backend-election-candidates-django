from django.urls import include, path
from . import views

urlpatterns = [
    # Political Party
    path(
        "",
        views.PoliticalPartyListCreateAPI.as_view(),
        name="political-party-list-create",
    ),
    path(
        "<int:pk>/",
        views.PoliticalPartyRetrieveUpdateDeleteAPI.as_view(),
        name="political-party-detail",
    ),
]
