import os

for i in range (0, 200, 15):
	os.system("python AI.py temp/training.txt temp/testing.txt " + str(i))