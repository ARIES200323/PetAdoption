
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


class RequestValidationError(ValueError):
    """Raised when incoming request data fails validation."""


@dataclass
class PetAdoptionRequestPattern:
    pet_id: int
    adopter_name: str
    adopter_email: str

    @classmethod
    def from_payload(cls, pet_id: int, payload: Dict[str, Any]) -> "PetAdoptionRequestPattern":
        adopter_name = str(payload.get("adopter_name", "")).strip()
        adopter_email = str(payload.get("adopter_email", "")).strip()

        return cls(
            pet_id=pet_id,
            adopter_name=adopter_name,
            adopter_email=adopter_email,
        )

    def validate(self) -> None:
        if self.pet_id <= 0:
            raise RequestValidationError("pet_id must be a positive integer.")

        if not self.adopter_name:
            raise RequestValidationError("adopter_name is required.")

        if not self.adopter_email:
            raise RequestValidationError("adopter_email is required.")
