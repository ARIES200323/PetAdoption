
from __future__ import annotations

from typing import Iterable

from django.shortcuts import get_object_or_404

from adoption.models import AdoptionRequest, Pet
from adoption.services.request_pattern import (
    PetAdoptionRequestPattern,
    RequestValidationError,
)


def get_all_pets() -> Iterable[Pet]:
    """Return all available pets."""
    return Pet.objects.filter(status=Pet.STATUS_AVAILABLE).order_by("name")


def get_available_pet_count() -> int:
    """Return the number of available pets."""
    return Pet.objects.filter(status=Pet.STATUS_AVAILABLE).count()


def get_adoption_request_count() -> int:
    """Return the total number of adoption requests."""
    return AdoptionRequest.objects.count()


def get_pet_by_id(pet_id: int) -> Pet:
    """Return a single pet by ID or raise 404 if not found."""
    return get_object_or_404(Pet, pk=pet_id)


def create_pet(
    name: str,
    species: str,
    breed: str,
    age: int,
    description: str | None = None,
    status: str = Pet.STATUS_AVAILABLE,
    image: str | None = None,
) -> Pet:
    """Create and return a new pet."""
    pet = Pet(
        name=name,
        species=species,
        breed=breed,
        age=age,
        description=description,
        status=status,
        image=image,
    )
    pet.save()
    return pet


def update_pet(
    pet_id: int,
    name: str,
    species: str,
    breed: str,
    age: int,
    description: str | None,
    status: str,
    image: str | None,
) -> Pet:
    """Update an existing pet and return it."""
    pet = get_pet_by_id(pet_id)
    pet.name = name
    pet.species = species
    pet.breed = breed
    pet.age = age
    pet.description = description
    pet.status = status
    pet.image = image
    pet.save()
    return pet


def delete_pet(pet_id: int) -> None:
    """Delete a pet by ID."""
    pet = get_pet_by_id(pet_id)
    pet.delete()


def request_adoption(request_pattern: PetAdoptionRequestPattern) -> AdoptionRequest:
    """Create an adoption request and mark the pet as adopted.

    Business rule:
    - When an adoption request is submitted, the pet status changes to 'adopted'.
    - Validation is handled by the service layer using the request pattern.
    """
    request_pattern.validate()

    pet = get_pet_by_id(request_pattern.pet_id)
    adoption_request = AdoptionRequest.objects.create(
        pet=pet,
        adopter_name=request_pattern.adopter_name,
        adopter_email=request_pattern.adopter_email,
    )
    pet.status = Pet.STATUS_ADOPTED
    pet.save()
    return adoption_request

