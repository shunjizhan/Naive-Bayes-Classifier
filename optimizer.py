import os

for i in range (0, 200, 15):
	os.system("python NaiveBayesClassifier.py training.txt testing.txt " + str(i))