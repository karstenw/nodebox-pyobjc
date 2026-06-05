

import sys
import os
import io
import pdb
import pprint
import subprocess

import AppKit

try:
    import nodebox
except ImportError:
    nodebox_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(nodebox_dir))

import nodebox.graphics

import nodebox.util
import nodebox.util.MP4Support

pp = pprint.pprint

NSApplication = AppKit.NSApplication
graphics = nodebox.graphics
util = nodebox.util
MovieWriter = nodebox.util.MP4Support.MovieWriter
writeframe = nodebox.util.MP4Support.writeframe

librarypath = "NONE"
try:
    result = subprocess.run([ "defaults","read","net.nodebox.NodeBox","libraryPath" ], capture_output=True)
    p = result.stdout  #os.system("/usr/bin/defaults read net.nodebox.NodeBox libraryPath")
    p = p.strip( b" \t\n\r" )
    p = str(p,encoding="utf-8")
    if os.path.exists(p):
        librarypath = p
        sys.path.insert(0, librarypath)
except Exception as err:
    print("READ Librarypath Preference failed.")
    print(err)
    librarypath = False
print("librarypath:", repr(librarypath))


class NodeBoxRunner(object):
    
    def __init__(self):
        # Force NSApp initialisation.
        NSApplication.sharedApplication().activateIgnoringOtherApps_(0)
        self.namespace = {}
        self.canvas = graphics.Canvas()
        self.context = graphics.Context(self.canvas, self.namespace)
        self.__doc__ = {}
        self._pageNumber = 1
        self.frame = 1
        self.library = False

    def _check_animation(self):
        """Returns False if this is not an animation, True otherwise.
        Throws an expection if the animation is not correct (missing a draw method)."""
        if self.canvas.speed is not None:
            if 'draw' not in self.namespace:
                raise( graphics.NodeBoxError('Not a correct animation: No draw() method.') )
            return True
        return False
        
    def run(self, source_or_code):
        self._initNamespace()
        if isinstance(source_or_code, str):
            source_or_code = compile(source_or_code + "\n\n", "<Untitled>", "exec")
        exec( source_or_code, self.namespace, self.namespace ) 
        if self._check_animation():
            if 'setup' in self.namespace:
                self.namespace['setup']()
            self.namespace['draw']()
        
    def run_multiple(self, source_or_code, frames):
        # pdb.set_trace()
        if isinstance(source_or_code, str):
            source_or_code = compile(source_or_code + "\n\n", "<Untitled>", "exec")
            
        # First frame is special:
        self.run(source_or_code)
        # yield 1
        animation = self._check_animation()
            
        # for i in range(frames-1):
        for frame in range(1,frames+1):
            
            self.canvas.clear()
            
            # self.frame = i + 2
            self.frame = frame
            
            # self.namespace["PAGENUM"] = self.namespace["FRAME"] = self.frame
            self.namespace["PAGENUM"] = self.namespace["FRAME"] = frame
            if animation:
                self.namespace['draw']()
            else:
                exec( source_or_code, self.namespace, self.namespace )
            yield self.frame


    def _initNamespace(self, frame=1):
        self.canvas.clear()
        self.namespace.clear()
        # Add everything from the namespace
        for name in graphics.__all__:
            self.namespace[name] = getattr(graphics, name)
        for name in util.__all__:
            self.namespace[name] = getattr(util, name)
        # Add everything from the context object
        self.namespace["_ctx"] = self.context
        for attrName in dir(self.context):
            self.namespace[attrName] = getattr(self.context, attrName)
        # Add the document global
        self.namespace["__doc__"] = self.__doc__
        # Add the frame
        self.frame = frame
        self.namespace["PAGENUM"] = self.namespace["FRAME"] = self.frame


def make_image(source_or_code, outputfile):
    
    """Given a source string or code object, executes the scripts and saves the result as
    an image.  Supported image extensions: pdf, tiff, png, jpg, gif"""
    
    if os.path.exists( source_or_code ):
        f = io.open( source_or_code, encoding="utf-8" )
        source_or_code = f.read()
        f.close()
        
    runner = NodeBoxRunner()
    runner.run(source_or_code)
    runner.canvas.save(outputfile)
    return source_or_code


def make_movie(source_or_code, outputfile, frames, fps=30):

    """Given a source string or code object, executes the scripts and saves the result as
    a movie.
    
    You also have to specify the number of frames to render.
    Supported movie extension: mov"""
    
    # pdb.set_trace()
    
    runner = NodeBoxRunner()
    runner.run( source_or_code )
    
    w = runner.canvas.width
    h = runner.canvas.height
    
    mw = MovieWriter(outputfile, (w,h), pix_fmt_in="rgba", fps=fps)
    movie = mw.openmovie()
    movie.send( None )
    
    for framenr in runner.run_multiple(source_or_code, frames):
        if 1:
            print("make_movie FRAME:", framenr)
            runner.canvas.save("dbg-%i.jpg" % framenr )
        writeframe( movie, runner.canvas )
    # movie.close()
    print()



def usage(err=""):
    if len(err) > 0:
        err = '\n\nError: ' + str(err)
    print("""NodeBox console runner
Usage: console.py sourcefile imagefile
   or: console.py sourcefile moviefile number_of_frames [fps]
Supported image extensions: pdf, tiff, png, jpg, gif
Supported movie extension:  mov""" + err)

def main():
    if len(sys.argv) < 2:
        usage()
    elif len(sys.argv) == 3: # Should be an image
        basename, ext = os.path.splitext(sys.argv[2])
        if ext not in ('.pdf', '.gif', '.jpg', '.jpeg', '.png', '.tiff'):
            return usage('This is not a supported image format.')
        make_image(open(sys.argv[1]).read(), sys.argv[2])
    elif len(sys.argv) == 4 or len(sys.argv) == 5: # Should be a movie
        basename, ext = os.path.splitext(sys.argv[2])
        if ext not in ('.mp4', '.mov', '.mkv'):
            return usage('This is not a supported movie format.')
        if len(sys.argv) == 5:
            try:
                fps = int(sys.argv[4])
            except ValueError:
                return usage()
        else:
            fps = 30
        make_movie(open(sys.argv[1]).read(), sys.argv[2], int(sys.argv[3]), fps)

def test():
    # Creating the NodeBoxRunner class directly:
    
    runner = NodeBoxRunner()
    testscript = ('size(512,512)\n'
                  'for i in range(400):\n'
                  '  oval(random(WIDTH),random(HEIGHT),50,50, '
                  'fill=(random(), 0,0,random()))')
    runner.run(testscript)
    runner.canvas.save('console-test.pdf')
    runner.canvas.save('console-test.png')
    
    # Using the runner for animations:
    runner = NodeBoxRunner()
    for frame in runner.run_multiple('size(304, 304)\ntext(FRAME, 100, 100)', 5):
        runner.canvas.save('console-test-frame%02i.png' % frame)
    
    # pdb.set_trace()
    
    script="""
size( 208, 208 )
fill(1,0,0)
stroke(0,1,0)
font(choice(fontnames()))
fontsize(36)
text(str(FRAME), 70, 70, 36 )"""
    make_movie( script, 'console-test.mp4', 10)
    make_movie( script, 'console-test.mkv', 10)
    make_movie( script, 'console-test.mov', 10)
    # Using the shortcut functions:
    #make_image('size(208,208)\ntext(FRAME, 100, 100)', 'console-test.jpg')
    # make_movie('size(208,208)\ntext(FRAME, 100, 100)', 'console-test.mp4', 10)
    #make_movie('size(208,208)\ntext(FRAME, 100, 100)', 'console-test.mkv', 10)
    #make_movie('size(208,208)\ntext(FRAME, 100, 100)', 'console-test.mov', 10)

if __name__=='__main__':
    main()
