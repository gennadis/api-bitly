import os
import json
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


def shorten_url(long_url: str) -> str:
    """Converts a long url to a Bitlink"""

    url = f"{BASE_URL}/shorten"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    }

    data = {
        "long_url": long_url,
        "domain": "bit.ly",
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()

    return response.json().get("id")


if __name__ == "__main__":
    # print(get_user_info())
    user_url = input("Enter full url to be shorten... ")
    print(shorten_url(user_url))
