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
    bitlink = response.json().get("id")

    return bitlink


if __name__ == "__main__":
    user_url = input("Enter full URL (like http://google.com) to be shorten... ")
    try:
        bitlink = shorten_link(TOKEN, user_url)
    except requests.exceptions.HTTPError as e:
        print(f"URL validation error - {e}")
    else:
        print("Битлинк", bitlink)
