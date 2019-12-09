class CMDCallerException(Exception):
    def __init__(self, reason=None):
        self.reason = reason


class WalletException(Exception):
    def __init__(self, reason=None):
        self.reason = reason


class WalletIsNotSupportedException(WalletException):
    def __init__(self):
        super().__init__(reason='Requested wallet is not supported')


class RPCCallerException(Exception):
    def __init__(self, reason=None):
        self.reason = reason
