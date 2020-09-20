import requests
import constant
import json
import os

from flask import Flask , redirect , url_for,render_template ,request ,send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS 
import xml.etree.ElementTree as ET

import time
import pandas as pd
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
global model
import numpy as np
import WeatherAndCloth_model

import pickle

# 파일을 업로드 할 폴더
UPLOAD_FOLDER = 'uploads/'
# 업로드 해도 되는 파일 
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg'])


from datetime import datetime


#start + config 
app = Flask(__name__ , template_folder = 'templates')
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

def dayNameFromWeekday(weekday):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return days[weekday]

@app.route("/survey" , methods = ['POST'])
def survey():
	req = requests.get(constant.url_weather_api + constant.city_ids.get("Seoul-teukbyeolsi"))

	if req.status_code == 200:
		resp = json.loads(req.text)
		text = json.dumps(resp)
		
		if request.form.get("goodButton") == "1" :
			result = request.form.get("goodButton")
		else:
			result = request.form.get("badButton")

		clothe = request.form.get("cloth")
		curtemp = int(resp["main"]["temp"])
		mintemp = int(resp["main"]["temp_min"])
		maxtemp = int(resp["main"]["temp_max"])
		windspeed = round(resp["wind"]["speed"])

		f1 = open('data.csv','a')	
		#f1.write(resp["name"]+",")
		#f1.write(resp["weather"][0]["icon"]+",")
		#f1.write(resp["weather"][0]["main"]+",")
		f1.write(str(resp["main"]["temp"])+",")
		#f1.write(str(resp["maint"]["temp_min"])+",")
		#f1.write(str(resp["main"]["temp_max"])+",")

		f1.write(str(resp["wind"]["speed"])+",")
		feel_temp =13.12+(0.6215*curtemp)-11.37*pow(windspeed,0.16)+0.3965*pow(windspeed,0.16)*curtemp
		f1.write(str(round(feel_temp))+",")
		f1.write(str(clothe)+",")
#		f1.write(str(result))
#		f1.write("\n")
		pred = predict().get(0)
		f1.write(str(pred))
		f1.write("\n")
		f1.close()

		return redirect("/")



@app.route("/")
def weatherJsonRequest():
	req = requests.get(constant.url_weather_api + constant.city_ids.get("Seoul-teukbyeolsi"))
	if req.status_code == 200:
		#f = open("./static/test.json",'w')
		with open('static/data.json','w') as outfile:
			json.dump(req.text, outfile)
		resp = json.loads(req.text)
		cityname = resp["name"]
		icon = resp["weather"][0]["icon"]
		main = resp["weather"][0]["main"]
		curtemp = int(resp["main"]["temp"])
		mintemp = int(resp["main"]["temp_min"])
		maxtemp = int(resp["main"]["temp_max"])
		windspeed = round(resp["wind"]["speed"])
		
	else:
		exit(0)
	return render_template("upload.html", **locals())

# 파일이 허용되는가? 
def allowed_file(filename):
	return  '.' in filename and \
		filename.rsplit('.',1)[1] in app.config['ALLOWED_EXTENSIONS']

def predict():

	pipe = joblib.load('./model/model.pkl')

	pr = pd.read_csv("set_to_predict.csv")
	pred_cols = list(pr.columns.values)[:4]

	pred = pd.Series(pipe.predict(pr[pred_cols]))
	print(pred) 
	return pred

@app.route('/classification/<result>')
def classification(result):
	
	req = requests.get(constant.url_weather_api + constant.city_ids.get("Busan"))
	resp = json.loads(req.text)
	cityname = resp["name"]
	icon = resp["weather"][0]["icon"]
	main = resp["weather"][0]["main"]
	curtemp = int(resp["main"]["temp"])		
	mintemp = int(resp["main"]["temp_min"])
	maxtemp = int(resp["main"]["temp_max"])
	windspeed = round(resp["wind"]["speed"])
	feel_temp =13.12+(0.6215*curtemp)-11.37*pow(windspeed,0.16)+0.3965*pow(windspeed,0.16)*curtemp
	
	f = open("set_to_predict.csv", 'w')
	f.write("temp,windspeed,feel_temp,clothe,result\n")
	f.write(str(curtemp)+",")
	f.write(str(windspeed)+",")
	f.write(str(feel_temp)+",")
	if str(result) == "coat":
		f.write(str(1)+",")
	elif str(result) == "padding":
		f.write(str(2)+",")	
	elif str(result) =="short":
		f.write(str(3)+",")
	elif str(result) =="shirt":
		f.write(str(4)+",")
	else :
		f.write(str(5)+",")
	f.close()
	prediction = str(predict().get(0))
	f1 = open("set_to_predict.csv", 'a')
	f1.write(prediction)
	print("prediction is " + prediction)
	
	return render_template('result.html' , **locals())


# 파일 업로드 하기
@app.route("/upload" , methods =['POST'])
def upload():
	# 업로드 할 파일 이름 가져오기 
	file = request.files['file']
	# 파일 체크 하기 
	if file and allowed_file(file.filename):
		# 지원 되지 않는 chars etc 를 제거 해준다. 
		filename = secure_filename(file.filename)
		# path 를 저장 한다. 
		save_to = os.path.join(app.config['UPLOAD_FOLDER'],filename)
		# save file 
		file.save(save_to)
		# model 에 파일을 전달해주고 bool 을 받아 온다. 
		is_coat = WeatherAndCloth_model.is_coat(save_to)
		return redirect(url_for('classification', result = is_coat))

# 파일이 업로도 되어있는지 확인
@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

if __name__ =='__main__':
	app.run(debug = True , host = "0.0.0.0", port = int(os.getenv('VCAP_APP_PORT','10000')))
