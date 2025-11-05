from django.urls import include, path
from . import views

urlpatterns = [
    path(
        "political-figures/",
        include(
            [
                path(
                    "",
                    views.PoliticalFigureListCreateAPI.as_view(),
                    name="political-figure-list-create",
                ),
                path(
                    "<int:pk>/",
                    views.PoliticalFigureRetrieveUpdateDeleteAPI.as_view(),
                    name="political-figure-detail",
                ),
            ]
        ),
    ),
]
