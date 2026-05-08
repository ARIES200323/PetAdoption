"""Root URL configuration for Pet Adoption System."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("adoption.controllers.api.urls")),
    path("", include("adoption.urls")),
]

