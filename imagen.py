import Image
import numpy as np
from math import floor
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
sep1 = 25;
h = 0;
lifetime = 240
ch = 60
pX = 0
pY = 0
pZ = 0

print "H first:", h

sep = int(floor(sep1/4))
for i in range(0,maxX,sep):
    for j in range(0,maxY,sep):
        for k in range(0,maxZ,sep):
            if(randint(0,3)>0):
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
                lifetime = randint(1*r,3*r)
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

sep = sep1
for i in range(20,maxX-20,sep):
    for j in range(20,maxY-20,sep):
        for k in range(20,maxZ-20,sep):
            if(randint(0,3)>=2):
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
                lifetime = randint(3*r,80*r)
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
                    #field[pZ][pX][pY] = np.uint8(0)



print "ja"
print len(points)
print "HASta. ", len(points)/60
print "H: ", h
for h in range(0,h/3,3):
    if(randint(0,10) > 2):
        r = randint(0,1)
    else:
        r = randint(2,4)
    #if(h%1000 == 0):
    #    print h
    for i in range(points[h]-r,points[h]+r+1):
        for j in range(points[h+1]-r,points[h+1]+r+1):
            for k in range(points[h+2]-r,points[h+2]+r+1):
                i2 = i-points[h]
                j2 = j-points[h+1]
                k2 = k-points[h+2]
                if(i2*i2+j2*j2+k2*k2 < r*r):
                    k2 = max(0,min(k,maxX-1))
                    i2 = max(0,min(i,maxY-1))
                    j2 = max(0,min(j,maxZ-1))
                    field[k2][i2][j2] = np.uint8(0)

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

rowsPerSlice = maxY

for i in range(maxZ):
    I2 = Image.frombuffer('L',(maxX,maxY), np.array(field[i]).astype(np.uint8),'raw','L',0,1)
    I.paste(I2,(0,rowsPerSlice*i))

I.save('textures/imagen.png')
