"""Get data from etherscan.io
"""
import os
import json
import ssl

from dotenv import load_dotenv
from bs4 import BeautifulSoup


from utils.api_requests import get_request

import urllib
from urllib.request import urlopen

ETHERSCAN_KEY = os.getenv("ETHERSCAN_KEY")
# headers = {
#   'authority': 'etherscan.io',
#   'accept': '*/*',
#   'accept-language': 'en-US,en;q=0.9',
#   'cookie': '_ga=GA1.2.1477440426.1665183637; _gid=GA1.2.610671769.1665183637; __stripe_mid=4a6f445b-32d4-48b3-9f74-80977e8988c16c598f; __cuid=787cacc35023460b9716d23a13120277; ASP.NET_SessionId=rsk22rvfobajgibe5uhijwdq; amp_fef1e8=1ee808aa-e99a-4b06-90bf-7d7a5d8873e9R...1ges2gpju.1ges4fuku.5.1.6; __cf_bm=M90zS7smeYWG_9KLTEo2MSk_CV6Lmufg9fUBND7cf10-1665253622-0-ASc29YNxhmpgnTLyBDyh7CfIxXLEAuD6W8h+GCfIZxPigDPc4ELMwbiLvHRv+u+1m3XjzLLVYYCM2UZa159PD4p9LgPTHmEFJlPbCNmyKac2v4wUnrP2VaDRvHhGJTpA+A==',
#   'dnt': '1',
#   'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
#   'sec-ch-ua-mobile': '?0',
#   'sec-ch-ua-platform': '"macOS"',
#   'sec-fetch-dest': 'empty',
#   'sec-fetch-mode': 'cors',
#   'sec-fetch-site': 'same-origin',
#   'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
#   'x-requested-with': 'XMLHttpRequest'
# }

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