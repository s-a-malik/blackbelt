
import requests
import pandas as pd
from pandas import json_normalize
import os

#Parameter
ETH_API_KEY = '<KEY>'

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
def get_transactions(address, tx_view = 'ERC20', ETH_API_KEY = ETH_API_KEY):
    if tx_view == 'ERC20':
        view = 'tokentx'
    elif tx_view == 'normal':
        view = 'txlist'
    
    
    url = f"""https://api.etherscan.io/api?module=account&action={view}&address={address}&page=1&offset=0&startblock=0&endblock=99999999999&sort=des&apikey={ETH_API_KEY}"""
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
