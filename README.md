# Wallet lib
[![PyPI version](https://badge.fury.io/py/wallet-lib.svg)](https://badge.fury.io/py/wallet-lib) ![](https://github.com/Bitcoin-com/wallet_lib/workflows/CI/badge.svg)
## Description
This library contains classes to work with hot wallet for different cryptocurrency.
## API Documentation
### Supported cryptocurrencies
1. BCH
2. BTC
### Endpoints
1. `create_address(label)` - creates address by label
2. `get_addresses(label)` - returns list of addresses by label
3. `get_balance()` - returns current balance
4. `get_transaction(tx_id)` - returns transaction info by tx id
5. `get_transactions(label, count, offset)` - returns list of transactions by label based on count and offset arguments. All arguments are optional. Default values: `label` - None, `count` - 25, `offset` - 0.
6. `send(sender, recipient, amount)` - sends some amount from sender to recipient.
7. `get_transactions_since(block_hash)` - get all transactions in blocks since block block_hash, or all transactions if block_hash is None.