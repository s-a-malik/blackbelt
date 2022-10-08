"""Methods for computing security score of contracts
"""
import time

from sources.etherscan import is_verified, is_audited
from sources.ipfs import store_on_ipfs
from sources.coinbase import isSmartContract, numberOfTransactionsAndUsersAndAge

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

    output.update({"contract_address": contract_address, "score": score, "risk_assessment_timestamp": time.time(), "contract_info": contract_info})

    # TODO send output as string to ipfs to store
    #store_on_ipfs('test')


    return output


