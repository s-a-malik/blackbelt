"""Methods for computing security score of contracts
"""

from sources.etherscan import is_verified, is_audited
from sources.ipfs import store_on_ipfs

def compute_security_score(contract_address, chain):
    """
    Returns the security score and the metadata used to compute it for a given contract address
    """

    # TODO check if EOA first using Coinbase Node eth_getCode API
    # then check if empty "0x" or "0x0" c.f. https://github.com/MetaMask/metamask-extension/blob/e3ea4f2cd044d48c61b6a35ef206fa942f3b43d1/shared/modules/contract-utils.js

    verified = is_verified(contract_address, chain)
    audited = is_audited(contract_address, chain)
    score = 0
    # logic
    if not verified:
        score = 0
    if audited:
        score += 100

    contract_info = {
        "verified": verified,
        "audited": audited
    }

    return score, contract_info

    #To-Do send output as string to ipfs to store
    #store_on_ipfs('test')
