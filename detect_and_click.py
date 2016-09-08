# -*- coding: utf-8 -*-
"""
Created on Wed Apr 06 16:03:33 2016

@author: Greencomp
"""

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy import ndimage
#from skimage import color
from skimage.filters import threshold_otsu#, threshold_adaptive
from skimage.measure import regionprops
from skimage.draw import circle_perimeter,circle_perimeter_aa
import time
import pickle
#import os
import cv2
#import scipy
#from skimage import io
import sys
from os import rename,listdir,path,makedirs
directory = '../Data/individualPics/07-12-2016/'#'../Data/19-May-2016/'   tg
directory = '../Data/stitched/09-07-16/'


#counter = 0
refPt =[]
click_locs = []
eggs = []
#set neighborhood to look for egg duplicates:
epsilon = 50
def click_and_count(event,x,y, flags, param):
# grab references to the global variables
    global counter, refPt,click_locs,eggs
  	# check to see if the left mouse button was released
    if event == cv2.EVENT_LBUTTONUP:
      # record the ending (x, y) coordinates and append to list of egg locations
        refPt = [(x,y)]
        counter = counter+1     
        eggs.append((y,x))
		#small = cv2.resize(image, (0,0), fx=0.5, fy=0.5)#small = scipy.misc.imresize(image,0.5)#image2 = cv2.resize(image, (25, 50))  #cv2.putText(image, 'X',refPt[0],1,(255,0,255))#draw a rectangle around the region of interest
        #draw circle around egg's location        
        cv2.circle(small, refPt[0],19, (255, 0, 0), 2)
        cv2.imshow("image", small)
    if event == cv2.EVENT_RBUTTONUP:
        refPt = [(x,y)]
        for i in range(len(eggs)):

            #print 'x coord: %s < %s and %s > %s' %(x,eggs[i][0]+epsilon,x,eggs[i][0]-epsilon)
            #print 'y coord: %s < %s and %s > %s' %(y,eggs[i][1]+epsilon,y,eggs[i][1]-epsilon)
            if (abs(x-eggs[i][1])**2+abs(y-eggs[i][0])**2)**(.5)<epsilon:            
            #if x < eggs[i][1] + epsilon and x > eggs[i][1] - epsilon and y < eggs[i][0] + epsilon and y > eggs[i][0]-epsilon:
                del eggs[i]
                print 'point has been removed'
                break
        #subtracts one for every right click so even if it's a little off will only lose position data, not count data    
        counter = counter-1
        #cv2.circle(small,refPt[0],1,(255,255,255),2)
        #draw an x over cancelled egg detections
        cv2.putText(small,'X',refPt[0], 1, 5, (0,0,255), 5)#, cv2.LINE_AA)
        cv2.imshow('image',small)


for names in range(int(len(listdir(directory)))):
    
    filename = directory+listdir(directory)[names]
    print filename
    first_file =  directory+listdir(directory)[0]
    date = first_file.split('/')[3]
    #date = 'test'
    t0 = first_file.split('/')[4].split('png')[0].split('_')[3].split('.')[0]    
    t = filename.split('/')[4].split('png')[0].split('_')[3].split('.')[0]
    print t
    #loc = filename.split('/')[4].split('png')[0].split('_')[0]+'_'+filename.split('/')[4].split('png')[0].split('_')[1]
    loc = filename.split('loc')[1].split('_')[0]
    if names>0:
        prevloc = listdir(directory)[names-1].split('loc')[1].split('_')[0]
        print "prevloc",prevloc
        prevplate = listdir(directory)[names-1].split('plate')[1].split('_')[0]
    hr0 = t0.split('-')[0]
    minute0 = t0.split('-')[1]
    sec0 = t0.split('-')[2]    
    totT0 = 3600*float(hr0)+60*float(minute0)+float(sec0)    
    
    hr = t.split('-')[0]
    minute = t.split('-')[1]
    sec = t.split('-')[2]
    totT = 3600*float(hr)+60*float(minute)+float(sec)

    plate = filename.split('plate')[1].split('_')[0]
    
    #print "plate:",plate
    #print "filename: %s\ndate: %s\nt: %s\nloc: %s\nhr: %s\nmin: %s\nsec: %s" %(filename,date,t,loc,hr,minute,sec)    
    #print "t0: %s\nt: %s\nloc: %s\nhr0: %s\nminute0: %s\nsec0: %s\nhr: %s\nminute: %s\nsec: %s\ntotT: %s"\
    #%(t0,t,loc,hr0,minute0,sec0,hr,minute,sec,totT)
    elapsed = totT - totT0
    im = Image.open(filename)
    image = np.asarray(im)
    #io.imshow(image)
   # io.show()
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
        if area < 2000 and area>65 and properties[i].eccentricity<0.95 and properties[i].euler_number>-1:# and properties[i].minor_axis_length>10 and properties[i].major_axis_length<65:
            coord = properties[i].centroid
            eggs.append(coord)        
            if area>400:
                coord2 = (properties[i].centroid[0]+4,properties[i].centroid[1]+4)
                eggs.append(coord2)
                if area>700:
                    coord3 = (properties[i].centroid[0]+10,properties[i].centroid[1]-10)
                    eggs.append(coord3)
                    if area>900:
                        coord4 = (properties[i].centroid[0]-10,properties[i].centroid[1]+10)
                        eggs.append(coord4)
            
    
    counter = len(eggs)
    #print eggs
    print '%i eggs' %counter
    
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
    #plt.imshow(image,cmap = plt.gray())
    #plt.show()
#plan: use area (or filled_area) to find the eggs, centroid? or coords to get the location of them



          
    # load the image, clone it, and setup the mouse callback function
    #image = cv2.imread(im)
    #small = cv2.resize(image,(0,0),fx=0.25,fy=0.25)
    #clone = image.copy()
    cv2.namedWindow("image",flags = cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("image", click_and_count)
    small = image
    #small = cv2.pyrDown( image, image, ( image.shape[0]/2, image.shape[1]/2 ))
    # keep looping until the 'q' key is pressed
    datafile = '../Data/egg_count/%s.txt'%date
    datafile2 = '../Data/egg_count/position_data/%s'%(date)
    text= '#location    time     elapsed(sec)    egg_count#\n'
    #if names>0:    
        #print "loc: ", loc
        #print "prev_loc: ",listdir(directory)[names-1].split('/')[0].split('png')[0].split('_')[1]
    while True:
    	# display the image and wait for a keypress
    	#smaller = cv2.resize(image, (0,0), fx=0.5, fy=0.5)
    	cv2.imshow("image",small)#, small)
    	key = cv2.waitKey(0) #& 0xFF #cv2.waitKey(1) & 0xFF
     

    	# if the 'c' key is pressed, break from the loop
    	if key == ord("n"):          
             if names > 0:
                 if loc == prevloc and plate == prevplate : #and they are the same location/plate
                     duplicates = []            
                     prev_filename = '../Data/egg_count/position_data/%s/eggpos%s.txt' %(date,names-1)
                     with open(prev_filename,'r') as j:
                         prev_eggs = pickle.load(j)
                     #prev_eggs =  pickle.load(open(prev_filename,'rb'))#np.loadtxt(prev_filename ,dtype = list)
                     #print 'dese r da prev eggs:',prev_eggs
                     #for pos2 in range(len(eggs)):
                         #print eggs[pos2]
                     #(y2,x2) = eggs[0]
                     #print "\n\n\n\n\n\n Eggs:",eggs[0]
                     #print "length previous eggs list",len(prev_eggs)
                     #print 'prev eggs', prev_eggs
                     #print 'current eggs', eggs
                     for pos1 in range(len(prev_eggs)):
                         (y1,x1) = prev_eggs[pos1]
                         #print (y1,x1)
                         #(y2,x2) = eggs[pos1]
                         #print pos1
                         for pos2 in range(len(eggs)):
                             #print pos1
                             #print eggs[pos2]
                             (y2,x2) = eggs[pos2]
                             #print(y2,x2)
                     #    print "\n\n\n\n\n\n Eggs:",eggs
                     #    (y2,x2) = eggs[pos2]
                             #if x1<x2+epsilon and x1>x2-epsilon and y1<y2+epsilon and y1>y2-epsilon:
                             if (abs(x1-x2)**2+abs(y1-y2)**2)**(.5)<epsilon:
                                 #print "egg coord (%s,%s)"%(x2,y2)
                                 #print "%s recognized as a duplicate of %s" %(eggs[pos2],prev_eggs[pos1])
                                 if eggs[pos2] not in duplicates:                             
                                     duplicates.append(eggs[pos2]) #later delete duplicates bc if delete now, messes w for loop indexing
                                     break#print "duplicates", duplicates    
                                 #break
                                 #print "duplicate"
                 #print "count before duplicates removed: ", len(eggs)                             
                     print "no of duplicates",len(duplicates)
                     #print '"dupes"',duplicates
                     #print "\n\n\neggs",eggs

                     #for i in range(len(duplicates)):
                     #    eggs.remove(duplicates[i]) #duplicates are redundant
                         #print "1 egg removed"
                     #print 'count after dup removed = ',len(eggs)#counter
                     counter = counter-len(duplicates)
             if not path.exists(datafile):
                 with open(datafile,"w") as f:
                     f.write(text)
                     f.close()
             
             try: 
                makedirs(datafile2)
             except OSError:
                if not path.isdir(datafile2):
                    raise             
            # with open(datafile2,"r+") as h:
            #        pickle.dump(eggs,h)
             
             if not path.exists(datafile2+'/eggpos%i.txt'%names):
                 with open(datafile2+'/eggpos%i.txt'%names,"wb")as h:
                     #h = open(datafile2,"a")
                     #print "HELLOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"                      
                     #print "eggs", eggs
                     pickle.dump(eggs,h)                    
                     #h.write('%s'%eggs)
                     #h.close
             g=open(datafile,"a")
             text2='%s        %s        %s         %s\n' %(loc, t, totT, counter)
             g.write(text2)
             g.close()
             eggs = []
             if counter != 0:
                 #newName = im.split('.png')[0]+'_eggs_%i.png'%counter
                 #rename(im, newName)
                 counter = 0
             break
    	if key == ord("q"):
             #print click_locs + eggs
             #print eggs
             sys.exit()
                
             break

     

    # close all open windows
cv2.destroyAllWindows()
    