"""Get data from coinbase cloud.
"""

import os
import json

from utils.api_requests import post_request

COINBASE_KEY = os.getenv("COINBASE_KEY")


def _make_base_coinbase_url(chain="mainnet"):
    if chain == "mainnet":
        return "https://mainnet.ethereum.coinbasecloud.net"
    elif chain == "goerli":
        return "https://goerli.ethereum.coinbasecloud.net"
    else:
        raise ValueError(f"Chain {chain} not supported")


def coinbaseCloud_getTransactionsByAddress(address: str, blockEnd: str = '', chain: str = 'mainnet'):
    url = _make_base_coinbase_url(chain=chain)
    chain = chain.capitalize()  # for coinbase

    if blockEnd == '':
        payload = json.dumps({
        "id": 1,
        "jsonrpc": "2.0",
        "method": "coinbaseCloud_getTransactionsByAddress",
        "params": {
            "address": address,
            "blockStart": "0x000000",
            "addressFilter": "SENDER_OR_RECEIVER",
            "blockchain": "Ethereum",
            "network": chain
        }
        })

    else:
        payload = json.dumps({
        "id": 1,
        "jsonrpc": "2.0",
        "method": "coinbaseCloud_getTransactionsByAddress",
        "params": {
            "address": address,
            "blockStart": "0x000000",
            "blockEnd": blockEnd,
            "addressFilter": "SENDER_OR_RECEIVER",
            "blockchain": "Ethereum",
            "network": chain
        }
        })

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {COINBASE_KEY}'
    }

    response = post_request(url, headers=headers, data=payload)

    return response.json()


def isSmartContract(address: str, chain: str = 'mainnet'):
    url = _make_base_coinbase_url(chain)
    payload = json.dumps({
        "id": 1,
        "jsonrpc": "2.0",
        "method": "eth_getCode",
        "params": [
        address,
        "latest"
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {COINBASE_KEY}'
    }

    response = post_request(url, headers=headers, data=payload).json()

    return len(response['result']) > 10


def numberOfTransactionsAndUsersAndAge(address: str, chain: str = 'mainnet'):

    total_count_transactions = 0
    total_count_users_to = set()
    total_count_users_from = set()
    contract_age = 10e12

    def countBlocksTransactions(blocks):
        count = 0
        for block in blocks:
            count += len(block['transactions']) 
        return count

    def addBlocksUsersDate(blocks):

        to_set = set()
        from_set = set()
        date = 1e20

        for block in blocks:
            for transaction in block['transactions']:

                to_set = to_set.union(set({transaction['to']}))
                from_set = from_set.union(set({transaction['from']}))

                if date > int(transaction['blockTimestamp'], 16):
                    date = int(transaction['blockTimestamp'], 16)

        return to_set, from_set, date

    def getNewEndBlock(response):
        return hex(int(response['result']['blockStart'], 16) - 1)

    blockEnd = ''
    counter = 0

    while (blockEnd == '' or int(blockEnd, 16) > 0) and counter < 10:

        response = coinbaseCloud_getTransactionsByAddress(address, blockEnd, chain)
        blocks = response['result']['blocks']

        total_count_transactions += countBlocksTransactions(blocks)
        to_set, from_set, date = addBlocksUsersDate(blocks)

        total_count_users_to = total_count_users_to.union(to_set)
        total_count_users_from = total_count_users_from.union(from_set)
        if contract_age > date:
            contract_age = date

        blockEnd_new = getNewEndBlock(response)

        if blockEnd == blockEnd_new:
            break
        else:
            blockEnd = blockEnd_new

        counter += 1

    return total_count_transactions, len(total_count_users_to) + len(total_count_users_from), date


if __name__ == "__main__":
    address = '0x00000000219ab540356cbb839cbe05303d7705fa'
    transactions, users, age = numberOfTransactionsAndUsersAndAge(address)
    print(transactions, users, age)