from .adapters import WalletAdapterBase
from .wallet_exceptions import WalletException

class WalletInterface:

  _GET_BALANCE_COMMAND = 'getbalance'
  _GET_TRANSACTION_COMMAND = 'gettransaction'
  _GET_TRANSACTIONS_COMMAND = 'listtransactions'
  _GET_TRANSACTIONS_SINCE_COMMAND = 'listsinceblock'
  _CREATE_ADDRESS_COMMAND = 'getnewaddress'
  _SEND_TO_COMMAND = 'sendtoaddress'

  def __init(self, *args):
    self.adapter = None
    raise Exception("Cannot create an instance of WalletInterface")

  def run(self, command, *args):
    res = self.adapter.run(command, *args)
    if res.error:
        raise WalletException('Failed to run command: {}. Reason: {}. Code: {}'.format(command, res.error, res.code))
    return res.result