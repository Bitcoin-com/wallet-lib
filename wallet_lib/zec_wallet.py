import json

from .adapters import WalletAdapterBase
from .wallet_exceptions import WalletException
from .wallet_base import WalletBase

class ZECWallet(WalletBase):

    TICKER_SYMBOL = 'ZEC'

    _GET_BALANCE_COMMAND = 'z_getbalance'
    _GET_TRANSACTION_COMMAND = 'gettransaction'
    _LIST_TRANSACTIONS_COMMAND = 'listtransactions'
    _LIST_SINCE_BLOCK_COMMAND = 'listsinceblock'
    _GET_NEW_ADDRESS_COMMAND = 'getnewaddress'
    _SEND_TO_ADDRESS_COMMAND = 'sendtoaddress'

    def __init__(self, adapter: WalletAdapterBase):
        self.adapter = adapter

    def create_address(self, label=None):
        label_str = label or '""'
        res = self.adapter.run(self._GET_NEW_ADDRESS_COMMAND, label_str)
        if res.error:
            raise WalletException('Failed to create address for {}. Reason: {}. Code: {}'.format(
                label, res.error, res.code))
        return res.result

    def get_balance(self):
        res = self.adapter.run(self._GET_BALANCE_COMMAND)
        if res.error:
            raise WalletException(
                'Failed to get balance. Reason: {}. Code: {}'.format(res.error, res.code))
        return res.result

    def get_transaction(self, tx_id):
        res = self.adapter.run(self._GET_TRANSACTION_COMMAND, tx_id)
        if res.error:
            raise WalletException('Failed to get transaction by {}. Reason: {}. Code: {}'.format(
                tx_id, res.error, res.code))
        return res.result

    def get_transactions(self, label: str = None, count: int = 25, offset: int = 0):
        label_str = label or '""'
        res = self.adapter.run(
            self._LIST_TRANSACTIONS_COMMAND, label_str, count, offset)
        if res.error:
            raise WalletException('Failed to get transactions for {} where count is {} and offset is {}. Reason: {}. Code: {}'.format(
                label_str, count, offset, res.error, res.code))
        return json.loads(res.result)

    def send(self, address:str, amount:int):
        if address is None:
            raise WalletException('Address is invalid')
        if amount <= 0:
            raise WalletException('Amount should be greater than 0')
        res = self.adapter.run(self._SEND_TO_ADDRESS_COMMAND, address, str(amount))
        if res.error:
            raise WalletException('Failed to send {} {} to {}. Reason: {}. Code: {}'.format(
                amount, self.TICKER_SYMBOL, address, res.error, res.code))
        return res.result

    def get_transactions_since(self, block_hash):
        res = self.adapter.run(
            self._LIST_SINCE_BLOCK_COMMAND, block_hash)
        if res.error:
            raise WalletException('Failed to get transactions since blockhash: {}. Reason: {}. Code: {}'.format(
                block_hash, res.error, res.code))
        return json.loads(res.result)

    def run(self, command, *args):
        res = self.adapter.run(command, *args)
        if res.error:
            raise WalletException('Failed to run command: {}. Reason: {}. Code: {}'.format(command, res.error, res.code))
        return res.result
