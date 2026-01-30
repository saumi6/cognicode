"""Address entity."""
from typing import Dict
from test_repo.string_tools import slugify
from test_repo.exceptions import ValidationError

class Address:
    def __init__(self, street: str, city: str, zip_code: str):
        if not zip_code:
            raise ValidationError("Zip code required")
        self.street = street
        self.city = city
        self.zip_code = zip_code
        
    def to_string(self) -> str:
        return f"{self.street}, {self.city} {self.zip_code}"
        
    def to_dict(self) -> Dict[str, str]:
        return {
            "street": self.street,
            "city": self.city,
            "zip": self.zip_code,
            "slug": slugify(self.city)
        }