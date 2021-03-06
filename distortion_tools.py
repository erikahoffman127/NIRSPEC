from scipy.optimize import leastsq
import numpy as n
import matplotlib.pyplot as plt
import numpy.polynomial.polynomial as poly

# Distortion polynomials
dist_x_prime = [[0.   ,        0.     ,      0.000059499,  0.0000005929,],
 [1.       ,    0.     ,      0.     ,      0.    ,      ],
 [0.   ,        0.0000005452, 0.    ,       0.   ,       ],
 [0.00000016,   0. ,          0.   ,        0.          ]]
dist_y_prime = [[ 0.      ,      1.      ,     -0.0000577988,  0.    ,      ],
 [ 0.      ,      0.0000093407, -0.000000836,   0.       ,   ],
 [-0.0000146104, -0.0000006679,  0.  ,          0.    ,      ],
 [ 0.0000001513,  0.   ,         0.    ,        0.          ]]

def forward_2d_poly_vec(x, y, ca, cb):
    y0 = 256/2
    x0 = 256/2
    fx = poly.polyval2d(n.array(x)-x0, n.array(y)-y0, ca) + x0     # evaluate polynomial
    fy = poly.polyval2d(n.array(x)-x0, n.array(y)-y0, cb) + y0
    return fx, fy

def x_y_to_xy(x_coord, y_coord): #join two seperate 1D lists of x and y into single 1D list
    coord_list = []
    for xy in zip(x_coord, y_coord): # I would have liked to remove this loop
        coord_list = n.append(coord_list, (xy))
    return coord_list
    
#TRANSFORM FROM TRUE (UNDISTORTED) TO OBSERVED (DISTORTED) REFERENCE FRAME
def undistorted_to_distorted(undist_x, undist_y): #input true stellar positions
    """ this function transforms from the true (undisorted) stellar positions to the observed (distorted) positions
        input two seperate 'x' , 'y' 1D arrays or lists of the true stellar positions, 
        the output will give you the observed stellar positions in your image as two seperate 'x' , 'y' 1D arrays"""
    dist_x, dist_y = forward_2d_poly_vec(undist_x, undist_y, dist_x_prime, dist_y_prime)
    return dist_x, dist_y

#TRANSFORM FROM OBSERVED (DISTORTED) REFERENCE FRAME TO TRUE (UNDISTORTED) 
def distorted_to_undistorted(dist_x, dist_y): #input observed stellar positions
    """ this function transforms from the observed (disorted) stellar positions to the true (undistorted) positions
        input two seperate 'x' , 'y' 1D arrays or lists of the observed stellar positions, 
        the output will give you the true stellar positions in your image's reference frame as two seperate 'x' , 'y' 1D arrays"""
  
    def pack_p(p): #turn a raveled 1D array into a 2d array of points
        len_distorted_data = int(len(p)/2)
        pts = n.array(p[0 : 2*len_distorted_data].reshape(len_distorted_data, 2))
        return pts

    def fitter_undistorted_pos(p): #p must be passed as a 1D
        coord = pack_p(p)
        
        xx, yy = coord[:,:1], coord[:,1:] #retrieve x's and y's seperatly from 2D array of points
    
        distort_x, distort_y = forward_2d_poly_vec(xx, yy, dist_x_prime, dist_y_prime)
    
        dist_coord = x_y_to_xy(distort_x, distort_y) #put x's and y's back together in 1D raveled array of points
    
        #should be x,y desired position minus polynomial*(undistorted)
        distorted_data = n.ravel(guess)
        res = n.subtract(distorted_data, dist_coord)
        return res

    guess = x_y_to_xy(dist_x, dist_y)
    p, ier = leastsq(fitter_undistorted_pos, guess) #SEE fitter_undistorted_pos ABOVE
        
    x_undist, y_undist = p[::2], p[1::2] #retrieve every other element of raveled coordinates
    
    return x_undist, y_undist
