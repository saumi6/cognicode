"""Checkout Controller."""
from test_repo.cart_manager import CartManager
from test_repo.price_calculator import PriceCalculator
from test_repo.payment_method import CreditCard
from test_repo.exceptions import PaymentError, ValidationError

class CheckoutController:
    def __init__(self):
        self.calc = PriceCalculator()
        
    def process_checkout(self, cart: CartManager, card: CreditCard):
        if not cart.items:
            raise ValidationError("Cart is empty")
            
        if not card.is_valid():
            raise PaymentError("Invalid card")
            
        total = self.calc.calculate_total(cart)
        
        # Simulate charging
        print(f"Charged {total} to card ending in {card.display_number()[-4:]}")
        return True