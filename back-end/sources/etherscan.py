"""Get data from etherscan.io
"""

import requests
# import pandas as pd
# from pandas import json_normalize
import os
from dotenv import load_dotenv

load_dotenv()   # load .env file
ETHERSCAN_KEY = os.getenv("ETHERSCAN_KEY")

#Simple query function
def query(url):
    """
    Returns api result
    @params:
        url       - Required  : api url
    """  
    request = requests.get(url)
    if request.status_code == 200:
        return request.json()
    else:
        return ('Query failed and return code is {}.      {}'.format(request.status_code, query))

#Query etherscan
def get_transactions(address, tx_view = 'ERC20'):
    if tx_view == 'ERC20':
        view = 'tokentx'
    elif tx_view == 'normal':
        view = 'txlist'
    
    
    url = f"""https://api.etherscan.io/api?module=account&action={view}&address={address}&page=1&offset=0&startblock=0&endblock=99999999999&sort=des&apikey={ETHERSCAN_KEY}"""
    request = query(url)
    result = json_normalize(request['result'])
    result['date'] = pd.to_datetime(result.timeStamp, unit='s')

    if tx_view == 'ERC20':
        result['value'] = result.loc[:,'value'].astype(float) / (10**(result.loc[:,'tokenDecimal'].astype(float)))
        result = result.loc[:,['blockNumber', 'timeStamp', 'date', 'hash', 'nonce', 'blockHash', 'from',
        'contractAddress', 'to', 'value', 'tokenName', 'tokenSymbol',
        'tokenDecimal', 'transactionIndex', 'gas', 'gasPrice', 'gasUsed',
        'cumulativeGasUsed', 'input', 'confirmations']]
    return result

#Example
# address = '<>address'
# res = get_transactions(address, tx_view='normal')

if __name__ == "__main__":
    print(ETHERSCAN_KEY)