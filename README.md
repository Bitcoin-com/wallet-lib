# Wallet lib
[![PyPI version](https://badge.fury.io/py/wallet-lib.svg)](https://badge.fury.io/py/wallet-lib) ![](https://github.com/Bitcoin-com/wallet_lib/workflows/CI/badge.svg)
## Description
This library contains classes to work with hot wallet for different cryptocurrency.
## API Documentation
### Supported cryptocurrencies
1. BCH
1. BTC
1. DASH
1. ZEC
### Endpoints
1. `create_address(label)` - creates address by label
1. `get_balance()` - returns current balance
1. `get_transaction(tx_id)` - returns transaction info by tx id
1. `get_transactions(label, count, offset)` - returns list of transactions by label based on count and offset arguments. All arguments are optional. Default values: `label` - None, `count` - 25, `offset` - 0.
1. `send(sender, recipient, amount)` - sends some amount from sender to recipient.
1. `get_transactions_since(block_hash)` - get all transactions in blocks since block block_hash, or all transactions if block_hash is None.
