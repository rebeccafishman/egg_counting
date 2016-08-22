from scipy import loadtxt
import numpy as np
from skimage import io
import matplotlib.pyplot as plt
from scipy import *
from skimage.feature import match_template
from PIL import Image
import os
#script loc C:\Python27\Lib\site-packages\xy


loc,time_str = loadtxt('../Data/egg_count/test.txt',skiprows = 1, unpack = True, usecols = [0,1],dtype = str)
tot_time,count = loadtxt('../Data/egg_count/test.txt',skiprows = 1, unpack = True, usecols = [2,3],dtype = int)
#print count

#print time_str
time = [0,3,6,9,12,15,18]#[0,3,6,9]
first = []
second = []
third = []
fourth = []

for i in range((len(count)+1)/3):
    
    hr1 = count[3*i]/2
    hr2 = count[3*i+1]/2
    hr3 = count[3*i+2]/2
    #hr4 = count[4*i+3]/2
    print "hr1 ",hr1
    print "hr2 ",hr2
    print "hr3 ",hr3
#    print 'hr4 ',hr4
    first.append(hr1)
    second.append(hr2)
    third.append(hr3)
    #fourth.append(hr4)
    
print "count:",count
print "first:",first
print "second:",second
print "third:",third
first.remove(-33)
second.remove(-29)
print first
print np.mean(first)
print np.mean(second)
print np.mean(third)
#print "fourth:", fourth
x = [12,29,42,54,int(np.mean(first)),int(np.mean(second)),int(np.mean(third))]#,int(np.mean(fourth))]
ax=plt.axes()
ax.plot(time,x,'c.-')
print "averages:",x


plt.legend(loc='upper left',prop={'size':13},fancybox=True,shadow=False)
ax.set_xlabel("hrs")
ax.set_ylabel("no of eggs")
title="Eggs laid over time"



#text= 'HR  EGG AVG\n0        %s\n3        %s\n6        %s\n9        %s' %(x[0],x[1],x[2],x[3])

#ax.text(0.7,0.7,text,transform=ax.transAxes)
ax.set_title(title)
plt.axis([-1,60,-1,450])
#plt.axis([15,26,.0035,.0065])
plt.savefig("calibration_mr.png")
plt.show()
