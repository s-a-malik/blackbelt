"""Get data from etherscan.io
"""
import os
import json

from dotenv import load_dotenv
from bs4 import BeautifulSoup

from utils.api_requests import get_request


load_dotenv()   # load .env file
ETHERSCAN_KEY = os.getenv("ETHERSCAN_KEY")


def _make_base_etherscan_url(chain="mainnet", url_type="api"):
    if chain == "mainnet":
        return "https://etherscan.io/" if url_type == "base" else "https://api.etherscan.io/api"
    else:
        if url_type == "base":
            base_url = f"https://{chain}.etherscan.io/"
        elif url_type == "api":
            base_url = f"https://api-{chain}.etherscan.io/api"
    return base_url


def is_verified(address, chain="mainnet"):
    # construct the request
    base_url = _make_base_etherscan_url(chain, url_type="api")
    params = {
        "module": "contract",
        "action": "getabi",
        "address": address,
        "apikey": ETHERSCAN_KEY
    }
    response = get_request(base_url, params=params, headers=None)
    response = response.json()
    verified = True if response["status"] == "1" else False

    return verified


def is_audited(address, chain="mainnet"):
    # construct the url
    base_url = _make_base_etherscan_url(chain, url_type="base")
    url = f"{base_url}address/{address}#code"
    # parse the html
    page = get_request(url, headers={})

    soup = BeautifulSoup(page.content, "lxml")
    # extract the json
    # x = soup.find('script', type='application/json').string
    # data = json.loads(x)

    pass


if __name__ == "__main__":
    print(ETHERSCAN_KEY)
    print(is_verified("0x984e7B3f332a2a6Fc1EB73B5B8F8E95D24ee2097"))
    print(is_verified("0x984e7B3f332a2a6Fc1EB73B5B8F8E95D24ee2097", chain="goerl"))
