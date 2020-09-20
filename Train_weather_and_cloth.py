import time
import pandas as pd
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
global model
import numpy as np
from sklearn.model_selection import train_test_split
import pickle

model_directory = 'model'
model_file_name = '%s/model.pkl' % model_directory
model_columns_file_name = '%s/model_columns.pkl' % model_directory


# 옷 과 날씨 정보 에 따른 적합도를 training 하는 함수.
def train():
	dataset = pd.read_csv('data.csv')
#	outcome = dataset['result']
	y = dataset.pop('result')
	X = dataset[dataset.columns[:4]]
	
	X_train , X_test , y_train , y_test = train_test_split(X,y ,test_size = 0.2 , random_state=0)
#	data = dataset[dataset.columns[:3]]
#	data = dataset.columns[2:3]
	model = LogisticRegression()
	start = time.time()
	model.fit(X_train ,y_train)
	
	print("Trained in %.1f seconds",(time.time() - start))
	print("Model training score: %s", model.score(X_test , y_test))
	final_predict = model.predict(X_test)
	final_predict = np.array(final_predict, dtype = int)
	
	print(final_predict)
	joblib.dump(model , model_file_name)
	print("Training finished.")
	return final_predict[-1]

train()
