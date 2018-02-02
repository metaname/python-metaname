#
# account_reference=$YOUR_ACCOUNT_REF api_key=$YOUR_API_KEY  python  account_balance.py
#

from metaname import Client as Metaname
import os

ENDPOINT = 'https://metaname.net/api/1.1'

account_reference = os.environ['account_reference']
api_key = os.environ['api_key']
metaname = Metaname(ENDPOINT, account_reference, api_key)

print metaname.account_balance()

