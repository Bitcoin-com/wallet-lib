import json

from abc import ABCMeta, abstractmethod
from .adapters import WalletAdapterBase
from .wallet_exceptions import WalletException
from .zmq_notifier import ZMQNotifier

class WalletBase(metaclass=ABCMeta):

    SUPPORTED_JSON_LOADS = [str, bytes, bytearray]

    def load_json(self, val):
        return json.loads(val) if type(val) in self.SUPPORTED_JSON_LOADS else val

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
        return ZMQNotifier(**kwargs)
