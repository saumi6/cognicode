"""Manages shopping carts."""
from typing import List, Dict
from test_repo.cart_item import CartItem
from test_repo.product import Product
from test_repo.user import User
from test_repo.constants import MAX_ITEMS_PER_CART, FREE_SHIPPING_THRESHOLD
from test_repo.exceptions import ValidationError

class CartManager:
    def __init__(self, user: User):
        self.user = user
        self.items: List[CartItem] = []
        
    def add_item(self, product: Product, qty: int = 1):
        current_count = sum(i.quantity for i in self.items)
        if current_count + qty > MAX_ITEMS_PER_CART:
            raise ValidationError("Cart is full")
            
        # Check if exists
        for item in self.items:
            if item.product.sku == product.sku:
                item.quantity += qty
                return
        
        self.items.append(CartItem(product, qty))
        
    def get_subtotal(self) -> float:
        return sum(item.get_total_price() for item in self.items)
        
    def qualifies_for_free_shipping(self) -> bool:
        return self.get_subtotal() > FREE_SHIPPING_THRESHOLD