import Image
import numpy as np
from math import floor, sqrt
from random import randint
import matplotlib
from matplotlib import pyplot as plt


def isin(x,y):
   v = x*x/6.5+y*y
   lastR = 0
   i = 0
   while(i < maxX/2):
      r = 1
      if(v > lastR*lastR and v < (lastR+r)*(lastR+r)): return True
      lastR = lastR + 2*r
      i = i+2
   return False

maxX = 128
maxZ = 128
maxY = 128

I = Image.new('L',(maxZ,maxX*maxY),0.0)

field = np.zeros((maxZ, maxX, maxY)).astype(np.uint8) + np.uint8(255)
points = np.zeros((10*10*10*3000)).astype(np.uint8)
points2 = np.zeros((10*10*10*1500)).astype(np.uint8)

r = 1;
h = 0;
lifetime = 240
ch = 60
pX = 0
pY = 0
pZ = 0

h = 0
sep =1
for i in range(0,maxX,sep):
    for j in range(0,maxY,sep):
         for k in range(0,15,sep):
             i2 = i-maxX/2.0
             j2 = j-maxY/2.0
             k2 = k-maxZ/2.0
             if(randint(0,100)>randint(60,100)):
                if(isin(i2,j2)):
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
    r = randint(1,3)
    if(h%6000 == 0): print h
    for i in range(points2[h]-r-1,points2[h]+r+1):
        for j in range(points2[h+1]-r-1,points2[h+1]+r+1):
             for k in range(points2[h+2]-r-1,points2[h+2]+r+1):
                 i2 = i-points2[h]#+randint(0,1)
                 j2 = j-points2[h+1]#+randint(0,1)
                 k2 = k-points2[h+2]#+randint(0,1)
                 if(i2*i2+j2*j2+k2*k2 < r*r):
                     x = max(0,min(i,maxX-1))
                     y = max(0,min(j,maxY-1))
                     z = max(0,min(k,maxZ-1))
                     field[z][x][y] = np.uint8(0)


print "Cortando"
for i in range(0,maxZ):
    for j in range(0,maxX):
        for k in range(0,maxY):
         i2 = i-maxX/2.0+randint(0,3)
         j2 = j-maxY/2.0+randint(0,3)
         k2 = k-maxZ/2.0+randint(0,3)
         if(j2*j2/3500+k2*k2/1500>1):
            field[i][j][k] = np.uint8(0)
         if(k > 80 or j > 120):
            field[i][j][k] = np.uint8(0)
                

plt.imshow(field[5], cmap=matplotlib.cm.gray)
plt.show()

rowsPerSlice = maxY

for i in range(maxZ):
    I2 = Image.frombuffer('L',(maxX,maxY), np.array(field[:,:,i]).astype(np.uint8),'raw','L',0,1)
    I.paste(I2,(0,rowsPerSlice*i))

I.save('textures/imagen.png')
