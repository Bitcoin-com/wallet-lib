from abc import ABCMeta, abstractmethod

from .adapters import WalletAdapterBase
from .wallet_exceptions import WalletException
from .zmq_notifier import ZMQNotifer

class WalletBase(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, *args): pass

    @abstractmethod
    def create_address(self, *args): pass

    @abstractmethod
    def get_balance(self): pass

    @abstractmethod
    def get_transaction(self, *args): pass

    @abstractmethod
    def get_transactions(self, *args): pass

    @abstractmethod
    def send(self, *args): pass

    @abstractmethod
    def get_transactions_since(self, *args): pass

    @abstractmethod
    def run(self, *args): pass

    def get_zmq_notifier(self, **kwargs):
        return ZMQNotifer(**kwargs)
