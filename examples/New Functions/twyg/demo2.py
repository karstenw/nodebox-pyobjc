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
    run()

def setconfig(cf):
    global config
    config = cf
    run()

def setdatafile( df ):
    global datafile
    fullpath = os.path.abspath(os.path.join('example-data', df))
    datafile = fullpath
    run()


def run():
    if config and datafile and colorscheme:
        twyg.generate_output_nodebox(datafile, config, colorscheme=colorscheme, margins=margins)
    
var("Config", MENU, default=setconfig, value=configs)
var("Colorscheme", MENU, default=setcolorscheme, value=colorschemes)
var("Datafile", MENU, default=setdatafile, value=datafiles)


run()