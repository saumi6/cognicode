"""Payment Method entity."""
from test_repo.string_tools import mask_card_number
from test_repo.date_utils import is_expired

class CreditCard:
    def __init__(self, number: str, expiry: str, cvv: str):
        self.number = number
        self.expiry = expiry  # ISO date string for simplicity
        self.cvv = cvv
        
    def is_valid(self) -> bool:
        return not is_expired(self.expiry) and len(self.cvv) in (3, 4)
        
    def display_number(self) -> str:
        return mask_card_number(self.number)