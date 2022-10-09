# Blackbelt

Self-defense against scammers, directly in your wallet.

Blackbelt provides additional security-related information about the contract you are interacting with, in real-time,
directly in your wallet. This is vital for improving the security of new and non-technical users.

## Overview

We provide security for metamask to avoid front end exploits.

## Repo Structure and Stack

Stack:

- Metamask snap
- coinbase cloud Node for web3 data
- etherscan API for contract information
- IPFS for storing security score computation information

### back-end

Server for retrieving blockchain data and computing security score.

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