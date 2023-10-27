
from __future__ import print_function

import os
import pprint

voicename=None

# get all voice names
v = voices()

allspeakers = []


for voice in v:
    attr = voiceattributes(voice)

    # get the demo text
    txt = makeunicode(attr[ u'VoiceDemoText' ])
    
    # get the official name
    name = attr[ u'VoiceName' ]

    path= "./%s.aiff" % name
    path = makeunicode(os.path.abspath( path ))

    allspeakers.append( (voice, txt, name, path) )

for s in allspeakers:
    voice, txt, name, path = s
    say(txt, voice, path)
    print( voice )
    print( name )
    print( txt )
    print()
print( "voicecount:", len(allspeakers) )
