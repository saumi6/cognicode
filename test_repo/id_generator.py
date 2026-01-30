"""ID generation utilities."""
import uuid
import random
import string

def generate_uuid() -> str:
    """Generate a robust UUID."""
    return str(uuid.uuid4())

def generate_order_id() -> str:
    """Generate a human-readable order ID order-XXXX."""
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"ORD-{suffix}"

def generate_sku(category: str, name: str) -> str:
    """Generate SKU from category and name."""
    prefix = category[:3].upper()
    suffix = name[:3].upper()
    num = random.randint(100, 999)
    return f"{prefix}-{suffix}-{num}"