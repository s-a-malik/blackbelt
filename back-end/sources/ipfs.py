#Import packages
import requests
from dotenv import load_dotenv

load_dotenv() 

#Stores file on IPFS and returns hash
def store_on_ipfs(input, ipfs_node, ipfs_id, ipfs_secret):
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

    resp = requests.post(f'{ipfs_node}:5001/api/v0/add', files=files, auth=(ipfs_id,ipfs_secret))
    resp = resp.json()
    
    return resp['Hash']
    