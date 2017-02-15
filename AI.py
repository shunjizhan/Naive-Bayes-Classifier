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
	noise = readStopWords(50)
	words = sentence.split()
	words = [strip(word) for word in words]	# strip punctuation
	resultwords  = [word for word in words if word not in noise]	# denoise
	# return [resultwords[:-1], resultwords[-1]]
	return resultwords

def deNoise(file):	 
	return [deNoiseSentence(sentence) for sentence in file]

def buildLib(collection):
	dictionary  = {}
	for li in collection:
		for word in li:
			if (dictionary.has_key(word)):
				dictionary[word] = dictionary.get(word) + 1
			else: 
				dictionary[word] = 1

	# print "built succeed!"
	return dictionary

def strip(word):
	return word.replace('.', '').replace(',', '').replace('!', '').replace('?', '').replace(':', '').replace('(', '').replace(')', '').replace('<', '').replace('>', '').replace('/', '').replace('\'s', '').replace('ing', '').replace('ed', '').replace('\"', '').replace('\'', '').replace('\'d', '').replace('.<br', '').replace('[', '').replace(']', '').replace('*', '')

def seperateData(data):		# data: [   ['a','b','1'] , ['c','c','1'] , ['d','e','1']   ]
	data1 = []
	data0 = []
	for li in data:
		if (li[-1] == '1'):
			data1.append(li)
		else: 
			data0.append(li)
	return [data1, data0]

def countTotal(lib):
	sum = 0
	for key in lib:
		sum += lib[key]

	return sum

def predict(comment):	# comment: [  ['a','b'] , ['c','c'] , ['d','e']  ]
	pos = 0
	neg = 0
	total = countTotal(frequencyLib)
	total1 = countTotal(frequencyLib1)
	total0 = countTotal(frequencyLib0)

	totalScore = float(frequencyLib['1']) + float(frequencyLib['0'])
	p1 = float(frequencyLib['1']) / totalScore
	p0 = float(frequencyLib['0']) / totalScore

	print p1 + p0
	
	return 0


def test():
	testData = deNoise(readFile(sys.argv[2]))
	comment = []
	realScore = []
	predictScore = []
	for oneComment in testData:
		comment.append(oneComment[:-1])
		realScore.append(int(oneComment[-1]))
		predictScore.append(predict(oneComment[:-1]))
	print 'commnet: ', comment		
	print 'realScore: ', realScore
	print 'predictsc: ', predictScore


#~~~~~~~~~~ Main ~~~~~~~~~~#
trainData = deNoise(readFile(sys.argv[1]))	# [   ['a','b','1'] , ['c','c','1'] , ['d','e','1']   ]
#collection = deNoise(collection)	# [   [['a','b'],'1'] , [['c','c'],'1'] , [['d','e'],'1']   ]

global frequencyLib
global frequencyLib1
global frequencyLib0

frequencyLib = buildLib(trainData)			# print frequencyLib.items()
freqLibSep = seperateData(trainData)
frequencyLib1 = buildLib(freqLibSep[0])
frequencyLib0 = buildLib(freqLibSep[1])

test()






