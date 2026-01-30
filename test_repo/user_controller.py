"""User API Controller.""" 
from test_repo.user_service import UserService
from test_repo.auth_service import AuthService

class UserController:
    def __init__(self):
        self.user_svc = UserService()
        self.auth_svc = AuthService(self.user_svc)
        
    def signup(self, name: str, email: str):
        return self.user_svc.register(name, email)
        
    def login(self, email: str):
        return self.auth_svc.login(email)