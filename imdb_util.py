import pickle
from pathlib import Path

data_path = 'C:/Users/rodri/OneDrive/Documentos/python/data/' # it's the place where I'm storing the pickle data

def file_exists(filename):
	if Path(data_path+filename).is_file():
		return True
	else:
		return False

def save_pickle(data, filename):
	with open(data_path+filename, 'wb') as f:
		pickle.dump(data, f)

def get_pickle(filename):
	with open(data_path+filename, 'rb') as f:
		data = pickle.load(f)
	return data