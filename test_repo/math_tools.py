"""Mathematical utilities."""
import math
from test_repo.constants import TAX_RATE

def apply_tax(amount: float) -> float:
    """Calculate total with tax."""
    return round(amount * (1 + TAX_RATE), 2)
#test 
def calculate_discount(price: float, discount_percent: float) -> float:
    """Calculate discounted price."""
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Invalid discount")
    factor = 1 - (discount_percent / 100)
    return round(price * factor, 2)

def round_currency(amount: float) -> float:
    """Round to 2 decimal places."""
    return round(amount, 2)

#test