from flask import Flask, render_template, request
import joblib
import numpy as np
import json



app = Flask(__name__)
app.config['SECRET_KEY'] = "somekey"

model = joblib.load('air_quality_linear_reg.pkl')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/table')
def table():
    tables = {

        "0-100": "Safe",
        "100-200": "Satisfactory",
        "200-300": "Moderate",
        "300-400": "Poor",
        "400-500": "Very Poor",
        "500-600": "Severe",
        "600 and above": "Fatal"
    }
    return render_template('table.html',tables = tables)


@app.route('/predict', methods = ['POST', 'GET'])
def predict():
    features = [float(x) for x in request.form.values()]
    final = [np.array(features, dtype = 'float')]

    pred = int(model.predict(final))

    quality = 'Safe'
    if 0 < pred <= 100:
        quality = 'Safe'
    elif 100 < pred <= 200:
        quality = 'Satisfactory'
    elif 200 < pred <= 300:
        quality = 'Moderate'
    elif 300 < pred <= 400:
        quality = 'Poor'
    elif 400 < pred <= 500:
        quality = 'Very Poor'
    elif 500 < pred <= 600:
        quality = 'Severe'
    else:
        quality = 'Fatal'
    params = 'Air Quality index is {}.\nThus it is {}'.format(pred, quality)
    return render_template('index.html', params = params)


if __name__ == '__main__':
    app.run(debug = True)
