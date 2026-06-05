import os
import tempfile
import pprint
import Foundation
import imageio_ffmpeg
import AppKit

pp=pprint.pprint

NSNumber = Foundation.NSNumber

NSImage = AppKit.NSImage
NSApplication = AppKit.NSApplication
NSColor = AppKit.NSColor
NSData = AppKit.NSData
NSBitmapImageRep = AppKit.NSBitmapImageRep
NSJPEGFileType = AppKit.NSJPEGFileType

# 
# file extensions for later use - extracted via "ffmpeg -formats" and manually selected & sorted; ignored imageformats for now
#
# this needs expansion

videoextensions = ("avi caf dhav dvd h261 h263 h264 mkv webm mov mp4 m4a 3gp 3g2 mj2 mpeg ogv rm vcd vob")

audioextensione = ("aa aac ac3 act afc aiff aif aix alaw au ast boa mp2 mp3 oga ogg")


def writeframe( movie, canvas ):
    """Write a frame from the current Nodebox canvas.
    
    Every NB-writer should do it like this.
    
    movie: a valid & open MovieWriter
    
    canvas: the canvas from current document
    """
    
    tiffData = canvas._nsImage.TIFFRepresentation()
    bitmap = NSBitmapImageRep.imageRepWithData_ ( tiffData )
    dataalpha = bytearray( bitmap.bitmapData() )
    movie.send( dataalpha)


class MovieReader:
    def __init__(self, path, pix_fmt="rgb24", bpp=None, input_params=None, output_params=None, bits_per_pixel=None ):
        self.path = os.path.abspath( os.path.expanduser(path) )
        self.pix_fmt = pix_fmt
        self.bpp = bpp
        self.input_params = input_params
        self.output_params = output_params
        self.bits_per_pixel = bits_per_pixel
        meta = self.readMeta()
        if 0:
            pp(meta)
        self.fps = meta.get('fps', 0.0)
        self.audio_codec = meta.get('audio_codec', None)
        self.codec = meta.get('codec', None)
        self.duration = meta.get('duration', 0.0)
        self.pix_fmt = meta.get('pix_fmt', None)
        self.rotate = meta.get('rotate', 0)
        self.size = meta.get('size', None)
        self.source_size = meta.get('source_size', self.size)
            
    def openmovie(self):
        return imageio_ffmpeg.read_frames( self.path, pix_fmt=self.pix_fmt, bpp=self.bpp,
                                           input_params=self.input_params, output_params=self.output_params,
                                           bits_per_pixel=self.bits_per_pixel)


    def readMeta( self ):
        movie = self.openmovie()
        meta = next(movie)
        movie.close()
        return meta


    def readFrames(self):
        movie = self.openmovie()
        
        # read meta
        _ = next(movie)
        
        for frame in next(movie):
            yield frame
        
        movie.close()




class MovieWriter:
    def __init__(self, path, size,
                       pix_fmt_in="rgb24",
                       # pix_fmt_out="yuv420p",
                       pix_fmt_out=None,
                       fps=16, quality=5,
                       bitrate=None, codec=None, macro_block_size=16, ffmpeg_log_level="warning",
                       ffmpeg_timeout=None, input_params=None, output_params=None,
                       audio_path=None, audio_codec=None ):

        self.path = os.path.abspath( os.path.expanduser(path) )
        folder, filename = os.path.split( self.path )
        basename, ext = os.path.splitext( filename )
        
        # handle different output formats here
        
        
        self.size = size
        self.pix_fmt_in = pix_fmt_in
        self.pix_fmt_out = pix_fmt_out
        self.fps = fps
        self.quality = quality
        self.bitrate = bitrate
        self.codec = codec
        self.macro_block_size = macro_block_size
        self.ffmpeg_log_level = ffmpeg_log_level
        self.ffmpeg_timeout = ffmpeg_timeout
        self.input_params = input_params
        self.output_params = output_params
        self.audio_path = audio_path
        self.audio_codec = audio_codec
        
    def openmovie(self):
        movie = imageio_ffmpeg.write_frames(
                self.path,
                self.size,
                self.pix_fmt_in,
                self.pix_fmt_out,
                self.fps,
                self.quality,
                self.bitrate,
                self.codec,
                self.macro_block_size,
                self.ffmpeg_log_level,
                self.ffmpeg_timeout,
                self.input_params,
                self.output_params,
                self.audio_path,
                self.audio_codec)
        return movie


    def writeFrames(self, frames):
        movie = self.openmovie()
        
        for frame in frames:
            movie.send( frame )
        movie.close()




def test():
    import sys
    sys.path.insert(0, '../..')
    sys.path.insert(0, '../../..')
    from nodebox.graphics import Context # Canvas, 
    from math import sin

    NSApplication.sharedApplication().activateIgnoringOtherApps_(0)
    w, h = 512, 320
    mw = MovieWriter("xx3.mp4", (w,h) )
    writer = mw.openmovie()
    for i in range(200):
        print("Frame %i" % i)
        ctx = Context()
        ctx.size(w, h)
        ctx.rect(100.0+sin(i/10.0)*100.0,i/2.0,100,100)
        ctx.text(str(i), i*2, 200)
        writer.send( ctx )
    m.save()
    
if __name__=='__main__':
    test()
