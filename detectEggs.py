# -*- coding: utf-8 -*-
"""
Created on Wed Apr 06 16:03:33 2016

@author: Greencomp
"""

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy import ndimage
from skimage import color
from skimage.filters import threshold_otsu, threshold_adaptive
from skimage.measure import regionprops
from skimage.draw import circle_perimeter,circle_perimeter_aa
import time
import os
directory = '../Data/individualPics/07-12-2016/'#'../Data/19-May-2016/'
directory = '../Data/stitched/07-12-16/'
#directory = '../../test/'
for names in range(int(len(os.listdir(directory))/4)):
    filename = directory+os.listdir(directory)[names]
    #filename = directory + 'loc_31_22-37-30.png'
    #filename = directory+os.listdir(directory)[7]
    filename = directory+'loc_16_22-23-26.png'
    #filename = directory + 'loc_25_14-21-29.png'
    im = Image.open(filename)
    image = np.asarray(im)
    #io.imshow(image)
    #io.show()
    
    start = time.time()
    
    global_thresh = 1.5*threshold_otsu(image)#.82
    binary_global = image < global_thresh
    
    #block_size = 40
    #binary_adaptive = threshold_adaptive(image, block_size, offset=10)
    
    	
    labeled_array, num_features = ndimage.measurements.label(binary_global)
    #plt.imshow(binary_global,cmap = plt.gray())
    #plt.show()
    
    eggs = []
    
    properties = regionprops(labeled_array)
    
    
    for i in range(len(properties)):
        area = properties[i].filled_area #(140)
        #area = properties[i].area
        if area < 2000 and area>65 and properties[i].eccentricity<0.95 and properties[i].euler_number>-1 and properties[i].minor_axis_length>7:# and properties[i].minor_axis_length>10 and properties[i].major_axis_length<65:
            coord = properties[i].centroid
            eggs.append(coord)        
            #print properties[i].euler_number            
            if area>400:
                coord2 = (properties[i].centroid[0]+4,properties[i].centroid[1]+4)
                eggs.append(coord2)
                if area>700:
                    coord3 = (properties[i].centroid[0]+10,properties[i].centroid[1]-10)
                    eggs.append(coord3)
                    if area>900:
                        coord4 = (properties[i].centroid[0]-10,properties[i].centroid[1]+10)
                        eggs.append(coord4)
            
    number = len(eggs)
    #print eggs
    print '%i eggs' %number
    
    radius = 22
    image.flags.writeable = True
    for i in range(len(eggs)):
        center_y, center_x = eggs[i]
        cx, cy,val = circle_perimeter_aa(int(center_x),int(center_y), radius)#,shape = image.shape)
        #image[cy,cx] = 255 
        try:        
            image[cy, cx] = 255# (220, 20, 20)# 0
        except IndexError:
            break
    
    ax = plt.axis()
    #plt.imshow(image, cmap=plt.cm.gray)
    plt.imshow(image,cmap = plt.gray())
    plt.show()
#plan: use area (or filled_area) to find the eggs, centroid? or coords to get the location of them
