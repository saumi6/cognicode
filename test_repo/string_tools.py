"""String manipulation utilities."""
import re
from test_repo.exceptions import ValidationError

def slugify(text: str) -> str:
    """Convert text to a slug."""
    if not text:
        return ""
    text = text.lower().strip()
    return re.sub(r'[^a-z0-9]+', '-', text).strip('-')

def sanitize_email(email: str) -> str:
    """Lowercase and strip email."""
    if not email:
        raise ValidationError("Email cannot be empty")
    return email.strip().lower()

def mask_card_number(card_num: str) -> str:
    """Mask all but last 4 digits."""
    if len(card_num) < 4:
        return card_num
    return "*" * (len(card_num) - 4) + card_num[-4:]