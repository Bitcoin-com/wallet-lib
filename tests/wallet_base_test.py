import pytest
import abc

from unittest.mock import patch
from unittest import TestCase
from wallet_base import WalletBase
from wallet_lib.wallet_exceptions import WalletException
from wallet_lib.wallet_base import WalletBase
from wallet_lib import WalletFactory

class WalletBaseTest(TestCase):

    def test_get_positive_wallet_base_inheritance(self):
        wallet_facory = WalletFactory()
        for ticker_symbol in wallet_facory.get_all_wallets():
            wallet = wallet_facory.get(ticker_symbol)
            assert WalletBase in wallet.__class__.__bases__

    def test_get_positive_wallet_base_parent(self):
        assert WalletBase.__class__ == abc.ABCMeta

    def test_get_negative_wallet_base_initiate(self):
        try:
            WalletBase()
            assert False
        except TypeError:
            assert True
        except Exception:
            assert False

        try:
            WalletBase(1,2,3)
            assert False
        except TypeError:
            assert True
        except Exception:
            assert False