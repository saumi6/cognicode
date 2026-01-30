import os
from pathlib import Path

# Base directory for the test repository
BASE_DIR = Path(r"C:\Users\gurav\prog\college\BE Proj\cognicode\test_repo")
BASE_DIR.mkdir(parents=True, exist_ok=True)

# Define file contents
files = {}

# --- Layer 1: Utils (7 files) ---

files["constants.py"] = """
\"\"\"System-wide constants.\"\"\"

TAX_RATE = 0.08
SHIPPING_FEE = 5.99
FREE_SHIPPING_THRESHOLD = 50.00
MAX_ITEMS_PER_CART = 20
CURRENCY = "USD"
ADMIN_EMAIL = "admin@example.com"
"""

files["exceptions.py"] = """
\"\"\"Custom exceptions for the system.\"\"\"

class ValidationError(Exception):
    \"\"\"Raised when data validation fails.\"\"\"
    pass

class InventoryError(Exception):
    \"\"\"Raised when inventory operations fail.\"\"\"
    pass

class AuthenticationError(Exception):
    \"\"\"Raised when authentication fails.\"\"\"
    pass

class PaymentError(Exception):
    \"\"\"Raised when payment processing fails.\"\"\"
    pass
"""

files["string_tools.py"] = """
\"\"\"String manipulation utilities.\"\"\"
import re
from .exceptions import ValidationError

def slugify(text: str) -> str:
    \"\"\"Convert text to a slug.\"\"\"
    if not text:
        return ""
    text = text.lower().strip()
    return re.sub(r'[^a-z0-9]+', '-', text).strip('-')

def sanitize_email(email: str) -> str:
    \"\"\"Lowercase and strip email.\"\"\"
    if not email:
        raise ValidationError("Email cannot be empty")
    return email.strip().lower()

def mask_card_number(card_num: str) -> str:
    \"\"\"Mask all but last 4 digits.\"\"\"
    if len(card_num) < 4:
        return card_num
    return "*" * (len(card_num) - 4) + card_num[-4:]
"""

files["math_tools.py"] = """
\"\"\"Mathematical utilities.\"\"\"
import math
from .constants import TAX_RATE

def apply_tax(amount: float) -> float:
    \"\"\"Calculate total with tax.\"\"\"
    return round(amount * (1 + TAX_RATE), 2)

def calculate_discount(price: float, discount_percent: float) -> float:
    \"\"\"Calculate discounted price.\"\"\"
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Invalid discount")
    factor = 1 - (discount_percent / 100)
    return round(price * factor, 2)

def round_currency(amount: float) -> float:
    \"\"\"Round to 2 decimal places.\"\"\"
    return round(amount, 2)
"""

files["date_utils.py"] = """
\"\"\"Date and time utilities.\"\"\"
from datetime import datetime, timedelta

def get_current_timestamp() -> str:
    \"\"\"Return ISO format timestamp.\"\"\"
    return datetime.utcnow().isoformat()

def is_expired(expiry_date_str: str) -> bool:
    \"\"\"Check if a date string is in the past.\"\"\"
    try:
        exp = datetime.fromisoformat(expiry_date_str)
        return exp < datetime.utcnow()
    except ValueError:
        return True

def add_days(date_str: str, days: int) -> str:
    \"\"\"Add days to an ISO date string.\"\"\"
    dt = datetime.fromisoformat(date_str)
    return (dt + timedelta(days=days)).isoformat()
"""

files["id_generator.py"] = """
\"\"\"ID generation utilities.\"\"\"
import uuid
import random
import string

def generate_uuid() -> str:
    \"\"\"Generate a robust UUID.\"\"\"
    return str(uuid.uuid4())

def generate_order_id() -> str:
    \"\"\"Generate a human-readable order ID order-XXXX.\"\"\"
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"ORD-{suffix}"

def generate_sku(category: str, name: str) -> str:
    \"\"\"Generate SKU from category and name.\"\"\"
    prefix = category[:3].upper()
    suffix = name[:3].upper()
    num = random.randint(100, 999)
    return f"{prefix}-{suffix}-{num}"
"""

files["logger.py"] = """
\"\"\"Deeply complex logging system (fake).\"\"\"
from .date_utils import get_current_timestamp

class Logger:
    def __init__(self, name: str):
        self.name = name
    
    def info(self, message: str):
        ts = get_current_timestamp()
        print(f"[INFO] {ts} [{self.name}]: {message}")
        
    def error(self, message: str):
        ts = get_current_timestamp()
        print(f"[ERROR] {ts} [{self.name}]: {message}")

def get_logger(name: str) -> Logger:
    return Logger(name)
"""


# --- Layer 2: Entities (5 files) ---

files["address.py"] = """
\"\"\"Address entity.\"\"\"
from typing import Dict
from .string_tools import slugify
from .exceptions import ValidationError

class Address:
    def __init__(self, street: str, city: str, zip_code: str):
        if not zip_code:
            raise ValidationError("Zip code required")
        self.street = street
        self.city = city
        self.zip_code = zip_code
        
    def to_string(self) -> str:
        return f"{self.street}, {self.city} {self.zip_code}"
        
    def to_dict(self) -> Dict[str, str]:
        return {
            "street": self.street,
            "city": self.city,
            "zip": self.zip_code,
            "slug": slugify(self.city)
        }
"""

files["product.py"] = """
\"\"\"Product entity.\"\"\"
from typing import Optional
from .math_tools import round_currency
from .id_generator import generate_sku
from .exceptions import ValidationError

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
"""

files["user.py"] = """
\"\"\"User entity.\"\"\"
from typing import List, Optional
from .address import Address
from .string_tools import sanitize_email
from .id_generator import generate_uuid
from .exceptions import ValidationError

class User:
    def __init__(self, name: str, email: str):
        self.id = generate_uuid()
        self.name = name
        self.email = sanitize_email(email)
        self.addresses: List[Address] = []
        self.is_active = True
        
    def add_address(self, address: Address):
        self.addresses.append(address)
        
    def get_primary_address(self) -> Optional[Address]:
        return self.addresses[0] if self.addresses else None
        
    def deactivate(self):
        self.is_active = False
"""

files["cart_item.py"] = """
\"\"\"Cart Item entity.\"\"\"
from .product import Product
from .math_tools import round_currency

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
"""

files["payment_method.py"] = """
\"\"\"Payment Method entity.\"\"\"
from .string_tools import mask_card_number
from .date_utils import is_expired

class CreditCard:
    def __init__(self, number: str, expiry: str, cvv: str):
        self.number = number
        self.expiry = expiry  # ISO date string for simplicity
        self.cvv = cvv
        
    def is_valid(self) -> bool:
        return not is_expired(self.expiry) and len(self.cvv) in (3, 4)
        
    def display_number(self) -> str:
        return mask_card_number(self.number)
"""


# --- Layer 3: Logic/Services (7 files) ---

files["inventory_manager.py"] = """
\"\"\"Manages product inventory.\"\"\"
from typing import Dict, List
from .product import Product
from .exceptions import InventoryError
from .logger import get_logger

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
"""

files["cart_manager.py"] = """
\"\"\"Manages shopping carts.\"\"\"
from typing import List, Dict
from .cart_item import CartItem
from .product import Product
from .user import User
from .constants import MAX_ITEMS_PER_CART, FREE_SHIPPING_THRESHOLD
from .exceptions import ValidationError

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
"""

files["price_calculator.py"] = """
\"\"\"Calculates final prices.\"\"\"
from .cart_manager import CartManager
from .math_tools import apply_tax, calculate_discount
from .constants import SHRIPPING_FEE

class PriceCalculator:
    def calculate_total(self, cart: CartManager, discount_percent: float = 0):
        subtotal = cart.get_subtotal()
        
        if discount_percent > 0:
            subtotal = calculate_discount(subtotal, discount_percent)
            
        total_with_tax = apply_tax(subtotal)
        
        shipping = 0 if cart.qualifies_for_free_shipping() else SHRIPPING_FEE
        
        return total_with_tax + shipping
"""

files["user_service.py"] = """
\"\"\"User management service.\"\"\"
from typing import Dict
from .user import User
from .exceptions import ValidationError
from .logger import get_logger

logger = get_logger("UserService")

class UserService:
    def __init__(self):
        self.users: Dict[str, User] = {}
        
    def register(self, name: str, email: str) -> User:
        for u in self.users.values():
            if u.email == email:
                raise ValidationError("Email taken")
                
        user = User(name, email)
        self.users[user.id] = user
        logger.info(f"User registered: {email}")
        return user
        
    def get_user(self, user_id: str) -> User:
        return self.users.get(user_id)
"""

files["auth_service.py"] = """
\"\"\"Authentication service.\"\"\"
from .user_service import UserService
from .exceptions import AuthenticationError
from .id_generator import generate_uuid

# Simulating a session store
sessions = {}

class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service
        
    def login(self, email: str) -> str:
        # Fake login - just checks existence
        for u in self.user_service.users.values():
            if u.email == email:
                token = generate_uuid()
                sessions[token] = u.id
                return token
        raise AuthenticationError("User not found")
        
    def get_current_user(self, token: str):
        user_id = sessions.get(token)
        if not user_id:
            raise AuthenticationError("Invalid token")
        return self.user_service.get_user(user_id)
"""

files["notification_service.py"] = """
\"\"\"Notification Service.\"\"\"
from .user import User
from .logger import get_logger

logger = get_logger("Notifier")

def send_welcome_email(user: User):
    logger.info(f"Sending welcome email to {user.email}")
    # Simulating email send
    pass

def send_order_confirmation(user: User, order_id: str):
    logger.info(f"Sending order confirmation {order_id} to {user.email}")
"""

files["recommendation_engine.py"] = """
\"\"\"Recommendation Engine.\"\"\"
from typing import List
from .user import User
from .product import Product
from .inventory_manager import InventoryManager

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
"""


# --- Layer 4: Controllers/Main (6 files) ---

files["checkout_controller.py"] = """
\"\"\"Checkout Controller.\"\"\"
from .cart_manager import CartManager
from .price_calculator import PriceCalculator
from .payment_method import CreditCard
from .exceptions import PaymentError, ValidationError

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
"""

files["product_controller.py"] = """
\"\"\"Product API Controller.\"\"\"
from typing import List
from .inventory_manager import InventoryManager
from .recommendation_engine import RecommendationEngine
from .product import Product

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
        from .user import User
        dummy_user = User("Guest", "guest@example.com") 
        products = self.recommender.suggest_products(dummy_user)
        return [p.name for p in products]
"""

files["user_controller.py"] = """
\"\"\"User API Controller.\"\"\"
from .user_service import UserService
from .auth_service import AuthService

class UserController:
    def __init__(self):
        self.user_svc = UserService()
        self.auth_svc = AuthService(self.user_svc)
        
    def signup(self, name: str, email: str):
        return self.user_svc.register(name, email)
        
    def login(self, email: str):
        return self.auth_svc.login(email)
"""

files["order_processor.py"] = """
\"\"\"Order Processor.\"\"\"
from .checkout_controller import CheckoutController
from .notification_service import send_order_confirmation
from .id_generator import generate_order_id
from .cart_manager import CartManager
from .payment_method import CreditCard

class OrderProcessor:
    def place_order(self, cart: CartManager, card: CreditCard):
        checkout = CheckoutController()
        if checkout.process_checkout(cart, card):
            order_id = generate_order_id()
            send_order_confirmation(cart.user, order_id)
            return order_id
        return None
"""

files["report_generator.py"] = """
\"\"\"Report Generator.\"\"\"
from  typing import List
from .inventory_manager import InventoryManager
from .date_utils import get_current_timestamp

def generate_inventory_report(inventory: InventoryManager) -> str:
    lines = [f"Inventory Report - {get_current_timestamp()}"]
    for sku, prod in inventory.products.items():
        lines.append(f"{sku}: {prod.name} - Stock: {prod.stock}")
    return "\\n".join(lines)
"""

files["main_app.py"] = """
\"\"\"Main Application Entry Point.\"\"\"
from .user_controller import UserController
from .product_controller import ProductController
from .order_processor import OrderProcessor
from .cart_manager import CartManager
from .payment_method import CreditCard

def main():
    print("Starting E-Commerce System...")
    
    # Setup
    user_ctrl = UserController()
    prod_ctrl = ProductController()
    order_proc = OrderProcessor()
    
    # Flow
    u1 = user_ctrl.signup("Alice", "alice@example.com")
    token = user_ctrl.login("alice@example.com")
    
    sku = prod_ctrl.create_product("Laptop", 1200.00, "Electronics")
    prod_ctrl.inventory.restock(sku, 5)
    
    product = prod_ctrl.inventory.products[sku]
    cart = CartManager(u1)
    cart.add_item(product, 1)
    
    card = CreditCard("1234567812345678", "2030-01-01", "123")
    
    order_id = order_proc.place_order(cart, card)
    print(f"Order placed: {order_id}")

if __name__ == "__main__":
    main()
"""

files["__init__.py"] = ""

# Write all files
for filename, content in files.items():
    file_path = BASE_DIR / filename
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"Created {filename}")

print(f"Successfully created {len(files)} files in {BASE_DIR}")
