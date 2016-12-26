#!/usr/bin/python
# This Python file uses the following encoding: utf-8
from spellchecker import *
print "Training..."
freq_dict, corr_dict = train('../db/freq_dict.txt', '../db/corr_dict.txt') 
print "Initializing spellchecker..."
sp = spellchecker(fwords=freq_dict, cwords=corr_dict)
print "Բարեւ"
while True:
	try:
		word = raw_input('> ').decode('utf-8')
		print (' ').join(sp.correct(word, 3))
	except KeyboardInterrupt:
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)

