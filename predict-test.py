#!/usr/bin/env python
# coding: utf-8

import requests

# EB
# host = 'lead-serving-env.eba-ikvs6hvr.ap-southeast-1.elasticbeanstalk.com'
# url = 'http://localhost:9696/predict'

# Local
host = 'localhost:9696'
url = f'http://{host}/predict'

customer = {'gender': 'Female',
    'region_code': 'RG269',
    'occupation': 'Other',
    'channel_code': 'X1',
    'credit_product': 'No',
    'is_active': 'No',
    'age': 36,
    'vintage': 27,
    'avg_account_balance': 12.727015912884449}


response = requests.post(url, json=customer).json()
print(response)

if response['is_lead'] == True:
    print('This customer is a good lead')
else:
    print('This customer is not a good lead')
