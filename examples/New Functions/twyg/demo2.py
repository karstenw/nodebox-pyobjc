
from __future__ import print_function
from importlib import reload
import os
twyg = ximport('twyg')
reload(twyg)


datafiles = list(filelist( os.path.abspath('example-data')))
datafile = datafiles[0]
datafiles = [os.path.split(i)[1] for i in datafiles]



configs = [ 'boxes', 'bubbles', 'edge', 'flowchart', 'hive', 'ios', 'jellyfish',
            'junction1', 'junction2', 'modern', 'nazca', 'rounded', 'square',
            'synapse', 'tron']

colorschemes = [ 'aqua', 'azure', 'bordeaux', 'clay', 'cmyk', 'cobalt', 'colors21',
                 'crayons', 'earth', 'forest', 'grape', 'honey', 'inca', 'jelly', 'kelp',
                 'mango', 'mellow', 'merlot', 'milkshake', 'mint-gray', 'mint', 'moon',
                 'mustard', 'neo', 'orbit', 'pastels', 'quartz', 'salmon', 'tentacle',
                 'terracotta', 'turquoise', 'violet']

config = configs[0]
colorscheme = colorschemes[0]

margins = ['10%', '5%']

def setcolorscheme( cs ):
    global colorscheme
    colorscheme = cs
    #print("colorscheme:", colorscheme)
    run()

def setconfig(cf):
    global config
    config = cf
    #print("config:", config)
    run()

def setdatafile( df ):
    global datafile
    fullpath = os.path.abspath(os.path.join('example-data', df))
    datafile = fullpath
    # print("datafile:", datafile)
    run()


def run():
    # if 1: #config and datafile and colorscheme:
    res = twyg.generate_output_nodebox(datafile, config, colorscheme=colorscheme, margins=margins)
    # print("result:", res)
    
var("Config", MENU, default=setconfig, value=configs)
var("Colorscheme", MENU, default=setcolorscheme, value=colorschemes)
var("Datafile", MENU, default=setdatafile, value=datafiles)


run()
