# Wallet lib
## Description
This library contains classes to work with hot wallet for different cryptocurrency.
## API Documentation
### BCH
1. `create_address(label)` - creates address by label
2. `get_addresses(label)` - returns list of addresses by label
3. `get_balance()` - returns current balance
4. `get_transaction(tx_id)` - returns transaction info by tx id
5. `get_transactions(account, count, offset)` - returns list of transactions for account based on acount and offset arguments. `count` is optional, default - 25. `offset` is optional, default = 0.
6. `move(from_account, to_account, amount)` - move some amount from one account to another account.
7. `send_from(from_account, address, amount)` - sends some amount from account to address.
### BTC
1. `create_address(label)` - creates address by label
2. `get_addresses(label)` - returns list of addresses by label
3. `get_balance()` - returns current balance
4. `get_transaction(tx_id)` - returns transaction info by tx id
5. `get_transactions(label, count, skip)` - returns list of transactions by label based on count and skip arguments. `count` is optional, default - 25. `skip` is optional, default = 0.
6. `send_to(address, amount)` - sends some amount to address.
### DASH
### ZEC
