import requests

def get_user_data(user_id: int) -> dict:
    """Fetch user data from external API"""
    response = requests.get(f"https://api.example.com/users/{user_id}")
    if response.status_code == 200:
        return response.json()
    raise ValueError("User not found")
