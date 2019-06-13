from polyglot.text import Text
import timeit
import numpy as np
#blob = """The Israeli Prime Minister Benjamin Netanyahu has warned that Iran poses a "threat to the entire world"."""
#text = Text(blob, hint_language_code='en')

# We can also specify language of that text by using
# text = Text(blob, hint_language_code='en')

#text.entities all entities

#entity for each sentence
# for sent in text.sentences:
# print(sent, "\n")
# for entity in sent.entities:
# print(entity.tag, entity)
def extract_entity(input):
	blob = Text(input, hint_language_code='en')
	name = []
	location = []
	organization = []
	start = timeit.timeit()
	for sent in blob.sentences:
		print(sent, "\n")
		for entity in sent.entities:
			if entity.tag == 'I-PER':
				name.append(entity)
			if entity.tag == 'I-LOC':
				location.append(entity)
			if entity.tag == 'I-ORG':
				organization.append(entity)
	end = timeit.timeit()
	print "time for processing: ", end - start
	return name, len(name), location, len(location), organization, len(organization)
