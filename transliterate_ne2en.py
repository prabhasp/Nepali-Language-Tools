#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs,re,optparse,sys

# This is a quick python script to transliterate Nepali (Devnagari) to English.
# It uses a lossy transliteration that I defined to do the work, and converts to all Ascii characters (ie, no diacritics), and doesn't use capital / small letters.
# The issue of the schwa (ie, the sometimes implicit a at the end of words (ie, बन्द becomes band or banda? नाम becomes naam or naama?)) is hard to deal with, so I have provided a flag to deal with the issues. 
#     -s or --inclue-schwa outputs banda and naama; by default the schwa is ignored
# Also, not sure what to do with अं (for now (m)) and अँ (for now (n))
 
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


def transliterate(string, includeschwa=False):
	if isinstance(string, basestring) and not isinstance(string, unicode): string = string.encode("utf-8") # make sure we have unicode
	ret = ''
	string = multiple_replace(preprocess, string)
	for i,v in enumerate(string):
		# akarsukars and vowels are simple 
		if akar_ukar.has_key(v):
			ret = ret + akar_ukar[v]
	 	elif vowels.has_key(v):	
			ret = ret + vowels[v]
		# for consonants, depends on what follows. If its not a word end, and not an ukar_akar, then a is added 
		elif consonants.has_key(v):
			if (i+1 < len(string) and not akar_ukar.has_key(string[i+1])):
				if not includeschwa and string[i+1] in punctuations: ret = ret + consonants.get(v,v)
				else: ret = ret + consonants.get(v,v) + 'a'
			else:
				ret = ret + consonants.get(v,v)
		else: ret = ret + v
	return ret

if __name__=="__main__":
	# parse in arguments
	parser = optparse.OptionParser()
	parser.add_option("-v", action="store_true", dest="verbose",
		  help="Verbose mode: give output about status.")
	parser.add_option("-s", action="store_true", dest="schwa",
		  help="Include the schwa (end words with an a if no vowel ends word). Example: naama, banda, etc.",metavar="SCHWA")
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
		f.write(transliterate(input,includeschwa=options.schwa))
		f.close()
		if options.verbose: print "Output written to ",outf
	else:
		if options.verbose: print "Output commencing..."
		print transliterate(input,includeschwa=options.schwa)
