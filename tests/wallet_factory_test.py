import pytest

from unittest import TestCase
from unittest.mock import patch
from wallet_lib import WalletFactory, BTCWallet, BCHWallet, WalletFactory, ZECWallet, DASHWallet
from wallet_lib.wallet_exceptions import WalletException, WalletIsNotSupportedException


class WalletFactoryTest(TestCase):

    def test_get_positive_supported_wallets(self):
        wallet_factory = WalletFactory()

        wallet_symbols = wallet_factory._SUPPORTED_WALLETS

        assert len(wallet_symbols) == 4

        assert wallet_symbols['BTC'] == BTCWallet

        assert wallet_symbols['ZEC'] == ZECWallet

        assert wallet_symbols['BCH'] == BCHWallet

        assert wallet_symbols['DASH'] == DASHWallet


    def test_get_positive(self):
        wallet_factory = WalletFactory()

        btc_wallet = wallet_factory.get('BTC')
        assert type(btc_wallet) == BTCWallet

        bch_wallet = wallet_factory.get('BCH')
        assert type(bch_wallet) == BCHWallet

        zec_wallet = wallet_factory.get('ZEC')
        assert type(zec_wallet) == ZECWallet

        dash_wallet = wallet_factory.get('DASH')
        assert type(dash_wallet) == DASHWallet

    def test_get_negative_wallet_not_support_exception(self):
        wallet_factory = WalletFactory()
        ticker_symbol = 'ABC'
        expected_result = '{} wallet is not supported'.format(ticker_symbol)
        with pytest.raises(WalletIsNotSupportedException) as excinfo:
            wallet_factory.get(ticker_symbol)
        
        assert expected_result == excinfo.value.reason

    def test_get_all_wallets(self):
        wallet_factory = WalletFactory()
        wallets = wallet_factory.get_all_wallets()
        assert 'BTC' in wallets
        assert 'BCH' in wallets
        assert 'DASH' in wallets
        assert 'ZEC' in wallets