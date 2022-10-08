from flask import Flask, request
from dotenv import load_dotenv

import configurations
from logic import security_score

load_dotenv()   # load .env file
app = Flask(__name__)
print('ready')

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/security_score/<str:contract_address>")
def security_score(contract_address):
    """
    Returns the security score and the metadata used to compute it for a given contract address
    Params:
    - contract_address (str): eth address of the contract
    Returns:
    - score (int): The security score (0-100)
    - contract_info (dict): 
        - age (int): age of the contract in days
        - balance (int): balance of the contract in wei
        - tx_count (int): number of transactions sent from the contract        
    """
    score = security_score(contract_address)

    return score


if __name__ == '__main__':

    app.config.from_object('configurations.DevelopmentConfig')
    # app.config.from_object('configurations.ProductionConfig')
    app.run()
