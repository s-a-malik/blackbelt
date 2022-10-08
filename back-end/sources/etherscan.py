"""Get data from etherscan.io
"""

from utils.api_requests import get_request
# import pandas as pd
# from pandas import json_normalize
import os
from dotenv import load_dotenv

load_dotenv()   # load .env file
ETHERSCAN_KEY = os.getenv("ETHERSCAN_KEY")


def _make_base_etherscan_url(chain="mainnet"):
    if chain == "mainnet":
        base_url = "https://api.etherscan.io/api"
    elif chain == "ropsten":
        base_url = "https://api-ropsten.etherscan.io/api"
    elif chain == "goerli":
        base_url = "https://api-goerli.etherscan.io/api"
    else:
        raise ValueError(f"Chain {chain} not supported")
    return base_url


def is_verified(address, chain="mainnet"):
    # construct the request
    base_url = _make_base_etherscan_url(chain)
    params = {
        "module": "contract",
        "action": "getabi",
        "address": address,
        "apikey": ETHERSCAN_KEY
    }
    response = get_request(base_url, params=params)
    response = response.json()
    verified = True if response["status"] == "1" else False

    return verified


def is_audited(address, chain="mainnet"):
    raise(NotImplementedError)


if __name__ == "__main__":
    print(ETHERSCAN_KEY)
    print(is_verified("0x984e7B3f332a2a6Fc1EB73B5B8F8E95D24ee2097"))
    print(is_verified("0x984e7B3f332a2a6Fc1EB73B5B8F8E95D24ee2097", chain="goerl"))
