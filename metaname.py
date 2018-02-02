import functools
import json
import requests

HEADERS = {'content-type': 'application/json'}

class Client(object):
    """JSON-RPC client for using the metaname api"""
    def __init__(self, endpoint, account_reference, api_key):
        self.endpoint = endpoint
        self.account_reference = account_reference
        self.api_key = api_key
        self.request_id = 0

    def __getattr__(self, attr):
        return functools.partial(self._request, attr)

    def _request(self, method, *args):
        """construct a request with the given method and params"""
        payload = self._construct_payload(method, *args)

        try:
            response = requests.post(self.endpoint, data=payload,
                headers=HEADERS, verify=True)
        except requests.exceptions.RequestException as ex:
            print(ex)
            return

        try:
            response_payload = response.json()
            #{u'jsonrpc': u'2.0', u'result': u'-662.69', u'id': 0}
            #{u'jsonrpc': u'2.0', u'id': 0, u'error': {u'message': u'Invalid
            # params', u'code': -32602, u'data': u'Wrong number of params'}}
            try:
                return response_payload['result']
            except KeyError:
                raise Exception(response_payload['error'])
        except ValueError as ex:
            print(ex)
            return

    def _construct_payload(self, method, *args):
        """construct the request payload for a given method and params"""
        params = [self.account_reference, self.api_key]
        params.extend(args)

        payload = {'jsonrpc': '2.0'}
        payload['method'] = method
        payload['id'] = self.request_id
        self.request_id += 1
        payload['params'] = params

        return json.dumps(payload)

