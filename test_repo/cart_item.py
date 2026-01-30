"""Cart Item entity."""
from test_repo.product import Product
from test_repo.math_tools import round_currency

class CartItem:
    def __init__(self, product: Product, quantity: int = 1):
        self.product = product
        self.quantity = quantity
        
    def get_total_price(self) -> float:
        return round_currency(self.product.price * self.quantity)
        
    def increment(self):
        self.quantity += 1
        
    def decrement(self):
        if self.quantity > 0:
            self.quantity -= 1