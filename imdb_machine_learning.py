import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing, cross_validation, svm

def start(data, prediction_data):
	# get features and label
	X, y = setup_data_and_label(data)
	
	# scale X before fit the data
	X = preprocessing.scale(X)
	
	# split our data
	# 20% of the data will be used for testing
	X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)
	
	clf = LinearRegression()
	# fit the training data (already processed and scaled) to our model
	clf.fit(X_train, y_train)

	#accuracy
	accuracy = clf.score(X_test, y_test)

	# predicting the testing data
	predictions = clf.predict(X_test)
	print(accuracy, predictions)
	
	# use the prediction_data to predict
	prediction_data.drop(['movie_title', 'plot_keywords'], 1, inplace=True)
	data = np.array(prediction_data)
	data = preprocessing.scale(data)
	predictions_2 = clf.predict(data)

	print(predictions_2)

def setup_data_and_label(df):
	df.drop(['movie_title', 'plot_keywords'], 1, inplace=True)

	# X - features, y - label
	X = np.array(df.drop(['imdb_score'], 1))
	y = np.array(df['imdb_score'], dtype='float64')
	
	return X, y

