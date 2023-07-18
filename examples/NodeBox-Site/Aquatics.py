size(1200,600)
 
try:
    supershape = ximport("supershape")
except:
    supershape = ximport("__init__")
    # reload(supershape)
 
class head:
    def __init__(self,x,y,w,h,c,pp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.c = c
        self.r = self.c.r
        self.g = self.c.g
        self.b = self.c.b
        self.eyelist = []
        self.backpad = oval(10,10,0,0)
        self.backpadintern = []
        self.backpadextern = []
        self.pp = pp
        
    def geefpad(self):
        return self.p
        
    def pupil(self,x,y,g):
        from math import sin, cos
        if not random()>.85:
            ''' normal '''
            s = g/4+random(g/3)
            fill(self.c.r*2.0,self.c.g,self.c.b,self.c.a/2.0)
            stroke(self.c.r,self.c.g/2,self.c.b,.6);strokewidth(2.0)
            ran = random(s/2,-s/2)
            oval(x-s+ran,y-s+ran,s*2,s*2)
            fill(1);strokewidth(5.0);stroke(0)
            oval(x-s/4+ran,y-s/4+ran,s/2,s/2)
        else:
            ''' spiral '''
            l = random();fill(0)
            stroke(self.c.r,self.c.g/2,self.c.b,1.0);strokewidth(.5)
            for i in range(100):
                v = x+i/5.0*sin(i*l)
                w = y+i/5.0*cos(i*l)
                oval(v,w,2,2)
        
    def shield(self,x,y,g):
        seg = oval(x-g,y-g,g*2,g*2,draw = False)
        pad = rect(x-g,y-random(10.0,-4.0),g*2,g*2,draw = False)
        pc = pad
        pad = pad.union(seg)
        pad = pad.difference(pc,False)
        fill(self.c.r,self.c.g,self.c.b,1.0)
        stroke(0);strokewidth(1.0)
        drawpath(pad)
        return(pad)
 
    def eyes(self,xx,yy,g):
        fill(1);stroke(0);strokewidth(2.0)
        oval(xx-g,yy-g,g*2,g*2)
        self.pupil(xx,yy,g)
        if random()>.5:
            cover = self.shield(xx,yy,g)
            f = [xx,yy]
            stroke(self.c.r/2,self.c.g/2,self.c.b/2,1.0);strokewidth(3.0)
            for eyelash in cover:
                if random() > .5:
                    x = eyelash.x-f[0]
                    y = eyelash.y-f[1]
                    lx = random(x)
                    ly = random(y)
                    line(eyelash.x, eyelash.y, eyelash.x+lx, eyelash.y+ly)
       
    def linedash(self,path,segment,gap):
        path._nsBezierPath.setLineDash_count_phase_([segment,gap],2,0)
        return path        
            
    def draw(self):
        ''' create  supershapes : 1 for the actual 'beast' and 1 as a mouth 
        the final shape is the difference between them'''
        m = int(random(1,30))
        if random()>.5:
            n1 = -.8-random(5.0)
        else:
            n1 = .8+random(5.0)
        n2 = .5+random(5.0)
        n3 = .5+random(.5,-1.5)
        
        '''uncomment to use textpaths __ see below '''
        #self.p = textpath(self.pp,self.x-random(50,100),self.y+100,800,0)
 
        self.p = supershape.path(self.x, self.y, self.w, self.h, m, n1, n2, n3)
        arms = 4 + random(20)
        l = supershape.path(self.x, self.y+self.h / 1.5,
                            self.w * 0.35,
                            self.h * 0.65,
                            arms, 0.98,3.0,
                            0.81 + random(-.8,.8) )
        self.p = self.p.difference(l)
        ''' create some locations to place the eyes on '''
        for i in range(2+random(10)):
            xx = self.x+random(-self.w,self.w)
            yy = self.y+random(-self.h)
            g = 5+random(self.w/5.0)
            if header.p.contains(xx,yy):
                tup = xx,yy,g
                self.eyelist.append(tup)
        mouth = []
        for p in l:
            if self.p.contains(p.x,p.y):
                loc = p.x,p.y
                mouth.append(loc)
                if random() < .01 and p.y < (self.h*4.8):
                    fill(1);strokewidth(5)
                    k = (-45,0,45)
                    '''teeth __ not to pleased about them '''
                    stroke(self.c.r/2,self.c.g/2,self.c.b/2,1.0)
                    si = 10+random(self.w*.1)
                    if not p.x < self.x:
                        skew(choice(k))
                        rect(p.x+si/2,p.y,-si,-si)
                        reset()
                    else:
                        skew(choice(k))
                        rect(p.x-si/2,p.y,si,si)
                        reset()
        fill(self.c);stroke(self.c.r/2,self.c.g/2,self.c.b/2) 
        strokewidth(self.w/20);#nostroke()
        ''' draw the shape __ all the rest comes on top of this '''
        drawpath(self.p)
        ''' lips '''
        for o in mouth:
            s = 1.5
            fill((self.r+self.g)*.8,(self.g+self.b)*.8,(self.b+self.r)*.8,.5)
            nostroke()
            oval(o[0]-s,o[1]-s,s*2,s*2)
        self.geefpad()
        
        ''' create an inner and outer path base on the position of the eyes '''
        for item in self.eyelist:
            x,y,g = item[0],item[1],item[2]
            seg = oval(x-g*3,y-g*3,g*6,g*6,draw = False)
            self.backpad = self.backpad.union(seg)
            self.backpadintern = self.backpad.intersect(self.p)
            self.backpadextern = self.backpad.difference(self.p)
            
        ''' draw hair on the outer path '''
        for p in self.backpadextern:
            autoclosepath(False);nofill()
            x = p.x-self.x
            y = p.y-self.y
            lx = random(x)
            ly = random(y)
            m = random(30)
            stroke(self.c);strokewidth(1.0)
            beginpath(p.x,p.y)
            curveto(p.x+random(m),p.y+random(m),p.x-random(m),p.y-random(m),
                    p.x+random(lx),p.y+random(ly))
            endpath()
            
        ''' draw the outer path in tranparant color and a stroke half the stroke of the shape itself '''
        fill(self.c.r,self.c.g,self.c.b,.4);
        stroke(self.c.r/2,self.c.g/2,self.c.b/2);strokewidth(self.w/40)
        drawpath(self.backpadextern)
 
        ''' some different jackets for the beast -- possibilities are unlimited here '''
        l = 5+random(self.w/6)
        rw = self.w*4/l;rh = self.h*4/l;dx = l;dy = l
        strokewidth(1.0)
        aantal = [1,2,3,4,5,2,3,3]
        pa = choice(aantal)
        cc = random(1,2)
        # print( pa )
        for x,y in grid(rw,rh,dx,dy):
            nx = x+self.x-self.w*2
            ny = y+self.y-self.h*2
            nxc = (nx-self.x)
            nyc = (ny-self.y)
            if self.p.contains(nx-dx,ny):
                fill((self.r+self.g)/2,(self.g+self.b)/2,(self.b+self.r)/2,.8)
                beginpath(nx-dx,ny)
                if random()>.5:
                    k = random(-self.w*.25)
                else:
                    k = random(self.w*.25)
                if pa==1:
                    ''' spikes '''
                    autoclosepath(True)
                    curveto(nx,ny,nx,ny,nx+random(nxc),ny+random(nyc))
                elif pa==2:
                    '''bubbles '''
                    autoclosepath(True)
                    curveto(nx+random(5.0),ny,nx-(dx/2),ny+k,nx-dx,ny)
                elif pa==3:
                    ''' lines '''
                    nofill();autoclosepath(False)
                    curveto(nx-dx,ny,nx,ny+k,nx,ny)
                else:
                    ''' flocks '''
                    autoclosepath(True)
                    curveto(nx-dx+random(-dx*2,dx*2),ny,nx-dx,ny+k,nx-dx,ny)
                endpath()
        
        ''' draw inner path with dotted line '''    
        fill((self.r+self.g)/2,(self.g+self.b)/2,(self.b+self.r)/2,.8)
        #d = self.linedash(self.backpadintern,10,5)
        stroke(self.c.r/2,self.c.g/2,self.c.b/2);strokewidth(1.5)
        drawpath(self.backpadintern)
        
        ''' draw an eye for each location in the eyelist '''
 
        for item in self.eyelist:
            self.eyes(item[0], item[1],item[2])

#r = random(100)
#print("r:", r)
#if r > 50:
if 0:
    for i in range(2):
        s = 70+random(50)
        c = color(random(),random(),random())
        # print( s )
        header = head(250+i*(400),HEIGHT/2+10,s,s,c,0)     
        header.draw()   
 
 
# textexample with background 
else:
    m = 'A'
    ttt = 'AquaTics'
    font("Marker Felt",250)
    #ttt = ''
    background(0.9,0.28,0.62)
    for i in range(10):
        fill(0.9,0.28*i/10,0.62)
        rotate(i*4.0)
        rect(i*WIDTH/10,0,WIDTH/10,HEIGHT)
    for i in range(len(ttt)):     
        m = ttt[i]   
        c = color(random(.5,.99),random(0.5,0),random(0.5,0),1.0)
        s = 70+random(50)
        print( s )
        header = head(80+i*(WIDTH/len(ttt)),HEIGHT/2+random(-5*i),s,s,c,m)     
        header.draw() 

