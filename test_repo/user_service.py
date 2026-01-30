"""User management service."""
from typing import Dict
from test_repo.user import User
from test_repo.exceptions import ValidationError
from test_repo.logger import get_logger

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