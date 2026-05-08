"""URL configuration for the adoption app."""

from django.urls import include, path

from adoption.controllers import pet_controller, user_controller

urlpatterns = [
    path("", user_controller.home, name="home"),
    path("dashboard/", user_controller.dashboard_home, name="dashboard"),
    path("about/", user_controller.about_us, name="about_us"),
    path("settings/", user_controller.settings, name="settings"),
    path("accounts/login/", user_controller.login_view, name="login"),
    path("accounts/logout/", user_controller.logout_view, name="logout"),
    path("accounts/register/", user_controller.register, name="register"),
    path("pets/", pet_controller.pet_list, name="pet_list"),
    path("pets/<int:pet_id>/", pet_controller.pet_detail, name="pet_detail"),
    path("pets/create/", pet_controller.pet_create, name="pet_create"),
    path("pets/<int:pet_id>/edit/", pet_controller.pet_update, name="pet_update"),
    path("pets/<int:pet_id>/delete/", pet_controller.pet_delete, name="pet_delete"),
    path("pets/<int:pet_id>/adopt/", pet_controller.adopt_pet, name="adopt_pet"),
    path("adoption/success/", pet_controller.adoption_success, name="adoption_success"),
    path("api/", include("adoption.controllers.api.urls")),
]

