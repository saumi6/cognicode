"""Recommendation Engine."""
from typing import List
from test_repo.user import User
from test_repo.product import Product
from test_repo.inventory_manager import InventoryManager

class RecommendationEngine:
    def __init__(self, inventory: InventoryManager):
        self.inventory = inventory
        
    def suggest_products(self, user: User) -> List[Product]:
        # Dumb algorithm: return first 3 available products
        available = []
        for p in self.inventory.products.values():
            if p.stock > 0:
                available.append(p)
            if len(available) >= 3:
                break
        return available