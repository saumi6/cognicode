"""Main Application Entry Point."""
from test_repo.user_controller import UserController
from test_repo.product_controller import ProductController
from test_repo.order_processor import OrderProcessor
from test_repo.cart_manager import CartManager
from test_repo.payment_method import CreditCard

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