import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ.get("TOKEN")

BASE_URL = "https://api-ssl.bitly.com/v4"


def get_user_info() -> dict:
    """Returns information for the current authenticated user"""

    url = f"{BASE_URL}/user"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
    }

    response = requests.get(url=url, headers=headers)
    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    print(get_user_info())
