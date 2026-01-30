"""User entity."""
from typing import List, Optional
from test_repo.address import Address
from test_repo.string_tools import sanitize_email
from test_repo.id_generator import generate_uuid
from test_repo.exceptions import ValidationError

class User:
    def __init__(self, name: str, email: str):
        self.id = generate_uuid()
        self.name = name
        self.email = sanitize_email(email)
        self.addresses: List[Address] = []
        self.is_active = True
        
    def add_address(self, address: Address):
        self.addresses.append(address)
        
    def get_primary_address(self) -> Optional[Address]:
        return self.addresses[0] if self.addresses else None
        
    def deactivate(self):
        self.is_active = False