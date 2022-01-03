import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ.get("TOKEN")

BASE_URL = "https://api-ssl.bitly.com/v4"


def get_user_info() -> dict:
    """Returns information for the current authenticated user"""

    endpoint = f"{BASE_URL}/user"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
    }

    response = requests.get(url=endpoint, headers=headers)
    response.raise_for_status()

    return response.json()


def shorten_link(token: str, url: str) -> str:
    """Converts a long url to a Bitlink"""

    endpoint = f"{BASE_URL}/shorten"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    data = {
        "long_url": url,
        "domain": "bit.ly",
    }

    response = requests.post(url=endpoint, headers=headers, data=json.dumps(data))
    response.raise_for_status()

    return response.json().get("id")


if __name__ == "__main__":
    user_url = input("Enter full url to be shorten... ")
    print("Битлинк", shorten_link(TOKEN, user_url))
