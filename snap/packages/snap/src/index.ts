import { OnRpcRequestHandler } from '@metamask/snap-types';
import { OnTransactionHandler } from "@metamask/snap-types";
//import fetch from 'cross-fetch';
//import axios from 'axios';
//const axios = require('axios');
//import 'cross-fetch/polyfill';
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
  // const contract_address =  transaction.to;
  //let contract_address = "0x984e7B3f332a2a6Fc1EB73B5B8F8E95D24ee2097";
  // Get tx data
  const user_address = transaction.from;
  const contract_address =  transaction.to;
  const chain_id =  chainId.split(":")[1];
  
  // Call api for risk assessment
  const url = 'http://127.0.0.1:5000/security_score?contract_address='+contract_address+'&user_address='+user_address+'&chain='+chain_id+'is_snaps=true';
  // console.log(url);
  let x = await fetch(url);
  //let x = await fetch('http://127.0.0.1:5000/security_score?contract_address='+ contract_address + 'is_snaps=true');
  //let x = await fetch('http://127.0.0.1:5000/security_score?contract_address=0x984e7B3f332a2a6Fc1EB73B5B8F8E95D24ee2097');
  let data = await x.json();
  console.log(data);
  // console.log(contract_address);
  // let z = y["contract_info"];
  // const insights = {"verified": z["verified"], 
  //                   "audited": z["audited"],
  //                   "transactions": z["number_of_transactions"]};
  // // Cases for returning insights
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
};

async function getFees() {
  const response = await fetch('https://www.etherchain.org/api/gasPriceOracle'); 
  return response.text(); 
}

//  axios.get('http://127.0.0.1:5000/security_score?contract_address=0x984e7B3f332a2a6Fc1EB73B5B8F8E95D24ee2097').then(function (response) {
//  	console.log(response);
//  });

/**
 * Get a message from the origin. For demonstration purposes only.
 *
 * @param originString - The origin string.
 * @returns A message based on the origin.
 */
export const getMessage = (originString: string): string => {
  return `Hello, ${originString}!`;
}

/**
 * Handle incoming JSON-RPC requests, sent through `wallet_invokeSnap`.
 *
 * @param args - The request handler args as object.
 * @param args.origin - The origin of the request, e.g., the website that
 * invoked the snap.
 * @param args.request - A validated JSON-RPC request object.
 * @returns `null` if the request succeeded.
 * @throws If the request method is not valid for this snap.
 * @throws If the `snap_confirm` call failed.
 */
 export const onRpcRequest: OnRpcRequestHandler = ({ origin, request }) => {
  switch (request.method) {
    case 'hello':
      return getFees().then(fees => {
        return wallet.request({
          method: 'snap_confirm', 
          params: [
            {
              prompt: getMessage(origin),
              description:
                'This custom confirmation is just for display purposes.',
              textAreaContent:
                `Current fee estimates: ${fees}`,
            }
          ]
        }); 
      }); 
}};

