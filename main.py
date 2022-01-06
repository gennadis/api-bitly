import os
import urllib
import requests
from dotenv import load_dotenv


BASE_URL = "https://api-ssl.bitly.com"
ENDPOINTS = {
    "shorten": "/v4/shorten",
    "clicks": "/v4/bitlinks/{}/clicks/summary",  # bitlink
    "is_bitlink": "/v4/bitlinks/{}",  # bitlink
}


def shorten_link(token: str, base_url: str, endpoint: str, link: str) -> str:
    """Converts a long url to a Bitlink"""

    url = base_url + endpoint
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    data = {
        "long_url": link,
        "domain": "bit.ly",
    }

    response = requests.post(url=url, headers=headers, json=data)
    response.raise_for_status()
    bitlink = response.json().get("id")

    return bitlink


def count_clicks(token: str, base_url: str, endpoint: str, bitlink: str) -> int:
    """Returns the click counts for a Bitlink"""

    url = base_url + endpoint.format(bitlink)
    headers = {
        "Authorization": f"Bearer {token}",
    }

    response = requests.get(url=url, headers=headers)
    response.raise_for_status()
    clicks: int = response.json().get("total_clicks")

    return clicks


def is_bitlink(base_url: str, endpoint: str, link: str) -> bool:
    """Check if URL is a Bitlink"""

    parsed_link = urllib.parse.urlparse(link)
    bitlink = parsed_link.netloc + parsed_link.path

    url = base_url + endpoint.format(bitlink)
    headers = {
        "Authorization": f"Bearer {TOKEN}",
    }

    response = requests.get(url=url, headers=headers)

    return response.ok


def main():

    load_dotenv()
    TOKEN = os.environ.get("BITLY_TOKEN")

    user_link = input("Please enter your URL: ")
    if is_bitlink(BASE_URL, ENDPOINTS["is_bitlink"], user_link):
        try:
            count = count_clicks(TOKEN, BASE_URL, ENDPOINTS["clicks"], user_link)
        except requests.exceptions.HTTPError as e:
            print(f"Bitlink validation error - {e}")
        else:
            print("Click counts:", count)
    else:
        try:
            bitlink = shorten_link(TOKEN, BASE_URL, ENDPOINTS["shorten"], user_link)
        except requests.exceptions.HTTPError as e:
            print(f"URL validation error - {e}")
        else:
            print("Bitlink:", bitlink)


if __name__ == "__main__":
    main()
