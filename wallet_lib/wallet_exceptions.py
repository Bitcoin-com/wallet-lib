class WalletException(Exception):
    def __init__(self, reason=None):
        self.reason = reason

class WalletIsNotSupportedException(WalletException):
    def __init__(self, ticker_symbol):
        super().__init__(reason='{} wallet is not supported'.format(ticker_symbol))