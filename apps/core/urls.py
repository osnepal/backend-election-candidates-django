from django.urls import include, path
from . import views

urlpatterns = [
    # Political Party
    path("core/", include([])),
    path(
        "countries/get/list/",
        views.GetCountryListAPI.as_view(),
        name="get-country-list",
    ),
]
