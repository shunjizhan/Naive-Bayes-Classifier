run: NaiveBayesClassifier
	./NaiveBayesClassifier training.txt testing.txt

test: NaiveBayesClassifier
	./NaiveBayesClassifier training.txt testing.txt | java -jar validate.jar