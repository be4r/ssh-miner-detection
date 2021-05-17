#!/usr/bin/env python3

from sklearn.tree import DecisionTreeClassifier
import pickle
import numpy as np

no = [b'runc:[2:INIT]', b'containerssh-ag', b'apt',b'dpkg']


class model:
	def __init__(self):
		self.d = DecisionTreeClassifier()

	def load(self, filename = 'model.p'):
		try:
			f = open(filename, 'rb')
			self.d = pickle.load(f)
			if type(self.d) != DecisionTreeClassifier:
				d = None
			f.close()
		except:
			return

	def save(self, filename = 'model.p'):
		f = open(filename, 'wb')
		pickle.dump(self.d, f)
		f.close()

	def fit(self, x, y):
		self.d.fit(x, y)

	def predict(self, x):
		return self.d.predict(x)

	def accuracy(self, y_pred, y_ref):
		return sum(np.array(y_pred) == np.array(y_ref)) / len(y_ref)

	def f1(self, y_pred, y_ref):
		tp = (np.array(y_pred) == 1) *  (np.array(y_ref) == 1)
		tn = (np.array(y_pred) == 0) *  (np.array(y_ref) == 0)
		fp = (np.array(y_pred) == 1) *  (np.array(y_ref) == 0)
		fn = (np.array(y_pred) == 0) *  (np.array(y_ref) == 1)
		return tp / (tp + (fp + fn) / 2)

def ngrams(array, size = 25, overlacing = False):
	return [array[i:i+size] for i in range(0, len(array)//size * size, 1 if overlacing else size)]

	res = [array[i:i+size] for i in range(0, len(array)//size * size, 1 if overlacing else size)]
	if sum([len(i) == size for i in res]) != len(res):
		raise Exception('wtf')

def gen_train(a, is_miner):
	#x1,y1,x2,y2 = train_test_split(x,y,0.05)
	x = ngrams(a)
	y = [1 if is_miner else 0,] * len(x)
	
	return x,y

def train_on_logs(*filenames, is_miner):
	classifier = model()
	#classifier.load()
	x, y = [], []
	for id, filename in enumerate(filenames):
		l = []
		with open(filename, 'r') as f:
			l = eval(''.join(f))
		codes = []
		for i in l:
			if i[0] not in no:
				codes.append(i[1])
		x_, y_ = gen_train(codes, is_miner[id])
		x.append(x_)
		y.append(y_)
	print(x,y)
	#classifier.fit(x,y)
	#classifier.save()

def predict_on_logs(*filenames, is_miner):
	classifier = model()
	classifier.load()
	x, y = [], []
	for id, filename in enumerate(filenames):
		l = []
		with open(filename, 'r') as f:
			l = eval(''.join(f))
		codes = []
		for i in l:
			if i[0] not in no:
				codes.append(i[1])
		x_, y_ = gen_train(codes, is_miner[id])
		x.append(x_)
		y.append(y_)
	y_pred = classifier.predict(x)
	print("Accuracy: ", classifier.accuracy(y_pred, y))
	print("F1: ",classifier.f1(y_pred, y))


def predict_on_trace(trace, A = 0.9):
	classifier = model()
	classifier.load()
	x, y = [], []
	for id, filename in enumerate(filenames):
		codes = []
		for i in trace:
			if i[0] not in no:
				codes.append(i[1])
		x_, y_ = gen_train(codes, is_miner[id])
		x.append(x_)
		y.append(y_)
	y_pred = classifier.predict(x)
	acc = sum(np.array(y_pred)) / len(y_pred)
	return acc > A
