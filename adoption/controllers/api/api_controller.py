
import json

from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotAllowed,
    JsonResponse,
)
from django.views.decorators.csrf import csrf_exempt

from adoption.models import AdoptionRequest, Pet
from adoption.services import pet_service
from adoption.services.request_pattern import PetAdoptionRequestPattern, RequestValidationError


def serialize_pet(pet: Pet) -> dict:
    return {
        "id": pet.id,
        "name": pet.name,
        "species": pet.species,
        "breed": pet.breed,
        "age": pet.age,
        "description": pet.description,
        "status": pet.status,
        "image": pet.image,
    }


def serialize_adoption_request(adoption_request: AdoptionRequest) -> dict:
    return {
        "id": adoption_request.id,
        "pet": serialize_pet(adoption_request.pet),
        "adopter_name": adoption_request.adopter_name,
        "adopter_email": adoption_request.adopter_email,
        "request_date": adoption_request.request_date.isoformat(),
    }


def api_pet_list(request: HttpRequest) -> JsonResponse:
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    pets = pet_service.get_all_pets()
    return JsonResponse([serialize_pet(pet) for pet in pets], safe=False)


def api_pet_detail(request: HttpRequest, pet_id: int) -> JsonResponse:
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    pet = pet_service.get_pet_by_id(pet_id)
    return JsonResponse(serialize_pet(pet))


@csrf_exempt
def api_request_adoption(request: HttpRequest, pet_id: int) -> HttpResponse:
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON payload.")

    try:
        adoption_request_pattern = PetAdoptionRequestPattern.from_payload(pet_id, payload)
        adoption_request = pet_service.request_adoption(adoption_request_pattern)
    except RequestValidationError as exc:
        return HttpResponseBadRequest(str(exc))

    return JsonResponse(serialize_adoption_request(adoption_request), status=201)
