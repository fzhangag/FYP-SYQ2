#textblob install
#$ pip install -U textblob (must)
#$ python -m textblob.download_corpora (corpora choice 1)
#$ python -m textblob.download_corpora lite (corpora choice 2, minimum package)



from textblob import TextBlob, Word, Blobber
#from textblob.classifiers import NaiveBayesClassifier
#from textblob.taggers import NLTKTagger
#These are the complete import, if only tag, the first import is enough


def extract_entity(text):

	blob = TextBolb(text)

	for word, pos in blob.tags:
		print word, pos
	return

