import os
import urllib
import requests
import argparse

from dotenv import load_dotenv


BASE_URL = "https://api-ssl.bitly.com"
ENDPOINTS = {
    "shorten": "/v4/shorten",
    "clicks": "/v4/bitlinks/{}/clicks/summary",  # bitlink
    "is_bitlink": "/v4/bitlinks/{}",  # bitlink
}


def shorten_link(token: str, base_url: str, endpoint: str, link: str) -> str:
    """Converts a long url to a Bitlink"""

    url = f"{base_url}{endpoint}"
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

    url = f"{base_url}{endpoint.format(bitlink)}"
    headers = {
        "Authorization": f"Bearer {token}",
    }

    response = requests.get(url=url, headers=headers)
    response.raise_for_status()
    clicks: int = response.json().get("total_clicks")

    return clicks


def is_bitlink(token: str, base_url: str, endpoint: str, link: str) -> bool:
    """Check if URL is a Bitlink"""

    parsed_link = urllib.parse.urlparse(link)
    bitlink = f"{parsed_link.netloc}{parsed_link.path}"

    url = f"{base_url}{endpoint.format(bitlink)}"
    headers = {
        "Authorization": f"Bearer {token}",
    }

    response = requests.get(url=url, headers=headers)

    return response.ok


def main():
    load_dotenv()
    token = os.environ.get("BITLY_TOKEN")

    parser = argparse.ArgumentParser()
    parser.add_argument("link", help="enter link to shorten or to get clicks count of")

    args = parser.parse_args()
    user_link = args.link

    if is_bitlink(token, BASE_URL, ENDPOINTS["is_bitlink"], user_link):
        try:
            count = count_clicks(token, BASE_URL, ENDPOINTS["clicks"], user_link)
        except requests.exceptions.HTTPError as e:
            print(f"Bitlink validation error - {e}")
        else:
            print("Click counts:", count)
    else:
        try:
            bitlink = shorten_link(token, BASE_URL, ENDPOINTS["shorten"], user_link)
        except requests.exceptions.HTTPError as e:
            print(f"URL validation error - {e}")
        else:
            print("Bitlink:", bitlink)


if __name__ == "__main__":
    main()
