from flask import Flask, request

import configurations
from logic import security_score

app = Flask(__name__)
print('ready')

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/carbon_density/<int:project_id>")
def security_score(contract_address):
    """
    Returns the security score and the metadata used to compute it for a given contract address
    Params:
    - contract_address (str): eth address of the contract
    Returns:
    - score (int): The security score (0-100)
    - contract_info (dict): 
        - baselineBiomass5Year (float): The baseline biomass of the project
        - satelliteDelta1Year (float): The change in biomass of the project over 1 year
        - projectedDelta1Year (float): The projected change in biomass of the project over 1 year
    """
    carbon_data = get_carbon_density(project_id)

    return carbon_data


if __name__ == '__main__':

    app.config.from_object('configurations.DevelopmentConfig')
    # app.config.from_object('configurations.ProductionConfig')
    app.run()