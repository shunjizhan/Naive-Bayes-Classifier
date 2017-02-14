import sys

def readFile(filename):
	lines = [line.rstrip('\n').lower() for line in open(filename)]
	return lines

def readStopWords(n):
	stopwords = []
	f = open("stopwords")
	for i in range(n):
	    word = f.next().strip('\n')
	    stopwords.append(word)
	f.close()
	return stopwords

def deNoiseSentence(sentence):
	noise = readStopWords(20)
	words = sentence.split()
	resultwords  = [word for word in words if word not in noise]
	return [resultwords[:-1], resultwords[-1]]


def deNoise(file):	 
	return [deNoiseSentence(sentence) for sentence in file]






collection = readFile(sys.argv[1])	# contain paragrahs list 
collection = deNoise(collection)	# [ [['a','b'],'1'] , [['c','c'],'1'] , [['d','e'],'1'] ]
print collection
