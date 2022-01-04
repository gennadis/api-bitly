import os
import json
import urllib
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ.get("BITLY_TOKEN")
BASE_URL = "https://api-ssl.bitly.com"
ENDPOINTS = {
    "shorten": "/v4/shorten",
    "clicks": "/v4/bitlinks/{}/clicks/summary",  # bitlink
    "is_bitlink": "/v4/bitlinks/{}",  # bitlink
}


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


def main():
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


if __name__ == "__main__":
    main()
