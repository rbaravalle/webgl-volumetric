import Image
import numpy as np
from math import floor
from random import randint
import matplotlib
from matplotlib import pyplot as plt

I = Image.new('L',(100,10000),0.0)


field = np.zeros((100,100,100)).astype(np.uint8) + np.uint8(180)
points = np.zeros((10*10*10*3000)).astype(np.uint8)

maxX = 100
maxZ = 100
maxY = 100

r = 6;
sep = 10;
h = 0;
lifetime = 240
ch = 60
pX = 0
pY = 0
pZ = 0

for i in range(0,maxX,sep):
    for j in range(0,maxY,sep):
        for k in range(0,maxZ,sep):
            if(randint(0,3)>1):
                s = lifetime#randint(1,lifetime)
                i2 = i-maxX/2
                j2 = j-maxY/2
                k2 = k-maxZ/2
                r = (i2*i2+j2*j2+k2*k2) 
                if(r==0):
                    r = 30
                else:
                    r = floor(16000/r)
                #print r
                lifetime = randint(10*r,20*r)
                ch = 1+floor(lifetime/500)
                for l in range(lifetime):
                    if(l%ch==0):
                        x = pX
                        y = pY
                        z = pZ
                    else: 
                        x = i
                        y = j
                        z = k
                    pX = x+randint(-r,r)
                    pY = y+randint(-r,r)
                    pZ = z+randint(-r,r)
                    pX = max(0,min(pX,maxX-1))
                    pY = max(0,min(pY,maxY-1))
                    pZ = max(0,min(pZ,maxZ-1))
                    field[pZ][pX][pY] = np.uint8(0)

for i in range(0,maxX,sep):
    for j in range(0,maxY,sep):
        for k in range(0,maxZ,sep):
            if(randint(0,3)>1):
                s = lifetime#randint(1,lifetime)
                i2 = i-maxX/2
                j2 = j-maxY/2
                k2 = k-maxZ/2
                r = (i2*i2+j2*j2+k2*k2) 
                if(r==0):
                    r = 30
                else:
                    r = floor(16000/r)
                #print r
                lifetime = randint(100*r,150*r)
                ch = 1+floor(lifetime/500)
                for l in range(lifetime):
                    if(l%ch==0):
                        x = pX
                        y = pY
                        z = pZ
                    else: 
                        x = i
                        y = j
                        z = k
                    pX = x+randint(-r,r)
                    pY = y+randint(-r,r)
                    pZ = z+randint(-r,r)
                    pX = max(0,min(pX,maxX-1))
                    pY = max(0,min(pY,maxY-1))
                    pZ = max(0,min(pZ,maxZ-1))
                    points[h] = pX
                    h = h+1
                    points[h] = pY
                    h = h+1
                    points[h] = pZ
                    h = h+1
                    field[pZ][pX][pY] = np.uint8(0)
print "ja"
print len(points)
for h in range(0,len(points)/70,3):
    r = randint(1,3)
    for i in range(points[h]-r,points[h]+r):
        for j in range(points[h+1]-r,points[h+1]+r):
            for k in range(points[h+2]-r,points[h+2]+r):
                i2 = i-points[h]
                j2 = j-points[h+1]
                k2 = k-points[h+2]
                if(i2*i2+j2*j2+k2*k2 < r*r):
                    k = max(0,min(k,maxX-1))
                    i = max(0,min(i,maxY-1))
                    j = max(0,min(j,maxZ-1))
                    field[k][i][j] = np.uint8(0)

print "Cilynder"
r = 50
for i in range(0,maxX):
    for j in range(0,maxY):
        for k in range(0,maxZ):
            i2 = i-floor(maxX/2)
            j2 = j-floor(maxY/2)
            k2 = k-floor(maxZ/2)
            if(k2*k2+j2*j2 > r*r):
                k = max(0,min(k,maxX-1))
                i = max(0,min(i,maxY-1))
                j = max(0,min(j,maxZ-1))
                field[k][i][j] = np.uint8(0)

plt.imshow(field[0], cmap=matplotlib.cm.gray)
plt.show()

rowsPerSlice = 100

for i in range(maxZ):
    I2 = Image.frombuffer('L',(maxX,maxY), np.array(field[i]).astype(np.uint8),'raw','L',0,1)
    I.paste(I2,(0,rowsPerSlice*i))

I.save('textures/imagen.png')
