class WalletException(Exception):
    def __init__(self, reason=None):
        super().__init__(reason)

class WalletIsNotSupportedException(WalletException):
    def __init__(self):
        super().__init__(reason='Requested wallet is not supported')