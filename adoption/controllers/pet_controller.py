"""HTTP controllers for pet operations.

These views are thin and delegate business logic to the service layer.
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from adoption.models import Pet
from adoption.services import pet_service
from adoption.services.request_pattern import PetAdoptionRequestPattern, RequestValidationError


@login_required
def pet_list(request: HttpRequest) -> HttpResponse:
    """Display a list of available pets."""
    pets = pet_service.get_all_pets()
    return render(request, "adoption/pet_list.html", {
        "pets": pets,
        "page_title": "Available Pets"
    })


@login_required
def pet_detail(request: HttpRequest, pet_id: int) -> HttpResponse:
    """Display details for a single pet."""
    pet = pet_service.get_pet_by_id(pet_id)
    return render(request, "adoption/pet_detail.html", {
        "pet": pet,
        "page_title": pet.name
    })


@login_required
def pet_create(request: HttpRequest) -> HttpResponse:
    """Create a new pet."""
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        species = request.POST.get("species", "").strip()
        breed = request.POST.get("breed", "").strip()
        age_raw = request.POST.get("age", "0").strip()
        description = request.POST.get("description", "").strip()
        status = request.POST.get("status", Pet.STATUS_AVAILABLE)
        image = request.POST.get("image", "").strip()

        age = int(age_raw or 0)

        pet = pet_service.create_pet(
            name=name,
            species=species,
            breed=breed,
            age=age,
            description=description,
            status=status,
            image=image,
        )
        return redirect("pet_detail", pet_id=pet.id)

    context = {"pet": None, "status_choices": Pet.STATUS_CHOICES, "page_title": "Add a Pet"}
    return render(request, "adoption/pet_form.html", context)


@login_required
def pet_update(request: HttpRequest, pet_id: int) -> HttpResponse:
    """Update an existing pet."""
    pet = pet_service.get_pet_by_id(pet_id)

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        species = request.POST.get("species", "").strip()
        breed = request.POST.get("breed", "").strip()
        age_raw = request.POST.get("age", "0").strip()
        description = request.POST.get("description", "").strip()
        status = request.POST.get("status", Pet.STATUS_AVAILABLE)
        image = request.POST.get("image", "").strip()

        age = int(age_raw or 0)

        pet_service.update_pet(
            pet_id=pet.id,
            name=name,
            species=species,
            breed=breed,
            age=age,
            description=description,
            status=status,
            image=image,
        )
        return redirect("pet_detail", pet_id=pet.id)

    context = {"pet": pet, "status_choices": Pet.STATUS_CHOICES, "page_title": "Edit Pet"}
    return render(request, "adoption/pet_form.html", context)


@login_required
def pet_delete(request: HttpRequest, pet_id: int) -> HttpResponse:
    """Delete a pet and redirect to the list."""
    if request.method == "POST":
        pet_service.delete_pet(pet_id)
        return redirect("pet_list")

    pet = pet_service.get_pet_by_id(pet_id)
    return render(request, "adoption/pet_detail.html", {"pet": pet, "confirm_delete": True})


@login_required
def adopt_pet(request: HttpRequest, pet_id: int) -> HttpResponse:
    """Handle an adoption request for a pet."""
    pet = pet_service.get_pet_by_id(pet_id)

    if request.method == "POST":
        adopter_name = request.POST.get("adopter_name", "").strip()
        adopter_email = request.POST.get("adopter_email", "").strip()
        
        try:
            pattern = PetAdoptionRequestPattern(
                pet_id=pet.id,
                adopter_name=adopter_name,
                adopter_email=adopter_email,
            )
            pattern.validate()
            pet_service.request_adoption(pattern)
        except RequestValidationError as e:
            return render(
                request,
                "adoption/pet_detail.html",
                {"pet": pet, "error": str(e)},
            )
        
        success_url = reverse("adoption_success")
        return redirect(success_url)

    return render(request, "adoption/pet_detail.html", {"pet": pet})


@login_required
def adoption_success(request: HttpRequest) -> HttpResponse:
    """Show a friendly adoption success message."""
    return render(request, "adoption/adoption_success.html", {
        "page_title": "Adoption Success"
    })

