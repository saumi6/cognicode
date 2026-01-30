"""Custom exceptions for the system."""

class ValidationError(Exception):
    """Raised when data validation fails."""
    pass

class InventoryError(Exception):
    """Raised when inventory operations fail."""
    pass

class AuthenticationError(Exception):
    """Raised when authentication fails."""
    pass

class PaymentError(Exception):
    """Raised when payment processing fails."""
    pass