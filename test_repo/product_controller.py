"""Product API Controller."""
from typing import List
from test_repo.inventory_manager import InventoryManager
from test_repo.recommendation_engine import RecommendationEngine
from test_repo.product import Product

class ProductController:
    def __init__(self):
        self.inventory = InventoryManager()
        self.recommender = RecommendationEngine(self.inventory)
        
    def create_product(self, name: str, price: float, category: str):
        p = Product(name, price, category)
        self.inventory.add_product(p)
        return p.sku
        
    def get_recommendations(self, user_id: str) -> List[str]:
        # Using a fake user here for simplicity or would need User service look up
        from test_repo.user import User
        dummy_user = User("Guest", "guest@example.com") 
        products = self.recommender.suggest_products(dummy_user)
        return [p.name for p in products]