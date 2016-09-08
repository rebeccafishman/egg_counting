# -*- coding: utf-8 -*-
"""
Created on Wed Apr 06 16:03:33 2016

@author: Greencomp
"""
import os
import numpy as np
from skimage import io
from PIL import Image
import matplotlib.pyplot as plt
from skimage.feature import match_template
from time import strftime

#script loc C:\Python27\Lib\site-packages\xy

#pic loc C:\Users\Melissa\Desktop\Becca\Data\good

#for i in range(len(os.listdir('../Data/26-May-2016/'))):    
#    filename = os.listdir('../Data/26-May-2016')[i]
xmax, ymax = 2592, 1944
'''
delty1 = 25.
deltx1 = 251.
delty2 = 132.
deltx2 = 15.

deltx1 =  246
delty1 =  111

delty1 = 80.
deltx1 = 248
delty2 = 161#132. 
deltx2 = 67.

delty2 = 135
deltx2 = 43
delty1 = 66
deltx1 = 260  
'''
#for z = -2.85 @ zoom3000:
deltx1 = 250#270#266
delty2 = 136
deltx2 = 110#65#44
delty1= 65

directory = '../Data/individualPics/09-06-2016/'#'../Data/19-May-2016/'
for i in range(int(len(os.listdir(directory))/4)):
    #finalSize = np.zeros((2*ymax+delty1-delty2,2*xmax+deltx2-deltx1))
    pos1 = directory+os.listdir(directory)[4*i]
    pos2 = directory+os.listdir(directory)[4*i+1]
    pos3 = directory+os.listdir(directory)[4*i+2]
    pos4 = directory+os.listdir(directory)[4*i+3]
    datetime = pos1.split('/')
    date = datetime[3]
    time = datetime[4]
    print pos1
    #filename = 'loc_1_17-29-02.png'
    a = 80
    finalSize = np.zeros((2*ymax+delty1-delty2+a,2*xmax+deltx2-deltx1))
    #net_displ = [0,44.147,46.957,55.606,63.702,69.029,76.662,79.756,85.0,84.971,95.016,92.962,90.973,86.023,]
    im1 = Image.open(pos1).convert('L')
    image1 = np.asarray(im1, dtype=int)
    im2 = Image.open(pos2).convert('L')
    image2 = np.asarray(im2, dtype=int)
    im3 = Image.open(pos3).convert('L')
    image3 = np.asarray(im3, dtype=int)
    im4 = Image.open(pos4).convert('L')
    image4 = np.asarray(im4, dtype=int)
   #image3 = 'manyegg.png'
   #io.imshow(image3)
   #io.show()
    tempbox1 = [2400,2540,100,700]#[2439,2586,10,300]
    tempbox2 =  [1900,2570,1812,1943]#[0,262,1730,1943]#[145,673,1808,1943]
    template1 = image2[tempbox1[2]:tempbox1[3],tempbox1[0]:tempbox1[1]] #UPPER left (x,y) = (tempbox[0],tempbox[2])
    #so now need to match up (2439,300) in im2 with x,y in im1
    template2 = image3[tempbox2[2]:tempbox2[3],tempbox2[0]:tempbox2[1]]
    
    '''
    result1 = match_template(image1, template1)
    ij = np.unravel_index(np.argmax(result1), result1.shape)
    x1, y1 = ij[::-1] #use this result to paste together.

    result2 = match_template(image2, template2)
    ij = np.unravel_index(np.argmax(result2), result2.shape)
    x2, y2 = ij[::-1] #use this result to paste together.
    
    #print 'x=%d \ny=%d' %(x,y)
    #x,y = (94,40)
    #ymax,xmax=image2.shape
    deltx1 = (xmax - tempbox1[0])+x1
    delty1 = abs(y1 - tempbox1[2])
    deltx2 = abs(tempbox2[0] - x2)
    delty2 = (ymax - tempbox2[2]) + y2
    '''   
    #delty1 = 30,24
    #deltx1 = 247,251
    #delty2 = 148,132
    #deltx2 = 22,15
    
    #finalSize2 = np.zeros((2*ymax+delty1-delty2,2*xmax+deltx2-deltx1))
    #finalSize3 = np.zeros((2*ymax+delty1-delty2,2*xmax+deltx2-deltx1))
    #finalSize4 = np.zeros((2*ymax+delty1-delty2,2*xmax+deltx2-deltx1))

    fSymax,fSxmax = finalSize.shape
    print 'delty1 = %d \n deltx1 = %d \ndelty2 = %d \n deltx2 = %d' %(delty1,deltx1,delty2,deltx2)

    #finalSize[ymax-.5*delty2:2*ymax-delty2,deltx2 + xmax:fSxmax]+=image1[.5*delty2:ymax,deltx1:xmax]
    #finalSize[ymax - .5*delty2 +50:fSymax,deltx2:xmax+deltx2]+=image2[.5*delty2-delty1:ymax,0:xmax]    
    #finalSize[ymax - .5*delty2:fSymax,deltx2:xmax+deltx2]+=image2[.5*132-80:1944,0:xmax]
    #finalSize[delty1+50:ymax - .5*delty2+50,0:xmax]+=image3[0:ymax - .5*delty2-delty1,0:xmax]    
    #finalSize[0:ymax-.5*delty2,xmax:fSxmax-deltx2]+=image4[0:ymax-.5*delty2,deltx1:xmax]

    finalSize[ymax:2*ymax-delty2,xmax:fSxmax]+=image1[delty2:ymax,deltx1 - deltx2:xmax]
    finalSize[ymax-.5*delty2 +a :fSymax,deltx2:xmax]+=image2[.5*delty2-delty1:ymax,0:xmax-deltx2] 
    finalSize[delty1+a:ymax+a - .5*delty2,0:xmax]+=image3[0:ymax - .5*delty2-delty1,0:xmax]
    finalSize[0:ymax,xmax:fSxmax-deltx2]+=image4[0:ymax,deltx1:xmax]

    #name = '/All%d.png'%i
    #name = 'All%d.npz'%i
    print time
   # print finalSize, np.max(finalSize),#0/0
   
    #np.savez(name, im=finalSize)
    #print "input max", np.amax(image1)
    #print "np.max",np.max(finalSize)
    #print "np.min ",np.min(finalSize)
    #print image1.shape
    #print finalSize.shape
    #plt.imsave(name,All)
    #plt.imshow(name)
    #plt.show()
    when = strftime('%m-%d-%y')
    stitchedDir = '../Data/stitched/'+when +'/'
    try:
        os.makedirs(stitchedDir)
    except OSError:
        if not os.path.isdir(stitchedDir):

            raise

    io.imsave(stitchedDir+time,finalSize/255)#255.)
    #io.imshow(finalSize)#/510)
    #io.show()
    #print finalSize
    #im = Image.fromarray(finalSize/255.,mode = 'L')
    #im = Image.open('All0.png')
    #print np.max(np.asarray(im))
    #im = Image.fromarray(np.asarray(im)/255.,mode ='L')
    #im = Image.new('L',finalSize.shape)
    #im.putdata(finalSize)

    #im.save(name)
   # im.show(im)
    #im = None
print 'done'
