#!/usr/bin/env python
# coding: utf-8

# Machine Learning Project - Credit Card Lead Prediction
import pickle
import pandas as pd
import numpy as np
import xgboost as xgb
import opendatasets as od
import os

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import roc_auc_score

# Model Parameter Values
eta = 0.1
max_depth = 5
num_boost_round=75

output_file = 'lead_scoring_model.bin'

# load the data

dataset_url = 'https://www.kaggle.com/datasets/sajidhussain3/jobathon-may-2021-credit-card-lead-prediction' 
od.download(dataset_url)
data_dir = './jobathon-may-2021-credit-card-lead-prediction'
os.listdir(data_dir)
train_file_name = os.listdir(data_dir)[1]
train_df = pd.read_csv(f"{data_dir}/{train_file_name}")
df = train_df

# data preparation

# Dropping the ID column since this will not be important as part of our model
df = df.drop(['ID'], axis=1)

df.columns = df.columns.str.lower()

categorical_columns = list(df.dtypes[df.dtypes == 'object'].index)

numeric_columns = ['age', 'vintage', 'avg_account_balance']

df.credit_product = df.credit_product.fillna('Unknown')

# Log Transform of the avg_account_balance
avg_bal_logs = np.log1p(df.avg_account_balance)
df.avg_account_balance = np.log1p(df.avg_account_balance)

# splitting the data

df_full_train, df_test = train_test_split(df, test_size=0.2, random_state=1)

def train(df_train, y_train):
    dicts = df_train[categorical_columns + numeric_columns].to_dict(orient='records')

    dv = DictVectorizer(sparse=False)
    X_train = dv.fit_transform(dicts)
    dtrain = xgb.DMatrix(X_train, label=y_train,
                    feature_names=tuple(dv.get_feature_names_out()))

    model = xgb.train(xgb_params, dtrain, num_boost_round=num_boost_round)
    
    return dv, model


def predict(df, dv, model):
    dicts = df[categorical_columns + numeric_columns].to_dict(orient='records')

    X = dv.transform(dicts)
    dtest = xgb.DMatrix(X, feature_names=tuple(dv.get_feature_names_out()))

    y_pred = model.predict(dtest)

    return y_pred


# training the final model

print('training the final model')

# Final model:
xgb_params = {
    'eta': eta, 
    'max_depth': max_depth,
    'min_child_weight': 1, 

    'objective': 'binary:logistic',
    'eval_metric': 'auc',

    'nthread': 8,
    'seed': 1,
    'verbosity': 1,
}

dv, model = train(df_full_train, df_full_train.is_lead.values)
y_pred = predict(df_test, dv, model)

y_test = df_test.is_lead.values
auc = roc_auc_score(y_test, y_pred)

# validation

print(f'auc={auc}')

# Save the model

with open(output_file, 'wb') as f_out:
    pickle.dump((dv, model), f_out)

print(f'the model is saved to {output_file}')
