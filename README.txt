This is a set of Nepali-Language-Tools written by Prabhas Pokharel.
They are all licensed under GPL v.3.0.

transliterate_ne2en.py
-- This is a transliteration tool from Nepali to English. It transliterates to a strict roman alphabet (ie, no diacritics). It was written to act as step 1 for a tool to do word comparison of nepali words. We want to, for example, search for सलाइ  have have a tool that returns documents with words like सलाई ा and salai and salaai. One approach to this tool is converting devnagari to roman characters and running soundex search algorithms on that text, for which this script is required.
