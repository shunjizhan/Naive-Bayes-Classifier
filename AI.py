import sys

for arg in sys.argv:
    print arg

def readFile(filename):
	lines = [line.rstrip('\n').split('\t') for line in open(filename)]
	return lines

print readFile(sys.argv[1])