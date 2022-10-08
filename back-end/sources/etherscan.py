"""Get data from etherscan.io
"""
import os
import ssl

import urllib
from bs4 import BeautifulSoup

from utils.api_requests import get_request


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
    url = f"{base_url}address/{address}"

    headers_urllib = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0'}
    req = urllib.request.Request(url, method="GET", headers=headers_urllib)
    gcontext = ssl.SSLContext()
    r = urllib.request.urlopen(req, context=gcontext)
    data = r.read()
    try:
        soup = BeautifulSoup(data, "html.parser")
        # print(soup)
        audit_reports = soup.find("div", {"id": "auditReportId"})
        if "No Contract Security Audit Submitted" in audit_reports.text:
            return False
        else:
            return True
    except:
        print(f"contract search not found for {url}")
        return False

if __name__ == "__main__":
    print(ETHERSCAN_KEY)
    print(is_verified("0x984e7B3f332a2a6Fc1EB73B5B8F8E95D24ee2097"))
    print(is_verified("0x984e7B3f332a2a6Fc1EB73B5B8F8E95D24ee2097", chain="goerli"))

    print(is_audited("0x984e7B3f332a2a6Fc1EB73B5B8F8E95D24ee2097"))