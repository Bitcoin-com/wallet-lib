class WalletException(Exception):

    def __init__(self, reason):
        self.reason = reason
        super().__init__(reason)

class WalletIsNotSupportedException(WalletException):
    
    def __init__(self, ticker_symbol):
        super().__init__('{} wallet is not supported'.format(ticker_symbol))