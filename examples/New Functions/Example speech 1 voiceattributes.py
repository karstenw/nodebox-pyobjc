import pprint


# get all voice names
v = voices()

for voice in v:
    print voice

    # get all attributes for voice
    attrs = voiceattributes(voice)

    # These are unnecessary here 
    if u'VoiceIndividuallySpokenCharacters' in attrs:
        attrs.pop( u"VoiceIndividuallySpokenCharacters", None )
    if u'VoiceSupportedCharacters' in attrs:
        attrs.pop( u'VoiceSupportedCharacters', None )

    for attr in attrs:
        print attr.ljust(30),
        print attrs[attr]
    # pprint.pprint(attr)
    print "-" * 80
    print
