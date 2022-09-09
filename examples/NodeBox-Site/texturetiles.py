img = "engine.jpg"
 
coreimage = ximport("coreimage")
 
def tile(img, w=350, h=350):
 
    """ Returns a tileable canvas of given width and height.
    """
 
    # Create a canvas from the image.
    # The canvas will have the same size as the image.
    canvas = coreimage.canvas(img)
    l = canvas.append(img)
 
    # Place the top left corner of the image
    # in the top left of the canvas.
    # We'll "wrap around" the overflow on the right and bottom.
    l.origin_top_left()
    l.x = 0
    l.y = 0
 
    # Create a duplicate, shift it to the left
    # so only the overflow on the right is visible.
    wrap = l.duplicate()
    wrap.x = -w
 
    # Add a horizontal linear gradient mask to the wrap.
    # It should gradually disappear revealing the original image.
    m = wrap.mask.gradient()
    m.scale(1.0, int(l.width-w))
    m.rotate(-90)
    m.origin_top_left()
    m.x = w
    m.y = l.height
 
    # We now have a composition that is horizontally tileable.
    # We'll flatten our work to a single layer which we can
    # then wrap vertically.
    merged = canvas.flatten()
    canvas[0].hidden = True
    canvas[1].hidden = True
    l = canvas.append(merged)
    l.origin_top_left()
    l.x = 0
    l.y = 0
 
    # Do the same for a vertical wrap.
    wrap = l.duplicate()
    wrap.y = -h
    m = wrap.mask.gradient()
    m.scale(1.0, int(l.height-h))
    m.origin_top_left()
    m.x = 0
    m.y = h
 
    # Crop the canvas to the tile size.
    # We do this at the end, because before we needed 
    # the full image size to flatten.
    canvas.w = w
    canvas.h = h
 
    # This is our tile.
    # We can now add it to another canvas, or export it.
    tile = canvas.flatten()
 
    canvas = coreimage.canvas(w, h)
    canvas.append(tile)
    return canvas
 
t = tile(img)
t.draw()
t.draw(0, t.h)
t.draw(t.w, 0)
t.draw(t.w, t.h)


t = tile(img)
p = t[0].pixels()

# see webarchive
#clr = p.get_pixel(i,j)
#fill(clr)

