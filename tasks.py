from flask import Flask
from celery import Celery
import application
import re
import nltk
import random

from nltk.corpus import stopwords

application = Flask(__name__)
application.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
application.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(application.name, broker=application.config['CELERY_BROKER_URL'], backend=application.config['CELERY_BROKER_URL'])
# celery.conf.update(application.config)
tag_to_word = {}
filename2 = "captions.txt"


def create_tagset(pos):
	for tagset in pos:
		# does tag_to_word already have this key?
		#iterating over the list to see whether dictionary has the key to that tag
		if tag_to_word.has_key(tagset[1]):
			val=tag_to_word[tagset[1]]
			#print val
			val.append(tagset[0])
			#print val
			tag_to_word[tagset[1]]=val
		else:
			tag_to_word[tagset[1]]= [tagset[0]]

	return tag_to_word


def convert_text(tag_to_word):
	all_text = ""
	nouns = tag_to_word['NN']
	adjectives = tag_to_word['JJ']

	for line in open(filename2):
		output = ""
		line = line.strip()
		line_tokens = re.split('\s+', line)
		pos2 = nltk.pos_tag(line_tokens)

		for tagset in pos2:
			if tagset[1] == 'NN':
			#grab random noun from dictionary
				nouns = tag_to_word['NN']
			#pick a random noun from list of nouns grabbed from dictionary
				random_noun = random.choice(nouns)
				print 'random noun ', random_noun
				output+= random_noun + " "

			elif tagset[1] == 'JJ':
				random_adjective = random.choice(adjectives)
				print 'random adj ', random_adjective
				output+= random_adjective + " "

			else:
				output += tagset[0] + " "

		output = output[0].upper() + output[1:] + " "
		all_text += output + "\n"
	return all_text

@celery.task
def main(tmp_file_name):
	body = open(tmp_file_name).read().lower().split('\n')[1]
	body_lines = body.split(".")
	if "\xe2\x80\x99" in body:
		body = re.sub(u"\xe2\x80\x99's", "", body)
	if "\xe2\x80\x94" in body:
		print 'body has a hyphen or something in it'
		body = re.sub(u"\xe2\x80\x94", "", body)
	if " it" in body:
		body = re.sub(" it", "", body)		
	source = open(tmp_file_name).read().lower().split('\n')[0]
	stop = set(stopwords.words('english'))
	body_sans_sw = [i for i in body.lower().split() if i not in stop]
	tokens = [re.sub(r"\W", "", x) for x in body_sans_sw]
	pos = nltk.pos_tag(tokens)
	tag_to_word = create_tagset(pos)
	converted_output = convert_text(tag_to_word)
	with open("converted_output.txt","w") as file:
		file.write(source + "\n" + converted_output)
	return source + "\n" + converted_output