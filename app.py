import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from catboost import CatBoostRegressor

app = Flask(__name__)
CORS(app)

model = CatBoostRegressor()
model.load_model("catboost_model.cbm")

metro_coefs = pd.read_csv("metro_coefs.csv")  

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    
    metro_coef = metro_coefs.loc[
        metro_coefs['Metro station'] == data['metro'], 'Metro_coef'
    ].values[0]
    
    df = pd.DataFrame({
        'Area': [float(data['area'])],
        'Number of rooms': [int(data['rooms'])],
        'Metro_coef': [metro_coef],
        'Minutes to metro': [int(data['minutes'])],
        'Floor': [int(data['floor'])]
    })
    
    pred = np.expm1(model.predict(df)[0])
    return jsonify({'prediction': float(pred)})

if __name__ == '__main__':
    app.run(debug=True)