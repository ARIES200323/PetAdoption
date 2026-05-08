"""Database models for the Pet Adoption System."""

from django.db import models


class Pet(models.Model):
    """Represents a pet that can be adopted."""

    STATUS_AVAILABLE = "available"
    STATUS_ADOPTED = "adopted"

    STATUS_CHOICES = [
        (STATUS_AVAILABLE, "Available"),
        (STATUS_ADOPTED, "Adopted"),
    ]

    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50)
    breed = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField(help_text="Age in years")
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_AVAILABLE,
    )
    image = models.URLField(
        max_length=500,
        blank=True,
        help_text="URL to an image of the pet",
    )

    def __str__(self) -> str:
        return f"{self.name} ({self.species})"


class AdoptionRequest(models.Model):
    """Represents a request to adopt a pet."""

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="adoption_requests")
    adopter_name = models.CharField(max_length=100)
    adopter_email = models.EmailField()
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Request by {self.adopter_name} for {self.pet.name}"

