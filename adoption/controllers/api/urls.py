"""API URL routes for the adoption app."""

from django.urls import path

from adoption.controllers import auth_controller
from adoption.controllers.api import pet_api_controller

urlpatterns = [
    # Authentication endpoints
    path("auth/register/", auth_controller.register_user, name="api_register"),
    path("auth/login/", auth_controller.login_user, name="api_login"),
    path("auth/refresh/", auth_controller.refresh_token, name="api_refresh_token"),
    path("auth/profile/", auth_controller.get_user_profile, name="api_user_profile"),

    # Pet endpoints
    path("pets/", pet_api_controller.pet_list_api, name="api_pet_list"),
    path("pets/<int:pet_id>/", pet_api_controller.pet_detail_api, name="api_pet_detail"),
    path("pets/create/", pet_api_controller.pet_create_api, name="api_pet_create"),
    path("pets/<int:pet_id>/update/", pet_api_controller.pet_update_api, name="api_pet_update"),
    path("pets/<int:pet_id>/delete/", pet_api_controller.pet_delete_api, name="api_pet_delete"),
    path("pets/<int:pet_id>/adopt/", pet_api_controller.adopt_pet_api, name="api_adopt_pet"),
]
