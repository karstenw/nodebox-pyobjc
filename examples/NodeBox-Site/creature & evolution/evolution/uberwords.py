#!/usr/bin/env python

from __future__ import print_function

from random import choice

starting_vowels = "aeiou".upper()
starting_consonants = "jbcdfghjkmnprstvwz".upper()

middle_vowels = "aeiou"
middle_consonants = "bcdghklmnprstvwz"

ending_vowels = "aeiou"
ending_consonants = "bcfhklmnprst"

def uberword(length, start_with_consonant=True):
    w = ""
    for i in range(length):
        if (i % 2 == 1) is start_with_consonant:
            if i == 0:
                w += choice(starting_vowels)
            elif i == length-1:
                w += choice(ending_vowels)
            else:
                w += choice(middle_vowels)            
        else:
            if i == 0:
                w += choice(starting_consonants)
            elif i == length-1:
                w += choice(ending_consonants)
            else:
                w += choice(middle_consonants)            
    return w


if __name__=='__main__':
    lengths = (5, 6)

    for i in range(100):
        print( uberword(choice(lengths)) )
