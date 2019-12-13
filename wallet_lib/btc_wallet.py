import json

from .adapters.wallet_adapter_base import WalletAdapterBase
from .wallet_exceptions import WalletException


class BTCWallet:

    _GET_ADDRESSES_COMMAND = 'getaddressesbylabel'
    _GET_BALANCE_COMMAND = 'getbalance'
    _GET_TRANSACTION_COMMAND = 'gettransaction'
    _GET_TRANSACTIONS_COMMAND = 'listtransactions'
    _GET_TRANSACTIONS_SINCE_COMMAND = 'listsinceblock'
    _CREATE_ADDRESS_COMMAND = 'getnewaddress'
    _SEND_TO_COMMAND = 'sendtoaddress'

    def __init__(self, adapter: WalletAdapterBase):
        self.adapter = adapter

    def create_address(self, label):
        res = self.adapter.run(self._CREATE_ADDRESS_COMMAND, label)
        if res.error:
            raise WalletException(reason='Failed to create address for {}. Reason: {}. Code: {}'.format(
                label, res.error, res.code))
        return res.result

    def get_addresses(self, label):
        ''' Get the an array of bitcoin addresses matching label. '''
        res = self.adapter.run(self._GET_ADDRESSES_COMMAND, label)
        if res.error:
            raise WalletException(reason='Failed to get addresses by {}. Reason: {}. Code: {}'.format(
                label, res.error, res.code))
        return res.result

    def get_balance(self):
        res = self.adapter.run(self._GET_BALANCE_COMMAND)
        if res.error:
            raise WalletException(
                reason='Failed to get balance. Reason: {}. Code: {}'.format(res.error, res.code))
        return res.result

    def get_transaction(self, tx_id):
        res = self.adapter.run(self._GET_TRANSACTION_COMMAND, tx_id)
        if res.error:
            raise WalletException(reason='Failed to get transactiob by {}. Reason: {}. Code: {}'.format(
                tx_id, res.error, res.code))
        return res.result

    def get_transactions(self, label: str = None, count: int = 25, offset: int = 0):
        label_str = label or '""'
        res = self.adapter.run(
            self._GET_TRANSACTIONS_COMMAND, label_str, count, offset)
        if res.error:
            raise WalletException(reason='Failed to get transactions for {} where count is {} and offset is {}. Reason: {}. Code: {}'.format(
                label_str, count, offset, res.error, res.code))
        return res.result

    def send(self, sender: str = None, recipient: str = None, amount: int = 0):
        if recipient is None:
            raise WalletException(reason='Recipinet is invalid')
        if amount == 0:
            raise WalletException(reason='Amount should be greater than 0')
        res = self.adapter.run(self._SEND_TO_COMMAND, recipient, str(amount))
        if res.error:
            raise WalletException(reason='Failed to send {} to {}. Reason: {}. Code: {}'.format(
                amount, recipient, res.error, res.code))
        return res.result

    def get_transactions_since(self, block_hash=None):
        res = self.adapter.run(
            self._GET_TRANSACTIONS_SINCE_COMMAND, block_hash)
        if res.error:
            raise WalletException(reason='Failed to get transactions since {}. Reason: {}. Code: {}'.format(
                block_hash, res.error, res.code))
        return res.result
