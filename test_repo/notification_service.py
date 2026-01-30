"""Notification Service."""
from test_repo.user import User
from test_repo.logger import get_logger

logger = get_logger("Notifier")

def send_welcome_email(user: User):
    logger.info(f"Sending welcome email to {user.email}")
    # Simulating email send
    pass

def send_order_confirmation(user: User, order_id: str):
    logger.info(f"Sending order confirmation {order_id} to {user.email}")