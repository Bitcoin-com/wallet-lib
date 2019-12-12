import pytest
from unittest.mock import patch

from unittest import TestCase
from wallet_lib import WalletFactory, BTCWallet, BCHWallet
from wallet_lib.wallet_exceptions import WalletException, WalletIsNotSupportedException


class WalletFactoryTest(TestCase):

    def test_get(self):
        btc_wallet_factory = WalletFactory().get('BTC')
        assert type(btc_wallet_factory) == BTCWallet

        btc_wallet_factory = WalletFactory().get('BCH')
        assert type(btc_wallet_factory) == BCHWallet

    def test_get_negative_wallet_exception(self):
        expected_result = 'Please define ticker symbol'
        with pytest.raises(WalletException) as excinfo:
            WalletFactory().get(None)

        assert expected_result == excinfo.value.reason

    def test_get_negative_wallet_not_support_exception(self):
        ticker_symbol = 'ABC'
        expected_result = '{} wallet is not supported'.format(ticker_symbol)
        with pytest.raises(WalletIsNotSupportedException) as excinfo:
            WalletFactory().get(ticker_symbol)
        
        assert expected_result == excinfo.value.reason
