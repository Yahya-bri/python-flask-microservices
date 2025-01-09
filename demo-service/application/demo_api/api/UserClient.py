# application/order_api/api/UserClient.py
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class UserClient:
    @staticmethod
    def get_user(api_key):
        headers = {
            'Authorization': api_key
        }
        api_url = os.getenv('API_URL', 'http://localhost:5001')
        response = requests.request(method="GET", url=f'{api_url}/api/user', headers=headers)

        if response.status_code == 401:
            return False
        
        try:
            user = response.json()
        except requests.exceptions.JSONDecodeError:
            return None
        
        return user
