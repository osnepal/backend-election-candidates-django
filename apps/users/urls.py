# apps/users/urls.py
from django.urls import path, include
from .views import auth as auth_views
from .views import users as user_views

app_name = "users"

urlpatterns = [
    path(
        "users/",
        include(
            [
                path(
                    "tokens/generate/",
                    auth_views.TokenGenerateAPI.as_view(),
                    name="token-generate",
                ),
                path(
                    "tokens/refresh/",
                    auth_views.TokenRefreshAPI.as_view(),
                    name="token-refresh",
                ),
                path(
                    "profile/", user_views.UserProfileAPI.as_view(), name="user-profile"
                ),
                path("list/", user_views.UserListAPI.as_view(), name="user-list"),
            ]
        ),
    ),
]
