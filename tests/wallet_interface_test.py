import pytest
from unittest.mock import patch

from unittest import TestCase
from wallet_base import WalletBase
from wallet_lib.wallet_exceptions import WalletException
from wallet_lib.wallet_interface import WalletInterface
from wallet_lib import WalletFactory

class WalletInterfaceTest(WalletBase, TestCase):

    def test_wallet_interface_inheritance(self):
        for ticker_symbol in WalletFactory.get_all_wallets():
            wallet = WalletFactory.get(ticker_symbol)

            assert WalletInterface in wallet.__class__.__bases__
            assert wallet.run != None

    def test_get_negative_wallet_interface_init_exception(self):
        expected_result = WalletException

        with pytest.raises(WalletException) as excinfo:
            WalletInterface()

        with pytest.raises(WalletException) as excinfo1:
            WalletInterface(None)

        assert expected_result == type(excinfo.value) == type(excinfo.value)
        assert excinfo.value.reason == excinfo1.value.reason