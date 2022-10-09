"""Methods for computing security score of contracts
"""
import time
from collections import defaultdict

from sources.etherscan import is_verified, is_audited
from sources.ipfs import store_on_ipfs
from sources.coinbase import isSmartContract, numberOfTransactionsAndUsersAndAge

# global variables
contract_to_score = defaultdict(list) # {contract_address: [(score, timestamp, ipfs_hash)]}
user_to_transactions = defaultdict(list)   # {wallet_address: [(score, timestamp, contract_address, ipfs_hash)] …}
blacklist = defaultdict(int)  # {contract_address: count}


def compute_security_score(contract_address, chain):
    """
    Returns the security score and the metadata used to compute it for a given contract address.
    NOTE: this actually only works for mainnet contracts right now. Need to change the coinbase urls.
    """
    output = {"status": "ok"}
    # check if EOA first
    if not isSmartContract(contract_address):
        output["status"] = "error, not a contract address"
        return output
    
    # check if chain is supported
    if chain != "mainnet" and chain != "goerli":
        output["status"] = "error, unsupported chain"
        return output
    
    verified = is_verified(contract_address, chain)
    audited = is_audited(contract_address, chain)
    transactions, users, deployed_date_unix = numberOfTransactionsAndUsersAndAge(contract_address)
    min_age_of_contract_in_days = (time.time() - deployed_date_unix) / 86400
    score = 0

    # logic
    if not verified:
        score = 0
    if audited:
        score += 100

    risk_level = "high" if score < 50 else "medium" if score < 75 else "low"

    contract_info = {
        "verified": verified,
        "audited": audited,
        "number_of_transactions": transactions,
        "number_of_unique_users": users,
        "min_age_of_contract_in_days": min_age_of_contract_in_days
    }

    output.update({
        "contract_address": contract_address,
        "security_score": score,
        "risk_level": risk_level,
        "risk_assessment_timestamp": int(time.time()),
        "num_times_reported": blacklist["contract_address"],
        "contract_info": contract_info,
        "recommendation": "PLACEHOLDER", #TO-DO
        # "ipfs_hash": store_on_ipfs(contract_info)
        # "ipfs_hash": "test"
    })

    #TO-DO: currently placeholder
    output.update(
       {"individual_scores": {
      "audited": 100, 
      "deployed_date": 100, 
      "number_of_transactions": 50, 
      "number_of_unique_users": 25, 
      "verified": 75
      }})
        
    
    
    # TODO send output as string to ipfs to store
    ipfs_hash = store_on_ipfs(output)
    output.update({"ipfs_hash": ipfs_hash})

    return output


