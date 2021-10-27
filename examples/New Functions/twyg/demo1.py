
from __future__ import print_function

import os
twyg = ximport('twyg')
# reload(twyg)

datafiles = list(filelist( os.path.abspath('example-data')))
datafile = choice(datafiles)


configs = [ 'boxes', 'bubbles', 'edge', 'flowchart', 'hive', 'ios', 'jellyfish',
            'junction1', 'junction2', 'modern', 'nazca', 'rounded', 'square',
            'synapse', 'tron']

colorschemes = [ 'aqua', 'azure', 'bordeaux', 'clay', 'cmyk', 'cobalt', 'colors21',
                 'crayons', 'earth', 'forest', 'grape', 'honey', 'inca', 'jelly', 'kelp',
                 'mango', 'mellow', 'merlot', 'milkshake', 'mint-gray', 'mint', 'moon',
                 'mustard', 'neo', 'orbit', 'pastels', 'quartz', 'salmon', 'tentacle',
                 'terracotta', 'turquoise', 'violet']

config = choice(configs)
colorscheme = choice(colorschemes)

margins = ['10%', '5%']

print( config )
print( colorscheme )
print( os.path.basename(datafile) )
print()
twyg.generate_output_nodebox(datafile, config, colorscheme=colorscheme, margins=margins)
