import Image
import numpy as np
from math import floor, sqrt
from random import randint
import matplotlib
from matplotlib import pyplot as plt



maxX = 100
maxZ = 100
maxY = 100

I = Image.new('L',(maxZ,maxX*maxY),0.0)

field = np.zeros((maxX, maxY, maxZ)).astype(np.uint8) + np.uint8(255)
points = np.zeros((10*10*10*3000)).astype(np.uint8)

r = 2;
sep1 = 15;
h = 0;
lifetime = 240
ch = 60
pX = 0
pY = 0
pZ = 0

sep = 2
for i in range(0,maxX,sep):
    for j in range(0,maxY,sep):
        for k in range(0,maxZ,sep):
            i2 = i-maxX/2
            j2 = j-maxY/2
            k2 = k-maxZ/2
            r = int(sqrt((i2*i2+j2*j2+k2*k2)))
            if(r==0):
                lifetime = 30
            else:
                lifetime = int(floor(150.0/r))+1
            for l in range(lifetime):
                pX = i+randint(-r,r)
                pY = j+randint(-r,r)
                pZ = k+randint(-r,r)
                pX = max(0,min(pX,maxX-1))
                pY = max(0,min(pY,maxY-1))
                pZ = max(0,min(pZ,maxZ-1))
                field[pZ][pX][pY] = np.uint8(0)

sep = 5
for i in range(20,maxX-20,sep):
    for j in range(20,maxY-20,sep):
        for k in range(20,maxZ-20,sep):
            if(randint(0,5)>3):
                points[h] = i
                h = h+1
                points[h] = j
                h = h+1
                points[h] = k
                h = h+1



print "Next"
print len(points)
#print "H: ", h
for h in range(0,h,3):
    r = randint(2,4)
    for i in range(points[h]-r-1,points[h]+r+1):
        for j in range(points[h+1]-r-1,points[h+1]+r+1):
            for k in range(points[h+2]-r-1,points[h+2]+r+1):
                i2 = i-points[h]
                j2 = j-points[h+1]
                k2 = k-points[h+2]
                if(i2*i2+j2*j2+k2*k2 <= r*r):
                    k2 = max(0,min(k,maxX-1))
                    i2 = max(0,min(i,maxY-1))
                    j2 = max(0,min(j,maxZ-1))
                    field[k2][i2][j2] = np.uint8(0)



plt.imshow(field[maxZ/2], cmap=matplotlib.cm.gray)
plt.show()

rowsPerSlice = maxY

for i in range(maxZ):
    I2 = Image.frombuffer('L',(maxX,maxY), np.array(field[i]).astype(np.uint8),'raw','L',0,1)
    I.paste(I2,(0,rowsPerSlice*i))

I.save('textures/imagen.png')
