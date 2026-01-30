"""Order Processor."""
from test_repo.checkout_controller import CheckoutController
from test_repo.notification_service import send_order_confirmation
from test_repo.id_generator import generate_order_id
from test_repo.cart_manager import CartManager
from test_repo.payment_method import CreditCard

class OrderProcessor:
    def place_order(self, cart: CartManager, card: CreditCard):
        checkout = CheckoutController()
        if checkout.process_checkout(cart, card):
            order_id = generate_order_id()
            send_order_confirmation(cart.user, order_id)
            return order_id
        return None