import { OnRpcRequestHandler } from '@metamask/snap-types';
import { OnTransactionHandler } from "@metamask/snap-types";
//import fetch from 'cross-fetch';
//import axios from 'axios';
//const axios = require('axios');
//import 'cross-fetch/polyfill';

export const onTransaction: OnTransactionHandler = async ({
  transaction,
  chainId,
}) => {
  await fetch('http://127.0.0.1:5000/security_score?contract_address=0x984e7B3f332a2a6Fc1EB73B5B8F8E95D24ee2097')
  .then((response) => response.json())
  .then((data) => console.log(data));
  const insights = { score: 42, "Is contract verified on Etherscan?": "Yes" };
  return { insights };
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
