import os
import sys

from wallet_lib.wallet_factory import WalletFactory

if len(sys.argv) != 2:
    raise Exception('Please define ticker symbol as an argument. Example: python3 test_runner.py BCH')

wallet = WalletFactory().get(sys.argv[1])
print ('Wallet balance is {}'.format(wallet.get_balance()))