import nltk

from nltk.corpus import names
from nltk.tag import StanfordNERTagger
from nltk.parse.stanford import StanfordParser
from nltk.parse.stanford import StanfordDependencyParser

import spacy
from spacy.lang.en.examples import sentences
# import en_core_web_sm

import numpy as np

def extract_entity(text):
	tagger = StanfordNERTagger(model_filename='./stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',path_to_jar='./stanford-ner/stanford-ner.jar')

	text2 = text.split('.')

	name = []
	location = []
	organization = []

	for i in text2:
		for j in [',',';',':','!','~','?']:
			i = i.replace(j,'')
		result = tagger.tag(i.split())
		result = np.array(result)

		n = np.where(result=='PERSON')
		for j in n[0]:
			name.append(result[j][0])

		l = np.where(result=='LOCATION')
		for j in l[0]:
			location.append(result[j][0])

		o = np.where(result=='ORGANIZATION')
		for j in o[0]:
			organization.append(result[j][0])

	for i in name:
		print ("name:")
		print(i)

	for i in location:
		print ("location:")
		print(i)

	for i in organization:
		print ("organization:")
		print (i)

	return name, location, organization

def dependency(text):
	parser = StanfordDependencyParser(u"./stanford-ner/stanford-parser/stanford-parser.jar",u"./stanford-ner/stanford-parser/stanford-parser-3.6.0-models.jar",u"./stanford-ner/classifiers/englishPCFG.ser.gz")

	text2 = text.split('.')
	if text2[len(text2)-1]=='':
		text2 = text2[0:len(text2)-1]


	adj = []
	center = []

	for i in text2:
		for j in [',',';',':','!','~','?']:
			i = i.replace(j,'')
		rec = list(parser.parse(i.split()))
		j=0
		for row in rec[0].triples():
			print (row)
			if j==0:
				center.append(str(row[0][0]))
			j+=1

			if str(row[1]).find('amod')!=-1:
				adj.append(str(row[2][0]))

	for i in adj:
		print ('111')
		print (i)

	print ('222')
	print (center)

	return center, adj

def cleanup(token, lower = True):
	if lower:
		token = token.lower()
	return token.strip()

def extract_entity_spacy(text):
	nlp = spacy.load('en')

	doc = nlp(text.decode('utf8'))
	print(doc)

	name = []
	location = []
	organization = []

	for e in doc.ents:
		if e.label_==u'PERSON':
			name.append(e)
		elif e.label_==u'GPE':
			location.append(e)
		elif e.label_==u'ORG':
			organization.append(e)

	return name, location, organization

def dependency_spacy(text):
	nlp = spacy.load('en')
	doc = nlp(text.decode('utf8'))

	for np in doc.noun_chunks:
		print (np.text, np.root.dep_, np.root.head.text)

	text2 = [sent for sent in doc.sents if 'dog' in sent.string.lower()]


