
# nodi arca linguistica == node box linguistics

import sys
import pprint
pp=pprint.pprint

import linguistics
import nltk
import textblob

pp( dir( textblob ))

# import textblob.download_corpora
# pp( l.nltk.data.path )
# pp( sys.modules )
print(textblob.__file__)
pp( dir( textblob ))

py = textblob.TextBlob("Python is a high level language.")

print("\n\nTags:")
pp( py.tags )

print("\n\nSentiment:")
pp( py.sentiment )

print("\n\nSentiment polarity:")
pp( py.sentiment.polarity  )

# noun_phrases
print("\n\nnoun_phrases:")
pp( py.noun_phrases  )

# words
print("\n\nwords:")
pp( py.words  )

#print( "nltk.corpus attributes START" )
#pp( dir(l.nltk.corpus) )
#print( "nltk.corpus attributes END" )

# print("\nsteam is noun?", l.is_noun( "steam" ) )
