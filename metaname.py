import functools
import json
import requests

ENDPOINT = 'https://test.metaname.net/api/1.1'
HEADERS = {'content-type': 'application/json'}

class Client(object):
    """JSON-RPC client for using the metaname api"""
    def __init__(self, account_reference, api_key):
        self.account_reference = account_reference
        self.api_key = api_key
        self.request_id = 0

    def __getattr__(self, attr):
        return functools.partial(self._request, attr)

    def _request(self, method, *args):
        """construct a request with the given method and params"""
        payload = self._construct_payload(method, *args)

        try:
            response = requests.post(ENDPOINT, data=payload,
                headers=HEADERS, verify=True)
        except requests.exceptions.RequestException as ex:
            print(ex)
            return

        try:
            response_payload = response.json()
        except ValueError as ex:
            print(ex)
            return

        return response_payload

    def _construct_payload(self, method, *args):
        """construct the request payload for a given method and params"""
        params = [self.account_reference, self.api_key]
        params.extend(args)

        payload = {'jsonrpc': '2.0'}
        payload['method'] = method
        payload['id'] = self.request_id
        payload['params'] = params

        return json.dumps(payload)

