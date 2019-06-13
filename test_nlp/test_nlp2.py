import nltk

from nltk.corpus import names
from nltk.tag import StanfordNERTagger
from nltk.parse.stanford import StanfordParser
from nltk.parse.stanford import StanfordDependencyParser

import spacy
from spacy.lang.en.examples import sentences
import en_core_web_sm

# https://polyglot.readthedocs.io/en/latest/NamedEntityRecognition.html
# download model from internet

import numpy as np


def extract_entity():
	tagger = StanfordNERTagger(model_filename='./stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',path_to_jar='./stanford-ner/stanford-ner.jar')
	text="""Rudy Harris and Kobi Reynolds and Dominic Fletcher and Natan Read and Aaron Bradley and Kit Robertson and Samuel Cole and Percy Knight and Billy Ryan and Robbie Kennedy and  and Aron Green and Eden Byrne and Grayson Thompson and Levi Bell and Darius Taylor and Dennis Harper and Ashton Bates and Alan Murphy and Tobias Cole and Dominic Hamilton and  and Caelan Scott and Adam Nicholson and Rupert Lloyd and Cameron Butler and Erik Kennedy and Euan Taylor and Gabriel Cooke and Oskar Lawrence and Aston Hunter and Dominic Hawkins and  and Franklin Burke and Robin Johnston and Benedict Thomson and Mason Howard and Douglas Stone and Kairo Palmer and Ralph Shaw and Haris Riley and Kane Watson and Christopher Bates and  and Toby Woods and Bertie Fletcher and Levi Wilson and Edison Hawkins and Hector Jordan and Phoenix Edwards and Heath Thompson and Zac Clarke and Ewan Poole and Evan Reynolds"""
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
		print "name:"
		print(i)

	for i in location:
		print "location:"
		print(i)

	for i in organization:
		print "organization:"
		print i

	return name, len(name), location, len(location), organization, len(organization)

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
			print row
			if j==0:
				center.append(str(row[0][0]))
			j+=1

			if str(row[1]).find('amod')!=-1:
				adj.append(str(row[2][0]))

	for i in adj:
		print '111'
		print i

	print '222'
	print center

	return center, adj

def cleanup(token, lower = True): 
	if lower: 
		token = token.lower() 
	return token.strip() 

def extract_entity_spacy():
	nlp = spacy.load('en')
	text="""Rudy Harris and Kobi Reynolds and Dominic Fletcher and Natan Read and Aaron Bradley and Kit Robertson and Samuel Cole and Percy Knight and Billy Ryan and Robbie Kennedy and  and Aron Green and Eden Byrne and Grayson Thompson and Levi Bell and Darius Taylor and Dennis Harper and Ashton Bates and Alan Murphy and Tobias Cole and Dominic Hamilton and  and Caelan Scott and Adam Nicholson and Rupert Lloyd and Cameron Butler and Erik Kennedy and Euan Taylor and Gabriel Cooke and Oskar Lawrence and Aston Hunter and Dominic Hawkins and  and Franklin Burke and Robin Johnston and Benedict Thomson and Mason Howard and Douglas Stone and Kairo Palmer and Ralph Shaw and Haris Riley and Kane Watson and Christopher Bates and  and Toby Woods and Bertie Fletcher and Levi Wilson and Edison Hawkins and Hector Jordan and Phoenix Edwards and Heath Thompson and Zac Clarke and Ewan Poole and Evan Reynolds"""
	##doc = nlp(text.decode('utf8'))
	doc = text
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

	return name, len(name), location, len(location), organization, len(organization)

def dependency_spacy(text):
	nlp = spacy.load('en')
	doc = nlp(text.decode('utf8'))

	for np in doc.noun_chunks: 
		print np.text, np.root.dep_, np.root.head.text 

	text2 = [sent for sent in doc.sents if 'dog' in sent.string.lower()]


