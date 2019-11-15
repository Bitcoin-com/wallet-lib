import json

from cmd_caller import CMDCaller
from wallet_exceptions import WalletException

class BTCWallet(CMDCaller):

    TICKER_SYMBOL = 'BTC'

    _GET_ADDRESSES_COMMAND = 'getaddressesbylabel'
    _GET_BALANCE_COMMAND = 'getbalance'
    _GET_TRANSACTION_COMMAND = 'gettransaction'
    _GET_TRANSACTIONS_COMMAND = 'listtransactions'
    _CREATE_ADDRESS_COMMAND = 'getnewaddress'
    _SEND_TO_COMMAND = 'sendtoaddress'
    
    def __init__(self):
        CMDCaller.__init__(self, 'bitcoin-cli')

    def create_address(self, label):
        res = self.run(self._CREATE_ADDRESS_COMMAND, label)
        if res.error:
            raise WalletException(reason='Failed to create address for {}. Reason: {}. Code: {}'.format(label, res.error, res.code))
        return res.result
    
    def get_addresses(self, label):
        ''' Get the an array of bitcoin addresses matching label. '''
        res = self.run(self._GET_ADDRESSES_COMMAND, label)
        if res.error:
            raise WalletException(reason='Failed to get addresses by {}. Reason: {}. Code: {}'.format(label, res.error, res.code))
        return json.loads(res.result)
    
    def get_balance(self):
        res = self.run(self._GET_BALANCE_COMMAND)
        if res.error:
            raise WalletException(reason='Failed to get balance. Reason: {}. Code: {}'.format(res.error, res.code))
        return res.result

    def get_transaction(self, tx_id):
        res = self.run(self._GET_TRANSACTION_COMMAND, tx_id)
        if res.error:
            raise WalletException(reason='Failed to get transactiob by {}. Reason: {}. Code: {}'.format(tx_id, res.error, res.code))
        return res.result

    def get_transactions(self, label=None, count:int=25, skip:int=0):
        label_str = label or '""'
        res = self.run(self._GET_TRANSACTIONS_COMMAND, label_str, count, skip)
        if res.error:
            raise WalletException(reason='Failed to get transactions for {} where count is {} and skip is {}. Reason: {}. Code: {}'.format(
                label_str, count, skip, res.error, res.code))
        return res.result

    def send_to(self, address, amount:int):
        res = self.run(self._SEND_TO_COMMAND, address, amount)
        if res.error:
            raise WalletException(reason='Failed to send {} to {}. Reason: {}. Code: {}'.format(
                amount, address, res.error, res.code))
        return res.result