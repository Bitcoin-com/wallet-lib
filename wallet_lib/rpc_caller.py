import logging
import subprocess
import requests
import json

from .wallet_exceptions import RPCCallerException


class RPCCallerResponse:

    def __init__(self, response, code):
        self.result = response['result']
        self.code = code
        self.error = response['error']
        if(response['error'] != None):
            self.error = response['error']['message']
            self.code = response['error']['code']


class RPCCaller:

    def __init__(self, username, password, rpc_url, port):
        self.log = logging.getLogger('RPCCaller')
        self.rpc_url = rpc_url
        self.port = port
        self.username = username
        self.password = password
        self.headers = {'content-type': 'application/json'}

    def run(self, command, *args):
        try:
            response = requests.post(self.rpc_url+':'+self.port,
                                     data=self._build_data(command, *args),
                                     headers=self.headers,
                                     auth=(self.username, self.password))
            return RPCCallerResponse(response.json(), response.status_code)
        except Exception as e:
            message = 'Failed to run {} command'.format(command)
            self.log.error(message, e)
            raise RPCCallerException(reason=message)

    def _build_data(self, command, *args):
        data = {
            'method': command,
            'params': list(args),
            'jsonrpc': '1.0',
        }
        return json.dumps(data)
