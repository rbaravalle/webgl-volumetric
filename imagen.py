import Image
import numpy as np
from math import floor, sqrt
from random import randint
import matplotlib
from matplotlib import pyplot as plt



maxX = 125
maxZ = 125
maxY = 125

I = Image.new('L',(maxZ,maxX*maxY),0.0)

field = np.zeros((maxX, maxY, maxZ)).astype(np.uint8) + np.uint8(255)
points = np.zeros((10*10*10*3000)).astype(np.uint8)
points2 = np.zeros((10*10*10*150)).astype(np.uint8)

r = 1;
h = 0;
lifetime = 240
ch = 60
pX = 0
pY = 0
pZ = 0

sep = 10
for i in range(0,maxX,sep):
    for j in range(0,maxY,sep):
        for k in range(0,maxZ,sep):
            i2 = i-maxX/2
            j2 = j-maxY/2
            k2 = k-maxZ/2
            r = int(sqrt((i2*i2+j2*j2+k2*k2))/3.0)
            if(r==0):
                lifetime = 30
            else:
                lifetime = int(floor(40.0/r))+1
            for l in range(lifetime):
                pX = i+randint(-r,r)
                pY = j+randint(-r,r)
                pZ = k+randint(-r,r)
                pX = max(0,min(pX,maxX-1))
                pY = max(0,min(pY,maxY-1))
                pZ = max(0,min(pZ,maxZ-1))
                field[pZ][pX][pY] = np.uint8(0)

sep = 2
for i in range(0,maxX,sep):
    for j in range(0,maxY,sep):
        for k in range(0,maxZ,sep):
            if(randint(0,5)>3):
                points[h] = i
                h = h+1
                points[h] = j
                h = h+1
                points[h] = k
                h = h+1



print "Next"
print len(points)
l = h
print "Total: ", l
for h in range(0,l,3):
    r = randint(1,2)
    if(h%2000 == 0): print h
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

h = 0
sep = 22
for i in range(0,maxX,sep):
    for j in range(0,maxY,sep):
        for k in range(0,maxZ,sep):
            if(randint(0,5)>2):
                points2[h] = i
                h = h+1
                points2[h] = j
                h = h+1
                points2[h] = k
                h = h+1

l = h
print "Bigger Bubbles"
print "Total: ", h
for h in range(0,l,3):
    r = randint(7,16)
    if(h%2000 == 0): print h
    for i in range(points2[h]-r-1,points2[h]+r+1):
        for j in range(points2[h+1]-r-1,points2[h+1]+r+1):
            for k in range(points2[h+2]-r-1,points2[h+2]+r+1):
                i2 = i-points2[h]+randint(0,10)
                j2 = j-points2[h+1]+randint(0,10)
                k2 = k-points2[h+2]+randint(0,10)
                if(i2*i2+j2*j2+k2*k2 <= r*r):
                    k2 = max(0,min(k,maxX-1))
                    i2 = max(0,min(i,maxY-1))
                    j2 = max(0,min(j,maxZ-1))
                    field[k2][i2][j2] = np.uint8(0)


print "Cortando"
for i in range(0,maxX):
    for j in range(0,maxY):
        for k in range(0,maxZ):
            i2 = i-maxX/2.0+randint(0,5)
            j2 = j-maxY/2.0+randint(0,5)
            k2 = k-maxZ/2.0+randint(0,5)
            if(j2*j2/3200+k2*k2/3800>1):
                field[k][i][j] = np.uint8(0)
            if(k2 > 65 or i2 > 25):
                field[k][i][j] = np.uint8(0)
                

plt.imshow(field[maxZ/2], cmap=matplotlib.cm.gray)
plt.show()

rowsPerSlice = maxY

for i in range(maxZ):
    I2 = Image.frombuffer('L',(maxX,maxY), np.array(field[i]).astype(np.uint8),'raw','L',0,1)
    I.paste(I2,(0,rowsPerSlice*i))

I.save('textures/imagen.png')
