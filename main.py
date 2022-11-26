from flask import Flask, render_template, request
from prediction_utils import *

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/prediction', methods=["GET", "POST"])
def get_prediction():
	name              = request.values.get('name')
	sex               = request.values.get('sex')
	age               = request.values.get('age')
	race              = request.values.get('race')
	height            = request.values.get('height')
	weight            = request.values.get('weight')
	smoking           = request.values.get('smoking')
	alcohol           = request.values.get('alcohol')
	general_health    = request.values.get('general_health')
	sleep_time        = request.values.get('sleep_time')
	mental_health     = request.values.get('mental_health')
	physical_health   = request.values.get('physical_health')
	physical_activity = request.values.get('physical_activity')
	diff_walking      = request.values.get('diff_walking')
	stroke            = request.values.get('stroke')
	diabetic          = request.values.get('diabetic')
	asthma            = request.values.get('asthma')
	skin_cancer       = request.values.get('skin_cancer')
	kidney_disease    = request.values.get('kidney_disease')

	model_prediction = predict(sex, age, race, height, weight, smoking, alcohol, general_health, sleep_time, mental_health, physical_health, physical_activity, diff_walking, stroke, diabetic, asthma, skin_cancer, kidney_disease)
	return render_template('prediction.html', name=name, heart_risk_rate=f"{model_prediction}%")

app.run(debug=True)