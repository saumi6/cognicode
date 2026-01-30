"""Authentication service."""
from test_repo.user_service import UserService
from test_repo.exceptions import AuthenticationError
from test_repo.id_generator import generate_uuid

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