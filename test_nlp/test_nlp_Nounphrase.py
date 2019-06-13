import nltk
import os

from nltk.corpus import names
from nltk.tag import StanfordNERTagger
from nltk.parse.stanford import StanfordParser
from nltk.parse.stanford import StanfordDependencyParser
from collections import Counter

import spacy
from spacy.lang.en.examples import sentences
import en_core_web_sm

import numpy as np


def noun_chunks_spacy(text,score,total):
    nlp = spacy.load('en')
    doc = nlp(text.encode('utf8').decode('utf8'))
    result = []
    for chunk in doc.noun_chunks:
        doc2 = nlp(chunk.text)
        incorrect = False
        for i in doc2:
            if i.tag_ == 'PRP$' or i.pos_ == 'PRON' or i.pos_ == 'PROPN':
                incorrect = True
        if not incorrect:
            result.append(str(chunk.text))

    if len(result) == 0:
        return 0, result

    elif len(result) == 1:
        return 1, result[0]

    else:
        for i in result:
            if i.find("job") != -1:
                result.remove(i)
    score= score + len(result)

    return score, total, result

path = "D:\FYP\test_nlp\Jobtitles"
while path != "exit":
	path = raw_input()
	path1 = os.listdir(path)
	score = 0
	total = 0
	for i in path1:
		file = open(path + "\\" + i,"r")
		text = file.read()
		total = total + text.count('0')
		score, total, result = noun_chunks_spacy(text,score,total)
	print("Noun phrase recognised by Spacy: ", score)
	print("Total job titles: ", total)
	print("percentage:", (float(score)/float(total)))
	print(result)