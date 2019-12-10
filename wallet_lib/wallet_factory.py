from . import BCHWallet, BTCWallet
from .wallet_exceptions import WalletException, WalletIsNotSupportedException
from .adapters import RPCAdapter, WalletAdapterBase


class WalletFactory:

    _SUPPORTED_WALLETS = {
        'BCH': BCHWallet,
        'BTC': BTCWallet
    }

    def __init__(self):
        pass

    def get(self, ticker_symbol, adapter: WalletAdapterBase):
        '''
        Returns an instance of class that you can use to work with wallet. It is based on ticker_symbol param.
        '''

        if ticker_symbol is None:
            raise WalletException('Please define ticker symbol')
        wallet = self._SUPPORTED_WALLETS.get(ticker_symbol.upper(), None)
        if wallet is None:
            raise WalletIsNotSupportedException(ticker_symbol.upper())
        return wallet(adapter)

    def get_all_wallets(self):
        return [w() for w in self._SUPPORTED_WALLETS]
