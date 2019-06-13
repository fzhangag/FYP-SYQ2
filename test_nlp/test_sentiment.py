import spacy
from spacy.lang.en.examples import sentences
import en_core_web_sm
from spacy.tokens import Doc
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import os

nlp = spacy.load('en')


sentiment_analyzer = SentimentIntensityAnalyzer()
def polarity_scores(doc):
    return sentiment_analyzer.polarity_scores(doc.text)
Doc.set_extension('polarity_scores', getter=polarity_scores)

text = "are you ok?"
pos = 0
neg = 0 
neu = 0
sum = 0

while text != "exit":
	path = raw_input()
	path1 = os.listdir(path)
	for i in path1:
		file = open(path + "\\" + i,"r")
		text = file.read()
		doc = nlp(text.decode('utf8'))
		dict = doc._.polarity_scores
		score = dict.get('compound')
		if score > 0 :
			pos = pos + 1
		elif score == 0 :
			neu = neu + 1
		else:
			neg = neg + 1
	print(pos)
	print(neu)
	print(neg)



