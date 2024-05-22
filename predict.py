import pickle
import xgboost as xgb

from flask import Flask
from flask import request
from flask import jsonify


model_file = 'lead_scoring_model.bin'

with open(model_file, 'rb') as f_in:
    dv, model = pickle.load(f_in)

app = Flask('lead')

def lead_probability(customer):
    X = dv.transform([customer])
    dtest = xgb.DMatrix(X, feature_names=tuple(dv.get_feature_names_out()))
    y_pred = model.predict(dtest)[0]
    return y_pred

@app.route('/predict', methods=['POST'])
def predict():
    customer = request.get_json()
    cust_lead_prob = lead_probability(customer)
    is_lead = cust_lead_prob >= 0.5

    result = {
        'lead_probability': round(float(cust_lead_prob), 3),
        'is_lead': bool(is_lead)
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)