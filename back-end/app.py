from dotenv import load_dotenv
import os

from flask import Flask, request, Response
from flask_cors import CORS, cross_origin

from logic import compute_security_score, contract_to_score, user_to_transactions, blacklist_dict


load_dotenv()   # load .env file
app = Flask(__name__)
CORS(app)
print('ready')

@app.route("/")
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/security_score", methods=['GET'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def security_score():
    """
    Returns the security score and the metadata used to compute it for a given contract address.
    Saves result to ipfs and local storage.
    Params:
    - user_address: the address of the user to check
    - contract_address (str): eth address of the contract
    - chain_id (int): chain to check the contract on
    Returns:
    - score (int): The security score (0-100)
    - contract_info (dict): 
        - age (int): age of the contract in days
        - balance (int): balance of the contract in wei
        - tx_count (int): number of transactions sent from the contract        
    """
    # user_address = request.args.get('user_address', type=str)
    # contract_address = request.args.get('contract_address', type=str)
    # chain_id = request.args.get('chain', default=1, type=int)
    # chain = "mainnet" if chain_id == 1 else "goerli"

    # print(f"retrieving security score for {contract_address} on {chain}")
    # output = compute_security_score(contract_address, chain)
    # if output["status"] != "ok":
    #     return output

    # # add to the server cache
    # contract_to_score[contract_address].append({"security_score": output["security_score"], "risk_assessment_timestamp": output["risk_assessment_timestamp"], "ipfs": output["ipfs_hash"]})
    # user_to_transactions[user_address].append({"security_score": output["security_score"], "contract_address": contract_address, "risk_assessment_timestamp": output["risk_assessment_timestamp"], "ipfs": output["ipfs_hash"]})
    
    output = {
        "contract_address": "0x984e7B3f332a2a6Fc1EB73B5B8F8E95D24ee2097", 
        "contract_info": {
            "audited": False, 
            "min_age_of_contract_in_days": 0.9696542505450823, 
            "number_of_transactions": 5541, 
            "number_of_unique_users": 3329, 
            "verified": True
        }, 
        "individual_scores": {
            "audited": 0, 
            "contract_age": 0.27, 
            "number_of_transactions": 57.5, 
            "number_of_unique_users": 100, 
            "verified": 100
        }, 
        "ipfs_hash": "test", 
        "num_times_reported": 0, 
        "recommendation": "Medium risk classification. Be cautious and double check the contract", 
        "risk_assessment_timestamp": "2022-10-09 02:40:29", 
        "risk_level": "Medium", 
        "security_score": 51.55, 
        "status": "ok"
    }
    return output
    

@app.route("/blacklist", methods=['GET'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def blacklist():
    """Flag a contract to the blacklist
    """
    contract_address = request.args.get('contract_address', type=str)
    print(f"blacklisting {contract_address}")
    print(blacklist_dict)
    print(blacklist_dict[contract_address])
    blacklist_dict[contract_address] += 1
    return {"status": "ok"}


@app.route("/prev_transactions")
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def prev_transactions():
    """
    Returns the previous transactions with security scores for a given wallet address
    Params:
    - wallet_address (str): eth address of the wallet
    - chain (str): chain to check the contract on
    Returns:
    - transactions (list): list of previous transactions
    """
    wallet_address = request.args.get('wallet_address', type=str)
    chain = request.args.get('chain', default="mainnet", type=str)
    print(f"retrieving previous transactions for {wallet_address} on {chain}")

    # check server cache
    output = user_to_transactions[wallet_address]
    
    return output


if __name__ == '__main__':

    app.config.from_object('configurations.DevelopmentConfig')
    # app.config.from_object('configurations.ProductionConfig')
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    # app.run()
