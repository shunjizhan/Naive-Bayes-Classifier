import sys

def readFile(filename):
	lines = [line.rstrip('\n').lower() for line in open(filename)]
	return lines

def deNoiseSentence(sentence):
	noise = ['the', 'a', 'an', 'i', 'that']

	words = sentence.split()
	resultwords  = [word for word in words if word not in noise]
	result = ' '.join(resultwords)

	return result


def deNoise(file):	 
	result = [deNoiseSentence(sentence) for sentence in file]
	return result





collection = readFile(sys.argv[1])	# contain paragrahs list 
collection = deNoise(collection)	
collection = [item.split('\t') for item in collection]	# now list of [{comment}, {score}]
print collection