
from __future__ import print_function

import pprint

"""Select a voice and it says it's demo text."""


voicename=None

# get all voice names
v = voices()

def dovoice(v, n):
    attr = voiceattributes(v)

    # get the demo text
    txt = attr[ u'VoiceDemoText' ]
    
    # get the official name
    name = attr[ u'VoiceName' ]

    # say my line
    say(txt, v, wait=True)
    
    # print some voice stuff
    print( "Name:", attr[ u'VoiceName' ] )
    print( "Age: %s" % (attr.get(u'VoiceAge', "")) )
    print( "Language: %s" % (attr.get( u'VoiceLanguage', "")) )
    print( txt )
    print()


# try to determine the default voice

# say nothing with default voice
vc = say("")
name = makeunicode(vc.voice())
name = name.replace(u"com.apple.speech.synthesis.voice.", "")
attr = voiceattributes(name)
voicename = name


v = var("Voice Name", MENU, default=voicename, handler=dovoice, menuitems=v)

dovoice(voicename, "")
