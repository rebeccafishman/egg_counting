from scipy import loadtxt
import numpy as np
from skimage import io
import matplotlib.pyplot as plt
from scipy import *
from skimage.feature import match_template
from PIL import Image
import os
#script loc C:\Python27\Lib\site-packages\xy

filename = 'Data/egg_count/09-01-16-clip.txt'
loc,time_str = loadtxt(filename,skiprows = 1, unpack = True, usecols = [0,1],dtype = str)
tot_time,count = loadtxt(filename,skiprows = 1, unpack = True, usecols = [2,3],dtype = int)
#print count
plates = []

for i in range(len(loc)):
    if i>0:
        if not loc[i] in plates:
            plates.append(loc[i])
    else:
        plates.append(loc[i])
        
noPlates = len(plates)
noCycles = len(loc)/len(plates)
print "# of plates: %s\n#of cycles:%s" %(noPlates,noCycles)
print "plates",plates
fourW = [9,12,16]
twoW = []
for i in range(len(plates)):
    if not plates[i] in fourW:
        twoW.append(plates[i])


#print time_str
#t0 = 12:45 
#time = [1,6.5,12.5,18.5,24.5,30.5,36.5,42.5,48.5,54.5,60.5,66.5,72.5]
#time = [.5,7,13.33,19.75,25,30.5,36.66,42.70,48.75,55.33,61.33,67.33]
time = [.5,3.5,6.5,9.5,12.5,15.5,18.5,21.5]#,27.5]
#time = range(0,72,6)
#make an array instead of a gazillion lists!
matrix = np.zeros([noCycles,noPlates])



#location data given by:
matrix[:,1]
#cycle data given by
matrix[1]
'''
# row and column sharing
f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row')

#ax 1: Jarred's results
ax1.plot(x, y)
ax1.set_title('Sharing x per column, y per row')
#ax2: cumulative count (brood size)
ax2.scatter(x, y)
#ax3: 2 worm plates and 4 worm plates.
ax3.scatter(x, 2 * y ** 2 - 1, color='r')
#ax4 eggs laid/hr/hr
ax4.plot(x, 2 * y ** 2 - 1, color='r')
'''
#iterate thru each matrix element to create cumulative matrix

#Need to use a dictionary!



for i in range(noPlates):
    if int(plates[i]) in fourW:
        worms = 4.
    else:
        worms = 2.
    for cycle in range(noCycles):
        hr = count[noCycles*i+cycle]/worms
        #print hr
        #print (cycle,i)
        matrix[cycle,i] = hr

print matrix


dict = {}
for i in range(len(plates)):
    dict[plates[i]] = i
    
x12 = matrix[:,dict['12']]    

cumu = np.zeros([noCycles,32])
for cycle in range(noCycles):
    for plate in range(noPlates):
        if cycle == 0:
            cumu[cycle,plate]=count[cycle,plate]
        else:
            cumu[cycle,plate]=count[cycle,plate] + cumu[cycle-1,plate]
            


for i in range(noCycles):
    cycleMean = np.mean(matrix[i])
    x.append(cycleMean)

    #meanX = matrix[i,np.where(np.asarray(plates)==plates[i])[0][0]] 
    mean2 = np.mean([matrix[i,1],matrix[i,2]])
    mean16 = matrix[i,1]
    mean25 = matrix[i,2]
    x2.append(mean2)
    mean4 = np.mean([matrix[i,0],matrix[i,3],matrix[i,4]])
    mean14 = matrix[i,0]
    mean32 = matrix[i,3]
    mean9 = matrix[i,4]    
    x4.append(mean4)
    x31.append(mean9)
    x14.append(mean14)
    x16.append(mean16)
    x32.append(mean32)
    x9.append(mean9)
    x25.append(mean25)
for i in range(noCycles):              
    if i is 0:
        cumulative = x[0]
    else:
        cumulative = x[i]+xtot[i-1]
    xtot.append(cumulative)

for i in range(noCycles):              
    if i is 0:
        cumulative = x14[0]
    else:
        cumulative = x14[i]+x14tot[i-1]
    x14tot.append(cumulative)

for i in range(noCycles):              
    if i is 0:
        cumulative = x16[0]
    else:
        cumulative = x16[i]+x16tot[i-1]
    x16tot.append(cumulative)

for i in range(noCycles):              
    if i is 0:
        cumulative = x25[0]
    else:
        cumulative = x25[i]+x25tot[i-1]
    x25tot.append(cumulative)

for i in range(noCycles):              
    if i is 0:
        cumulative = x32[0]
    else:
        cumulative = x32[i]+x32tot[i-1]
    x32tot.append(cumulative)

for i in range(noCycles):              
    if i is 0:
        cumulative = x9[0]
    else:
        cumulative = x9[i]+x9tot[i-1]
    x9tot.append(cumulative)    

for i in range(noCycles):              
    if i is 0:
        cumulative = x2[0]
    else:
        cumulative = x2[i]+x2tot[i-1]
    x2tot.append(cumulative)

for i in range(noCycles):              
    if i is 0:
        cumulative = x4[0]
    else:
        cumulative = x4[i]+x4tot[i-1]
    x4tot.append(cumulative)        

for i in range(noCycles):              
    if i is 0:
        cumulative = x31[0]
    else:
        cumulative = x31[i]+x31tot[i-1]
    x31tot.append(cumulative)
   
ax=plt.axes()
#ax.plot(time,x,'c.')
#print "averages:",x
    
ax.set_xlabel("hrs")
ax.set_ylabel("no of eggs (cumulative)")
title="Eggs laid over time"
#title = 'Egg laying rate'

#cumulative egg count


#cumulative egg count/worm for 2 worm plates:

#cumulative egg count/worm for 4 worm plates:
#print len(xtot)
#ax.plot(time,xtot,'ko-')

ax.plot(time,x,'ko-')
#ax.plot(time,x14tot,'bo-',label = '11')
#ax.plot(time,x9tot,'ko-', label = '9')
#ax.plot(time,x16tot,'mo-', label = '16')
#ax.plot(time,x25tot,'go-',label = '26')
#ax.plot(time,x32tot,'ro-',label = '28')
#ax.plot(time,x31tot,'co-',label = '31')
#ax.plot(time,x14,'bo-')
#ax.plot(time,x9,'ko-')
#ax.plot(time,x16,'mo-')
#ax.plot(time,x25,'go-')
#ax.plot(time,x32,'ro-')
#ax.plot(time,x2tot,'ro-',label = '2 worm plates')
#ax.plot(time,x4tot,'bo-',label = '4 worm plates')
plt.legend(loc='upper left',prop={'size':13},fancybox=True,shadow=False)

#text= 'HR  EGG AVG\n0        %s\n3        %s\n6        %s\n9        %s' %(x[0],x[1],x[2],x[3])

#ax.text(0.7,0.7,text,transform=ax.transAxes)
ax.set_title(title)
plt.axis([-1,60,-1,450])
#plt.axis([0,70,0,300])
#plt.axis([15,26,.0035,.0065])
#plt.savefig("layingRate_07-22.png")
plt.show()
