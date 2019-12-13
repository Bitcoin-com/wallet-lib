from .adapters import WalletAdapterBase
from .wallet_exceptions import WalletException

class WalletInterface:

    def __init__(self, *args):
        self.adapter = None
        raise WalletException("Cannot initialize WalletInterface")

    def run(self, command, *args):
        res = self.adapter.run(command, *args)
        if res.error:
            raise WalletException('Failed to run command: {}. Reason: {}. Code: {}'.format(command, res.error, res.code))
        return res.result