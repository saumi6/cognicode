"""Calculates final prices."""
from test_repo.cart_manager import CartManager
from test_repo.math_tools import apply_tax, calculate_discount
from test_repo.constants import SHIPPING_FEE

class PriceCalculator:
    def calculate_total(self, cart: CartManager, discount_percent: float = 0):
        subtotal = cart.get_subtotal()
        
        if discount_percent > 0:
            subtotal = calculate_discount(subtotal, discount_percent)
            
        total_with_tax = apply_tax(subtotal)
        
        shipping = 0 if cart.qualifies_for_free_shipping() else SHIPPING_FEE
        
        return total_with_tax + shipping