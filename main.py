import os
import json
import urllib
import requests
from dotenv import load_dotenv


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


def count_clicks(token: str, bitlink: str) -> int:
    """Returns the click counts for a Bitlink"""

    endpoint = f"{BASE_URL}/bitlinks/{bitlink}/clicks/summary"
    headers = {
        "Authorization": f"Bearer {token}",
    }

    response = requests.get(url=endpoint, headers=headers)
    response.raise_for_status()
    clicks: int = response.json().get("total_clicks")

    return clicks


def is_bitlink(url: str) -> bool:
    """Check if URL is a Bitlink"""

    parsed_url = urllib.parse.urlparse(url)
    bitlink = f"{parsed_url.netloc}{parsed_url.path}"
    endpoint = f"{BASE_URL}/bitlinks/{bitlink}"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
    }

    response = requests.get(url=endpoint, headers=headers)

    return response.ok


if __name__ == "__main__":

    load_dotenv()
    TOKEN = os.environ.get("BITLY_TOKEN")
    BASE_URL = "https://api-ssl.bitly.com/v4"

    user_url = input("Please enter your URL: ")
    if is_bitlink(user_url):
        try:
            count = count_clicks(TOKEN, user_url)
        except requests.exceptions.HTTPError as e:
            print(f"Bitlink validation error - {e}")
        else:
            print("Click counts:", count)
    else:
        try:
            bitlink = shorten_link(TOKEN, user_url)
        except requests.exceptions.HTTPError as e:
            print(f"URL validation error - {e}")
        else:
            print("Bitlink:", bitlink)
