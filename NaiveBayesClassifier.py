import sys
import math
import time

global frequencyLib
global frequencyLib1
global frequencyLib0

global total
global total1
global total0

global totalScore
global pos
global neg

global trainingTime
global testingTime


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
	# noise = readStopWords(int(sys.argv[3]))
	noise = readStopWords(75)
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
	# print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
	# print pos, neg
	one = two = 0
	positive = math.log(pos, 2)
	negative = math.log(neg, 2)
	# positive = 0
	# negative = 0
	for word in comment:
		if (word != '1' and word != '0' and frequencyLib.has_key(word)):			# library contains this word
			if (frequencyLib1.has_key(word) and frequencyLib0.has_key(word)):		# both contain
				pWord1 = float(frequencyLib1[word]) / total1
				pWord0 = float(frequencyLib0[word]) / total0
			elif(frequencyLib1.has_key(word)):										# only 1 contains
				pWord1 = float(frequencyLib1[word]) / total1
				pWord0 = pWord1 / 10		# assign weight to 1/10
			else:																	# only 0 contains
				pWord0 = float(frequencyLib0[word]) / total0
				pWord1 = pWord0 / 10		# assign weight to 1/10

			positive += math.log(pWord1, 2) 
			negative += math.log(pWord0, 2)	
			# print positive, negative	

	if(positive > negative):
		return 1
	else:
		return 0	

def test(num):
	if (num == 0):
		testData = deNoise(readFile(sys.argv[1]))
	else:
		testData = deNoise(readFile(sys.argv[2]))
	comment = []
	realScore = []
	predictScore = []
	for oneComment in testData:
		comment.append(oneComment[:-1])
		realScore.append(int(oneComment[-1]))
		predictScore.append(predict(oneComment[:-1]))
	# print 'commnet: ', comment		
	# print 'realScore: ', realScore
	# print 'predictsc: ', predictScore

	compare(realScore, predictScore, num)


def compare(li1, li2, num):
	# print 'compare ', num
	right = 0
	wrong = 0
	for i in range (len(li1)):
		print li2[i]
		if(li1[i] == li2[i]):
			right += 1
		else:
			wrong += 1

	# print "n: {0}".format(sys.argv[3]),
	# print "right: {0}".format(right),
	# print "wrong: {0}".format(wrong),
	if (num == 0):
		global trainingAccu
		trainingAccu = format(float(right) / (right + wrong), '.3f')
		# print trainingAccu
	else :
		global testingAccu
		testingAccu = format(float(right) / (right + wrong), '.3f')
		# print testingAccu



#~~~~~~~~~~ Main ~~~~~~~~~~#
trainStart = time.time()

trainData = deNoise(readFile(sys.argv[1]))	# [   ['a','b','1'] , ['c','c','0'] , ['d','e','1']   ]
#collection = deNoise(collection)	# [   [['a','b'],'1'] , [['c','c'],'0'] , [['d','e'],'1']   ]



frequencyLib = buildLib(trainData)		# whole library
freqLibSep = seperateData(trainData)	
# print freqLibSep[0], freqLibSep[1]

frequencyLib1 = buildLib(freqLibSep[0])
frequencyLib0 = buildLib(freqLibSep[1])

total = countTotal(frequencyLib)		# total words
total1 = countTotal(frequencyLib1)		# total words | 1
total0 = countTotal(frequencyLib0)		# total words | 0

totalScore = float(frequencyLib['1']) + float(frequencyLib['0'])
pos = float(frequencyLib['1']) / totalScore		# p(1)
neg = float(frequencyLib['0']) / totalScore		# p(0)

trainingTime = int(time.time() - trainStart)

testStart = time.time()
test(0)
test(1)
testingTime = int(time.time() - testStart)

print trainingTime, 'seconds (training)'
print testingTime, 'seconds (labeling)'
print trainingAccu, '(training)'
print testingAccu, '(testing)'



