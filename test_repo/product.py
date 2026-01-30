"""Product entity."""
from typing import Optional
from test_repo.math_tools import round_currency
from test_repo.id_generator import generate_sku
from test_repo.exceptions import ValidationError

class Product:
    def __init__(self, name: str, price: float, category: str = "General"):
        if price < 0:
            raise ValidationError("Price cannot be negative")
        self.name = name
        self.price = round_currency(price)
        self.category = category
        self.sku = generate_sku(category, name)
        self.stock = 0
        
    def update_price(self, new_price: float):
        if new_price < 0:
            raise ValidationError("Price cannot be negative")
        self.price = round_currency(new_price)
        
    def add_stock(self, qty: int):
        self.stock += qty
        
    def remove_stock(self, qty: int):
        if self.stock < qty:
            raise ValueError("Not enough stock")
        self.stock -= qty