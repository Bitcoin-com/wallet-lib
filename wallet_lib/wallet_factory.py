from . import BCHWallet
from . import BTCWallet
from .wallet_exceptions import WalletException, WalletIsNotSupportedException

class WalletFactory:

    _SUPPORTED_WALLETS = [ BCHWallet, BTCWallet ]

    def get(self, ticker_symbol, username, password, rpc_url, port):
        '''
        Returns an instance of class that you can use to work with wallet. It is based on ticker_symbol param.
        '''
        if ticker_symbol is None:
            raise WalletException('Please define ticker symbol')
        found = [w for w in self._SUPPORTED_WALLETS if w.TICKER_SYMBOL == ticker_symbol.upper()]
        if len(found) == 0:
            raise WalletIsNotSupportedException()
        return found[0](username, password, rpc_url, port)
    
    def get_all_wallets(self):
        return [w() for w in self._SUPPORTED_WALLETS]