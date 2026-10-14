# normalize: value, low, high -> 0...1
# Normalize the given value and range to 0...1
print( "\nnormalize( 127.5, 0, 255 ):", normalize( 127.5, 0, 255 ) )
print( "\nnormalize( 128,   1, 255 ):", normalize( 128, 1, 255 ) )
print( "\nnormalize(  33,   0, 100 ):", normalize(  33, 0, 100 ) )

print( "\nnormalize( 128, 0, 255 ):", normalize( 128, 0, 255 ) )
print( "\nnormalize(   0, 1, 256 ):", normalize(   0, 1, 256 ) )
print( "\nnormalize( 257, 0, 255 ):", normalize( 257, 0, 255 ) )
print( "\nnormalize( 5, 0, 10 ):", normalize( 5, 0, 10 ) )

print()
# constrain value, low, high -> low <= value <= high
print( "\nconstrain( 128,  0, 255 ):", constrain( 128,  0, 255 ) )
print( "\nconstrain(   5, 10,  90 ):", constrain(   5, 10,  90 ) )
print( "\nconstrain( 500, 10,  90 ):", constrain( 500, 10,  90 ) )

print()
# lerp start, end, t -> start + t * (end - start)
# Linearly interpolate the start value to the end value
print( "\nlerp( 10,  90, 0.5 ):", lerp( 10,  90, 0.5 ) )
print( "\nlerp( 10, 200, 0.5 ):", lerp( 10, 200, 0.5 ) )
print( "\nlerp(  0, 999, 2.5 ):", lerp(  0, 999, 2.5 ) )

print()
# Remap a value from the source range to the dest range
#
# remap val, src_start, src_end, dst_start, dst_end
# -> val mapped to dst_start, dst_end

print( "\nremap( 0.25, 0.0, 1.0, 50, 500 )",
        remap( 0.25, 0.0, 1.0, 50, 500 ))

print( "\nremap( 0.25, 0.0, 1.0,  0, 100 )",
        remap( 0.25, 0.0, 1.0,  0, 100 ))

print( "\nremap(  0.25, 500.0, 1000.0, 50, 500 )",
        remap( 625.0, 500.0, 1000.0, 50, 500 ))

print( "\nremap( 0.334, 0.0, 10.0, 50, 5000 )",
        remap( 0.334, 0.0, 10.0, 50, 5000 ))
