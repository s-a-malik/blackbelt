# Blackbelt

Self-defense against scammers, directly in your wallet.

Blackbelt provides additional security-related information about the contract you are interacting with, in real-time,
directly in your wallet. This is vital for improving the security of new and non-technical users.

## Overview

We provide security assessments for smart contract interactions directly in metamask and on our website. The risk score is calculated in real-time based on on-chain data. 

Furthermore, we experimented with a revert feature that transforms the transaction focused execution to an intend focused value transfer. The feature uses a smart contract to check if the balance changes are in line with what is expected and reverts the transaction if the criteria is not fulfilled. 

## Repo Structure and Stack

Stack:

- Metamask snap
- Coinbase cloud Node for web3 data
- Etherscan API for contract information
- IPFS for storing security score computation information
- PocketNetwork node client
- Solidity and Polygon testnet to test our revert feature:
   - https://mumbai.polygonscan.com/tx/0x990e5be972a7c79a700b97f72ba77df1ff934669c5bab1097243a01fd73194cc
   - https://mumbai.polygonscan.com/tx/0x7d4931f717df02d7f64b6610552ffc56a87098921c3e5e99ac340c989e637cd5
   - https://mumbai.polygonscan.com/tx/0xfbf941c560125e34edd2c072dcc1ada50f961d595fc48eab371246fddf6fc8fb

### back-end

Flask server for retrieving blockchain data and computing security score.

Usage:

- Create a python virtual environment (recommended)
- install requirements `pip install -r requirements.txt`
- add API keys to .env file
- run server `python app.py`

### front-end

Website to set up snaps and trial usage.

Usage:

- `npm install`
- `npm start`

### snap

Add the Blackbelt snap to metamask.

Usage:
- Follow instructions from the metamask snap template (documentation)[https://docs.metamask.io/guide/snaps.html?utm_source=ethbogota&utm_medium=event&utm_campaign=2022_Sep_ethbogota-hackathon-page_awareness_event].


### revert

Smart contracts for reverting transactions if intent not met.
