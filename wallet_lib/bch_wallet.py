import json

from cmd_caller import CMDCaller
from wallet_exceptions import WalletException

class BCHWallet(CMDCaller):

    TICKER_SYMBOL = 'BCH'

    _GET_ADDRESSES_COMMAND = 'getaddressesbyaccount'
    _GET_BALANCE_COMMAND = 'getbalance'
    _GET_TRANSACTION_COMMAND = 'gettransaction'
    _GET_TRANSACTIONS_COMMAND = 'listtransactions'
    _CREATE_ADDRESS_COMMAND = 'getnewaddress'
    _MOVE_COMMAND = 'move'
    _SEND_FROM_COMMAND = 'sendfrom'
    
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

    def get_transactions(self, account=None, count:int=25, offset:int=0):
        account_str = account or '""'
        res = self.run(self._GET_TRANSACTIONS_COMMAND, account_str, count, offset)
        if res.error:
            raise WalletException(reason='Failed to get transactions for {} where count is {} and offset is {}. Reason: {}. Code: {}'.format(
                account_str, count, offset, res.error, res.code))
        return res.result

    def move(self, from_account, to_account, amount:int):
        res = self.run(self._MOVE_COMMAND, from_account, to_account, amount)
        if res.error:
            raise WalletException(reason='Failed to move {} from {} to {}. Reason: {}. Code: {}'.format(
                amount, from_account, to_account, res.error, res.code))
        return res.result

    def send_from(self, from_account, address, amount:int):
        res = self.run(self._SEND_FROM_COMMAND, from_account, address, amount)
        if res.error:
            raise WalletException(reason='Failed to send {} from {} to {}. Reason: {}. Code: {}'.format(
                amount, from_account, address, res.error, res.code))
        return res.result