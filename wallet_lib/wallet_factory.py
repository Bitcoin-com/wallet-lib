from . import BCHWallet, BTCWallet, DASHWallet, ZECWallet
from .wallet_exceptions import WalletException, WalletIsNotSupportedException
from .adapters.wallet_adapter_base import WalletAdapterBase
from .adapters.rpc_adapter import RPCAdapter


class WalletFactory:

    _SUPPORTED_WALLETS = [BCHWallet, BTCWallet, DASHWallet, ZECWallet]

    @staticmethod
    def get(ticker_symbol, adapter: WalletAdapterBase = RPCAdapter()):
        '''Returns a wallet instance based on 'ticker_symbol' that you can use to work with your local wallet.'''
        for wallet in WalletFactory._SUPPORTED_WALLETS:
            if wallet.TICKER_SYMBOL == ticker_symbol: return wallet(adapter)
        raise WalletIsNotSupportedException(ticker_symbol)

    @staticmethod
    def get_all_wallets():
        return [wallet.TICKER_SYMBOL for wallet in WalletFactory._SUPPORTED_WALLETS]