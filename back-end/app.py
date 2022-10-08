from flask import Flask, request
from dotenv import load_dotenv

from logic import compute_security_score

load_dotenv()   # load .env file
app = Flask(__name__)
print('ready')

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/security_score")
def security_score():
    """
    Returns the security score and the metadata used to compute it for a given contract address
    Params:
    - contract_address (str): eth address of the contract
    - chain (str): chain to check the contract on
    Returns:
    - score (int): The security score (0-100)
    - contract_info (dict): 
        - age (int): age of the contract in days
        - balance (int): balance of the contract in wei
        - tx_count (int): number of transactions sent from the contract        
    """
    contract_address = request.args.get('contract_address', type=str)
    chain = request.args.get('chain', default="mainnet", type=str)
    print(f"retrieving security score for {contract_address} on {chain}")
    score, contract_info = compute_security_score(contract_address, chain)
    
    # submit to ipfs

    return {"score": score, "contract_info": contract_info}


if __name__ == '__main__':

    app.config.from_object('configurations.DevelopmentConfig')
    # app.config.from_object('configurations.ProductionConfig')
    app.run()
