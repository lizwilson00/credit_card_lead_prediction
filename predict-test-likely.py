#!/usr/bin/env python
# coding: utf-8

import requests

# EB
# host = 'lead-serving-env.eba-ikvs6hvr.ap-southeast-1.elasticbeanstalk.com'
# url = 'http://localhost:9696/predict'

# Local
host = 'localhost:9696'
url = f'http://{host}/predict'

customer = {'gender': 'Male',
    'region_code': 'RG269',
    'occupation': 'Self_Employed',
    'channel_code': 'X2',
    'credit_product': 'Unknown',
    'is_active': 'Yes',
    'age': 54,
    'vintage': 63,
    'avg_account_balance': 13.851664072068086}


response = requests.post(url, json=customer).json()
print(response)

if response['is_lead'] == True:
    print('This customer is a good lead')
else:
    print('This customer is not a good lead')
