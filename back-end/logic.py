"""Methods for computing security score of contracts
"""
import time
from collections import defaultdict
import numpy as np
from datetime import datetime

from sources.etherscan import is_verified, is_audited
from sources.ipfs import store_on_ipfs
from sources.coinbase import isSmartContract, numberOfTransactionsAndUsersAndAge

# global variables
contract_to_score = defaultdict(list) # {contract_address: [(score, timestamp, ipfs_hash)]}
user_to_transactions = defaultdict(list)   # {wallet_address: [(score, timestamp, contract_address, ipfs_hash)] …}
blacklist = defaultdict(int)  # {contract_address: count}

#Rating functions
#Activation functions
def sigmoid(x):
    return round(100*1/(1+e**(-x)),2)

def linear(start, end, value):
    return min(100, round(value/(end-start)*100,2))

def bucket(num, start, end, value):
    perc_bucket = 1/num
    bucket_size = (end-start)/num

    return round(np.ceil(value / bucket_size) * perc_bucket * 100,2)

#Rate deployment date - the older the better
def get_deployment_rating(days_since_deployment):
    return linear(0,365, days_since_deployment)

#Rate number of transactions - the higher the better
def get_transaction_rating(num_txs):
    return bucket(40,0,10000, num_txs)

#Rate unique users - the higher the better
def get_user_rating(number_of_unique_users):
    return linear(0,1000, number_of_unique_users)

#Rate unique users - the higher the better
def get_user_rating(number_of_unique_users):
    return linear(0,1000, number_of_unique_users)

#Rate audit score
def get_audit_rating(audited):
    if audited:
        return 100
    else:
        return 0

#Rate audit score
def get_verified_rating(verified):
    if verified:
        return 100
    else:
        return 0

#Calculate total score
def total_score(ratings):
    return round(sum(ratings)/len(ratings),2)

#Retrieve risk classification
def classify_risk(score):
    if score <= 50:
        return "High"
    elif score >50 and score <=80:
        return "Medium"
    else:
        return "Low"

#Retrieve recommendation
def get_recommendation(classification):
    if classification == 'Low':
        return "Low risk classification. The contract is unlikely to be malicious"
    elif classification == 'Medium':
        return "Medium risk classification. Be cautious and double check the contract"
    else:
        return "Warning high risk classification! Interaction is not recommended"



def compute_security_score(contract_address, chain):
    """
    Returns the security score and the metadata used to compute it for a given contract address.
    NOTE: this actually only works for mainnet contracts right now. Need to change the coinbase urls.
    """
    output = {"status": "ok"}
    # check if EOA first
    if not isSmartContract(contract_address, chain):
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


    #Calculate risk ratings
    risk_ratings =[]
    if type(verified) == bool:
        verified_rating = get_verified_rating(verified)
        risk_ratings.append(verified_rating)
    else:
        verified_rating = None

    if type(audited) == bool:
        audited_rating = get_verified_rating(audited)
        risk_ratings.append(audited_rating)
    else:
        audited_rating=None
        
    if type(min_age_of_contract_in_days) == float:
        deployment_rating = get_deployment_rating(min_age_of_contract_in_days)
        risk_ratings.append(deployment_rating)
    else:
        deployment_rating = None

    if type(transactions) == float or type(transactions) == int:
        transaction_rating = get_transaction_rating(transactions)
        risk_ratings.append(transaction_rating)
    else:
        transaction_rating = None

    if type(users) == float or type(users) == int:
        user_rating = get_user_rating(users)
        risk_ratings.append(user_rating)
    else:
        user_rating = None

    #Calculate total scores
    score = total_score(risk_ratings)
    risk_level = classify_risk(score)
    recommendation = get_recommendation(risk_level)


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
        "risk_assessment_timestamp": str(datetime.fromtimestamp(int(time.time()))),
        "num_times_reported": blacklist["contract_address"],
        "contract_info": contract_info,
        "recommendation": recommendation,
        # "ipfs_hash": store_on_ipfs(contract_info)
        # "ipfs_hash": "test"
    })


    output.update(
       {"individual_scores": {
      "audited": audited_rating, 
      "contract_age": deployment_rating, 
      "number_of_transactions": transaction_rating, 
      "number_of_unique_users": user_rating, 
      "verified": verified_rating
      }})
        
    
    
    # TODO send output as string to ipfs to store
    # ipfs_hash = store_on_ipfs(output)
    # output.update({"ipfs_hash": ipfs_hash})
    output.update({"ipfs_hash": "test"})

    return output


