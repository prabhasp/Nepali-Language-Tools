#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs,re,optparse,sys

# This is a quick python script to transliterate Nepali (Devnagari) to English.
# It uses a lossy transliteration that I defined to do the work, and converts to all Ascii characters (ie, no diacritics), and doesn't use capital / small letters.
# The issue of the schwa (ie, the sometimes implicit a at the end of words (ie, बन्द becomes band or banda? नाम becomes naam or naama?)) is dealt of in the following way:
#     If there is a punctuation or a halanta preceding the consonant, schwa is added (ex: बान्द => banda, म => ma)
#     However, if what precedes is a vowel, then no schwa is added (ex: नाााम => naam, प्रसाद => prasaad)
#     This is not a perfect rule: works well for nouns (see above) but not for verbs (पर्दैन => pardaina)
#     But its the best for right now
 
def unicodify(strdict):
	return dict([(unicode(x[0],'utf-8'),unicode(x[1],'utf-8')) for x in strdict.items()])

preprocess = unicodify({'ज्ञ' : 'ग्य','ऊँ ':'ओम् ','।':'.'})
punctuations = '.!?,"\')(&@#$%+-_ '
consonants = unicodify({'क' : 'k', 'ख' : 'kh', 'ग' : 'g', 'घ' : 'gh', 'ङ' : 'ng', 'च' : 'ch', 'छ' : 'chh', 'ज' : 'j', 'झ' : 'jh', 'ञ' : 'yn', 'ट' : 't', 'ठ' : 'th', 'ड' : 'd', 'ढ' : 'dh', 'ण' : 'n', 'त' : 't', 'थ' : 'th', 'द' : 'd', 'ध' : 'dh', 'न' : 'n', 'प' : 'p', 'फ' : 'ph', 'ब' : 'b', 'भ' : 'bh', 'म' : 'm', 'य' : 'y', 'र' : 'r', 'ल' : 'l', 'व' : 'v', 'श' : 'sh', 'ष' : 's', 'स' : 's', 'ह' : 'h', 'श्र' : 'shr'})
vowels = unicodify({'अ' : 'a', 'आ' : 'aa', 'इ' : 'i', 'ई' : 'ee', 'उ' : 'u', 'ऊ' : 'oo', 'ए' : 'e', 'ऐ' : 'ai', 'ओ' : 'o', 'औ' : 'au', 'ऋ' : '.r', 'ॠ' : '.rr', 'ऌ' : '.l', 'ॡ' : '.ll', 'अं' : 'am', 'ँ':'(n)', 'ं': '(m)'}) # अं and अँ are here because if they are not like ikars/ukars, ie, don't erase the "अ" at the end of consonants
akar_ukar = unicodify({'ा':'aa','ि':'i', 'ी' : 'ee', 'ु': 'u', 'ू' : 'oo', 'े' : 'e', 'ै' : 'ai', 'ो' : 'o', 'ौ' : 'au', 'ृ' : 'ri', '्':''}) #note the last two items (् halanta and  space): they are hacks to take out the a after the consonants. Also, ि has a special rule; see code below

def multiple_replace(dictionary, text): 
	# Create a regular expression  from the dictionary keys
	regex = re.compile("(%s)" % "|".join(map(re.escape, dictionary.keys())))
	# For each match, look-up corresponding value in dictionary
	return regex.sub(lambda mo: dictionary[mo.string[mo.start():mo.end()]], text)


def transliterate(string):
	if isinstance(string, basestring) and not isinstance(string, unicode): string = string.encode("utf-8") # make sure we have unicode
	ret = ''
	string = multiple_replace(preprocess, string)
	for i,v in enumerate(string):
		# akars, ukars and vowels are simple: you just transliterate based on the table.
		if akar_ukar.has_key(v):
			ret = ret + akar_ukar[v]
	 	elif vowels.has_key(v):	
			ret = ret + vowels[v]
		# Consonants are tricky (क is ka or just k depending on what follows).
		elif consonants.has_key(v):
			# If the consonant is followed by an akar or an ukar things are simple (see else)
			if i < len(string) and akar_ukar.has_key(string[i+1]):
				ret = ret + consonants.get(v,v)
			# If not, we have to check whether the consonant is at a word's end, and go into schwa rules
			else:
				if i == len(string) or string[i+1] in punctuations: #if its a schwa
					#Schwa rule: 
					if i > 0 and (string[i-1] == u'्' or string[i-1] in punctuations): # if preceding char is halanta or a punctuation
						ret = ret + consonants.get(v,v) + 'a'
					else:
						ret = ret + consonants.get(v,v)
				else: #no schwa and no akar. means we have an अ following the consonant
					ret = ret + consonants.get(v,v) + 'a'
		else: ret = ret + v
	return ret

if __name__=="__main__":
	# parse in arguments
	parser = optparse.OptionParser()
	parser.add_option("-v", action="store_true", dest="verbose",
		  help="Verbose mode: give output about status.")
	parser.add_option("-o", "--output", dest="outputfile",
		  help="Output filename. Prints to stdout if unspecified", metavar="OUTFILE")
	(options, args) = parser.parse_args()
	if len(args)==0: 
		print parser.print_help()
		sys.exit(0)
	# read the inputfile, and either print output to file or stdout
	input = codecs.open(args[0], "r", "utf-8").read()
	if options.verbose: print "\nInput received...\n",repr(input),"\n"
	outf = options.outputfile
	if outf:
		f = codecs.open(outf, "w", 'utf-8')
		f.write(transliterate(input))
		f.close()
		if options.verbose: print "Output written to ",outf
	else:
		if options.verbose: print "Output commencing..."
		print transliterate(input)
