import { OnRpcRequestHandler } from '@metamask/snap-types';
import { OnTransactionHandler } from "@metamask/snap-types";

function stringify_json(field, data){
  var temp_data = data[field];
  temp_data = JSON.stringify(temp_data);
  temp_data = temp_data.replace('{','').replace('}','').replace(/"/g, " ").replace(/_/g, ' ');

  return temp_data
};

export const onTransaction: OnTransactionHandler = async ({
  transaction,
  chainId,
}) => {

  // Get tx data
  const user_address = transaction.from;
  const contract_address =  transaction.to;
  const chain_id =  chainId.split(":")[1];
  
  // Call api for risk assessment
  const url = 'http://127.0.0.1:5000/security_score?contract_address='+contract_address+'&user_address='+user_address+'&chain='+chain_id;
  console.log(url);

  await fetch(url)
  .then((response) => response.json())
  .then((data) => {

  console.log(data);

  // Cases for returning insights
  if (data.status == "ok"){
    const individual_scores = stringify_json('individual_scores', data)
    const individual_details = stringify_json('contract_info', data)
    return {
      insights: {"Risk Assessment": data.risk_level, "Security Score": data.security_score, "Recommendation": data.recommendation, "IPFS Storage Hash": data.ipfs_hash, "Individual Scores": individual_scores, "Details": individual_details, "Assessment Timestamp": data.risk_assessment_timestamp},
    };
  } else if(data.status =='error, not a contract address'){
    return {
      insights: {"No Score Available": "No interaction with a smart contract detected.", "Assessment Timestamp": data.risk_assessment_timestamp},
    };
  } else if(data.status =='error, unsupported chain'){
    return {
      insights: {"Chain Not Supported": "We are currently supporting Ethereum and Goerli only. We are working on adding more networks."},
    };
  } else {
    return {
      insights: {"Unknown Error": "An unknown error occured. Please contact the team and try again later."},
    };
  }
});

};

