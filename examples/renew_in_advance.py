#
# Performs advance renewals of domain names that are coming to term soon.
#
# Use:
#
#     account_reference=$YOUR_ACCOUNT_REF api_key=$YOUR_API_KEY  python3  renew_in_advance.py
#

from metaname import Client as Metaname
import os
from datetime import datetime


RENEW_DAYS_PRIOR = 28


#ENDPOINT = 'https://metaname.net/api/1.1'
# NOTE: Earlier versions of Python do not support SNI
ENDPOINT = 'https://test.metaname.net/api/1.1'

account_reference = os.environ['account_reference']
api_key = os.environ['api_key']
metaname = Metaname(ENDPOINT, account_reference, api_key)


def pluralise(n, name):
  return ('%i %s' if n == 1 else '%i %ss')% (n, name)


# Go through all domains
for domain in metaname.domain_names():
  print('  %s'% domain['name'])

  # Work out how many days until domain's term is up
  when_paid_up_to = datetime.strptime(domain['when_paid_up_to'], '%Y-%m-%dT%H:%M:%S')
  days_to_term = (when_paid_up_to - datetime.now()).days

  # auto_renew_term is not provided by domain_names(), hence:
  domain = metaname.domain_name(domain['name'])
  auto_renew_term = domain['auto_renew_term']
  print('    days_to_term %i  auto_renew %s'% (days_to_term, auto_renew_term != 0))

  # Names should be renewed names only if they have not expired and not been
  # configured to expire
  if domain['status'] == 'Active' and 0 < days_to_term < RENEW_DAYS_PRIOR and auto_renew_term != 0:
    print('    Renewing for  %s'% pluralise(auto_renew_term, 'month'))
    metaname.renew_domain_name(domain['name'], auto_renew_term)
    # Should show the new term end
    domain = metaname.domain_name(domain['name'])
    print('    New term ends ', domain['when_paid_up_to'])

