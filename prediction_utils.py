import pandas as pd
import pickle

def encode_data(race, diabetic):
	race_encoder     = {'American Indian/Alaskan Native':0,'Asian':1,'Black':2,'Hispanic':3,'Other':4,'White':5}
	diabetic_encoder = {'No':0, 'No, borderline diabetes':1, 'Yes':2, 'Yes (during pregnancy)':3}

	encoded_race     = race_encoder[race]
	encoded_diabetic = diabetic_encoder[diabetic]

	return encoded_race, encoded_diabetic

def min_max_scaling(bmi, physical_health, mental_health, sleep_time):
	MAX_BMI             = 94.85
	MIN_BMI             = 12.02
	MAX_SLEEP_TIME      = 24.0
	MIN_SLEEP_TIME      = 1.0
	MAX_PHYSICAL_HEALTH, MAX_MENTAL_HEALTH = 30.0, 30.0
	MIN_PHYSICAL_HEALTH, MIN_MENTAL_HEALTH = 0.0, 0.0

	scaled_bmi 			   = (bmi - MIN_BMI) / (MAX_BMI - MIN_BMI)
	scaled_physical_health = (int(physical_health) - MIN_PHYSICAL_HEALTH) / (MAX_PHYSICAL_HEALTH - MIN_PHYSICAL_HEALTH)
	scaled_mental_health   = (int(mental_health) - MIN_MENTAL_HEALTH) / (MAX_MENTAL_HEALTH - MIN_MENTAL_HEALTH)
	scaled_sleep_time      = (int(sleep_time) - MIN_SLEEP_TIME) / (MAX_SLEEP_TIME - MIN_SLEEP_TIME)

	return scaled_bmi, scaled_physical_health, scaled_mental_health, scaled_sleep_time

def load_model():
	file = open("MyModel.h5", "rb")
	model = pickle.load(file) 
	return model

def predict(sex, age, race, height, weight, smoking, alcohol, general_health, sleep_time, mental_health, physical_health, physical_activity, diff_walking, stroke, diabetic, asthma, skin_cancer, kidney_disease):
	
	gen_health_dict = {"Poor":0, "Fair":1, "Good":2, "Very good":3, "Excellent":4}
	age_category_dict = {"18-24":0, "25-29":1, "30-34":2, "35-39":3, "40-44":4, "45-49":5, "50-54":6, "55-59":7, "60-64":8, "65-69":9, "70-74":10, "75-79":11, "80 or older": 12}
	bmi               = int(weight) / ((int(height)/100) **2)

	smoking           = 1 if smoking == "Yes"  else 0
	alcohol           = 1 if alcohol == "Yes"  else 0 
	stroke            = 1 if stroke == "Yes"  else 0
	diff_walking      = 1 if diff_walking == "Yes"  else 0
	physical_activity = 1 if physical_activity == "Yes"  else 0 
	asthma            = 1 if asthma == "Yes"  else 0
	kidney_disease    = 1 if kidney_disease == "Yes"  else 0
	skin_cancer       = 1 if skin_cancer == "Yes"  else 0
	sex               = 1 if sex == "Female"  else 0
	general_health    = gen_health_dict[general_health]
	age               = age_category_dict[age]
	race, diabetic    = encode_data(race, diabetic)
	bmi, physical_health, mental_health, sleep_time = min_max_scaling(bmi, physical_health, mental_health, sleep_time)

	df_dict = {"BMI": bmi, "Smoking":smoking, "AlcoholDrinking":alcohol, "Stroke": stroke, "PhysicalHealth": physical_health, "MentalHealth":mental_health, "DiffWalking":diff_walking, "Sex":sex, "AgeCategory":age, "Race":race, "Diabetic":diabetic, "PhysicalActiviy":physical_activity, "GenHealth":general_health, "SleepTime":sleep_time, "Asthma":asthma, "KidneyDisease":kidney_disease, "SkinCancer":skin_cancer}
	temp_df = pd.DataFrame(df_dict, index=[0])
	temp_df = temp_df.iloc[0]
	model = load_model()
	predict_proba = model.predict_proba([temp_df])[0][1] * 100

	return round(predict_proba, 2)
