"""Manages product inventory."""
from typing import Dict, List
from test_repo.product import Product
from test_repo.exceptions import InventoryError
from test_repo.logger import get_logger

logger = get_logger("InventoryManager")

class InventoryManager:
    def __init__(self):
        self.products: Dict[str, Product] = {}
        
    def add_product(self, product: Product):
        if product.sku in self.products:
            raise InventoryError(f"Product {product.sku} already exists")
        self.products[product.sku] = product
        logger.info(f"Added product {product.name}")
        
    def check_stock(self, sku: str, qty: int) -> bool:
        product = self.products.get(sku)
        if not product:
            return False
        return product.stock >= qty
        
    def restock(self, sku: str, qty: int):
        product = self.products.get(sku)
        if product:
            product.add_stock(qty)
            logger.info(f"Restocked {sku} by {qty}")