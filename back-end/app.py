from dotenv import load_dotenv

from flask import Flask, request, Response

from logic import compute_security_score, contract_to_score, user_to_transactions, blacklist

load_dotenv()   # load .env file
app = Flask(__name__)
print('ready')

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/security_score", methods=['GET'])
def security_score():
    """
    Returns the security score and the metadata used to compute it for a given contract address.
    Saves result to ipfs and local storage.
    Params:
    - user_address: the address of the user to check
    - contract_address (str): eth address of the contract
    - chain (str): chain to check the contract on
    Returns:
    - score (int): The security score (0-100)
    - contract_info (dict): 
        - age (int): age of the contract in days
        - balance (int): balance of the contract in wei
        - tx_count (int): number of transactions sent from the contract        
    """
    user_address = request.args.get('user_address', type=str)
    contract_address = request.args.get('contract_address', type=str)
    chain = request.args.get('chain', default="mainnet", type=str)
    print(f"retrieving security score for {contract_address} on {chain}")
    output = compute_security_score(contract_address, chain)
    if output["status"] != "ok":
        return Response(output, status=400)

    # add to the server cache
    contract_to_score[contract_address].append({"security_score": output["security_score"], "risk_assessment_timestamp": output["risk_assessment_timestamp"], "ipfs": output["ipfs_hash"]})
    user_to_transactions[user_address].append({"security_score": output["security_score"], "contract_address": contract_address, "risk_assessment_timestamp": output["risk_assessment_timestamp"], "ipfs": output["ipfs_hash"]})

    return output


@app.route("/blacklist", methods=['POST'])
def blacklist():
    """Flag a contract to the blacklist
    """
    contract_address = request.args.get('contract_address', type=str)
    print(f"blacklisting {contract_address}")
   
    blacklist[contract_address] += 1

    return Response({"status": "ok"}, status=200)


@app.route("/prev_transactions")
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
    app.run()
