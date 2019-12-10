from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import logging

from .wallet_adapter_base import WalletAdapterBase


class RPCAdapterException(Exception):
    def __init__(self, reason=None):
        self.reason = reason


class RPCAdapterResponse:

    def __init__(self, result, error=None, code=None):
        self.result = result
        self.error = error
        self.code = code


class RPCAdapter(WalletAdapterBase):
    def __init__(self, rpc_user, rpc_password, rpc_url, rpc_port):
        self.log = logging.getLogger('RPCCaller')
        self.rpc_url = rpc_url
        self.rpc_port = rpc_port
        self.rpc_user = rpc_user
        self.rpc_password = rpc_password

    def run(self, command, *args):
        try:
            rpc_connection = AuthServiceProxy(
                "http://%s:%s@%s:%s" % (self.rpc_user, self.rpc_password, self.rpc_url, self.rpc_port))
            try:
                response = rpc_connection.batch_(
                    self._build_args(command, *args))
            except Exception as e:
                return RPCAdapterResponse(None, e.message, e.code)
            return RPCAdapterResponse(response)
        except Exception as e:
            message = 'Failed to run {} command'.format(command)
            self.log.error(message, e)
            raise RPCAdapterException(reason=message)

    def _build_args(self, command, *args):
        data = list(args)
        data.insert(0, command)
        return [data]
