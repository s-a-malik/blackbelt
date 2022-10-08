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
    
    verified = is_verified(contract_address, chain)
    audited = is_audited(contract_address, chain)
    transactions, users, deployed_date_unix = numberOfTransactionsAndUsersAndAge(contract_address)
    score = 0
    # logic
    if not verified:
        score = 0
    if audited:
        score += 100

    contract_info = {
        "verified": verified,
        "audited": audited,
        "number_of_transactions": transactions,
        "number_of_unique_users": users,
        "deployed_date_unix": deployed_date_unix
    }

    output.update({
        "contract_address": contract_address,
        "security_score": score,
        "risk_assessment_timestamp": int(time.time()),
        "num_times_reported": blacklist["contract_address"],
        "contract_info": contract_info,
        # "ipfs_hash": store_on_ipfs(contract_info)
        # "ipfs_hash": "test"
    })

    # TODO send output as string to ipfs to store
    ipfs_hash = store_on_ipfs(output)
    output.update({"ipfs_hash": ipfs_hash})

    return output


