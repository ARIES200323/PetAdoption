from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from adoption.models import Pet, AdoptionRequest
from adoption.services import pet_service


@api_view(['GET'])
def pet_list_api(request):
    """Get all available pets."""
    try:
        pets = pet_service.get_all_pets()
        pet_data = []
        for pet in pets:
            pet_data.append({
                'id': pet.id,
                'name': pet.name,
                'species': pet.species,
                'breed': pet.breed,
                'age': pet.age,
                'description': pet.description,
                'status': pet.status,
                'image': pet.image,
            })

        return Response({
            'count': len(pet_data),
            'results': pet_data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def pet_detail_api(request, pet_id):
    """Get details of a specific pet."""
    try:
        pet = pet_service.get_pet_by_id(pet_id)
        if not pet:
            return Response(
                {'error': 'Pet not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        pet_data = {
            'id': pet.id,
            'name': pet.name,
            'species': pet.species,
            'breed': pet.breed,
            'age': pet.age,
            'description': pet.description,
            'status': pet.status,
            'image': pet.image,
        }

        return Response(pet_data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def pet_create_api(request):
    """Create a new pet."""
    try:
        name = request.data.get('name', '').strip() if isinstance(request.data.get('name'), str) else str(request.data.get('name', '')).strip()
        species = request.data.get('species', '').strip() if isinstance(request.data.get('species'), str) else str(request.data.get('species', '')).strip()
        breed = request.data.get('breed', '').strip() if isinstance(request.data.get('breed'), str) else str(request.data.get('breed', '')).strip()

        # Handle age - can be int or string
        age_raw = request.data.get('age', 0)
        if isinstance(age_raw, str):
            age_str = age_raw.strip()
        else:
            age_str = str(age_raw)

        description = request.data.get('description', '').strip() if isinstance(request.data.get('description'), str) else str(request.data.get('description', '')).strip()
        status_value = request.data.get('status', Pet.STATUS_AVAILABLE)
        image = request.data.get('image', '').strip() if isinstance(request.data.get('image'), str) else str(request.data.get('image', '')).strip()

        # Validation
        if not name or not species:
            return Response(
                {'error': 'Name and species are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            age = int(age_str)
            if age < 0:
                raise ValueError
        except ValueError:
            return Response(
                {'error': 'Age must be a valid positive number'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if status_value not in [Pet.STATUS_AVAILABLE, Pet.STATUS_ADOPTED]:
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Make description and image nullable (empty string means null)
        final_description = description if description else None
        final_image = image if image else None

        pet = pet_service.create_pet(
            name=name,
            species=species,
            breed=breed,
            age=age,
            description=final_description,
            status=status_value,
            image=final_image
        )

        return Response({
            'message': 'Pet created successfully'
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PUT'])
def pet_update_api(request, pet_id):
    """Update an existing pet."""
    try:
        pet = get_object_or_404(Pet, id=pet_id)

        name = request.data.get('name', pet.name)
        species = request.data.get('species', pet.species)
        breed = request.data.get('breed', pet.breed)
        age_raw = request.data.get('age', pet.age)
        description = request.data.get('description', pet.description)
        status_value = request.data.get('status', pet.status)
        image = request.data.get('image', pet.image)

        # Handle string conversion safely
        name = name.strip() if isinstance(name, str) else str(name).strip()
        species = species.strip() if isinstance(species, str) else str(species).strip()
        breed = breed.strip() if isinstance(breed, str) else str(breed).strip()
        description = description.strip() if isinstance(description, str) else str(description).strip()
        image = image.strip() if isinstance(image, str) else str(image).strip()

        # Handle age conversion
        if isinstance(age_raw, str):
            age_str = age_raw.strip()
        else:
            age_str = str(age_raw)

        # Validation
        if not name or not species:
            return Response(
                {'error': 'Name and species are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            age = int(age_str)
            if age < 0:
                raise ValueError
        except ValueError:
            return Response(
                {'error': 'Age must be a valid positive number'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if status_value not in [Pet.STATUS_AVAILABLE, Pet.STATUS_ADOPTED]:
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Make description and image nullable
        final_description = description if description else None
        final_image = image if image else None

        updated_pet = pet_service.update_pet(
            pet_id=pet_id,
            name=name,
            species=species,
            breed=breed,
            age=age,
            description=final_description,
            status=status_value,
            image=final_image
        )

        return Response({
            'message': 'Pet updated successfully',
            'pet': {
                'id': updated_pet.id,
                'name': updated_pet.name,
                'species': updated_pet.species,
                'breed': updated_pet.breed,
                'age': updated_pet.age,
                'description': updated_pet.description,
                'status': updated_pet.status,
                'image': updated_pet.image,
            }
        }, status=status.HTTP_200_OK)

    except Pet.DoesNotExist:
        return Response(
            {'error': 'Pet not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
def pet_delete_api(request, pet_id):
    """Delete a pet."""
    try:
        pet = get_object_or_404(Pet, id=pet_id)
        pet_service.delete_pet(pet_id)
        return Response(
            {'message': 'Pet deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )

    except Pet.DoesNotExist:
        return Response(
            {'error': 'Pet not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def adopt_pet_api(request, pet_id):
    """Submit an adoption request for a pet."""
    try:
        pet = get_object_or_404(Pet, id=pet_id)
        adopter_name = request.data.get('adopter_name', '').strip()
        adopter_email = request.data.get('adopter_email', '').strip()

        if not adopter_name or not adopter_email:
            return Response(
                {'error': 'Adopter name and email are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create adoption request
        adoption_request = AdoptionRequest.objects.create(
            pet=pet,
            adopter_name=adopter_name,
            adopter_email=adopter_email
        )

        # Mark pet as adopted
        pet.status = Pet.STATUS_ADOPTED
        pet.save()

        return Response({
            'message': 'Adoption request submitted successfully',
            'adoption_request': {
                'id': adoption_request.id,
                'pet_id': adoption_request.pet.id,
                'pet_name': adoption_request.pet.name,
                'adopter_name': adoption_request.adopter_name,
                'adopter_email': adoption_request.adopter_email,
                'request_date': adoption_request.request_date,
            }
        }, status=status.HTTP_201_CREATED)

    except Pet.DoesNotExist:
        return Response(
            {'error': 'Pet not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )