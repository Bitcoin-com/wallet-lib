import pytest
from unittest.mock import patch

from unittest import TestCase
from wallet_lib import WalletFactory, BTCWallet, BCHWallet, WalletFactory, ZECWallet, DASHWallet
from wallet_lib.wallet_exceptions import WalletException, WalletIsNotSupportedException


class WalletFactoryTest(TestCase):

    def test_get_positive(self):
        btc_wallet_factory = WalletFactory.get('BTC')
        assert type(btc_wallet_factory) == BTCWallet

        btc_wallet_factory = WalletFactory.get('BCH')
        assert type(btc_wallet_factory) == BCHWallet

        btc_wallet_factory = WalletFactory.get('ZEC')
        assert type(btc_wallet_factory) == ZECWallet

        btc_wallet_factory = WalletFactory.get('DASH')
        assert type(btc_wallet_factory) == DASHWallet

    def test_get_negative_wallet_not_support_exception(self):
        ticker_symbol = 'ABC'
        expected_result = '{} wallet is not supported'.format(ticker_symbol)
        with pytest.raises(WalletIsNotSupportedException) as excinfo:
            WalletFactory.get(ticker_symbol)
        
        assert expected_result == excinfo.value.reason

    def test_get_all_wallets(self):
        wallets = WalletFactory.get_all_wallets()
        assert 'BTC' in wallets
        assert 'BCH' in wallets
        assert 'DASH' in wallets
        assert 'ZEC' in wallets