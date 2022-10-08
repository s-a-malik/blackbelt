#Import packages
import os
import requests

IPFS_NODE = os.environ.get("IPFS_NODE")
IPFS_ID = os.environ.get("IPFS_ID")
IPFS_SECRET = os.environ.get("IPFS_SECRET")

#Stores file on IPFS and returns hash
def store_on_ipfs(input):
    """
    Stores file on IPFS and returns hash
    @params:
        input          - Required  : input data to be uploaded
        ipfs_node      - Required  : ipfs node url
        ipfs_id        - Required  : ipfs id to connect to node
        ipfs_secret     - Optional  : ipfs secret to connect to node 
    """
    files = {
    'file': (f'{input}'),
    }

    resp = requests.post(f'{IPFS_NODE}:5001/api/v0/add', files=files, auth=(IPFS_ID, IPFS_SECRET))
    resp = resp.json()
    print(f"saved to ipfs: {resp['Hash']}")
    return resp['Hash']
    