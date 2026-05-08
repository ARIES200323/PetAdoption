"""Admin configuration for adoption app."""

from django.contrib import admin

from adoption.models import AdoptionRequest, Pet


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ("name", "species", "breed", "age", "status")
    list_filter = ("species", "status")
    search_fields = ("name", "breed", "species")


@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ("pet", "adopter_name", "adopter_email", "request_date")
    list_filter = ("request_date",)
    search_fields = ("adopter_name", "adopter_email", "pet__name")

