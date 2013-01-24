import Image
import numpy as np
from math import floor, sqrt
from random import randint
import matplotlib
from matplotlib import pyplot as plt


def isin(x,y):
   v = x*x+y*y
   lastR = 0
   i = 0
   r = 3
   #if(randint(0,100)>98): r = 1
   while(lastR < maxX/2):
      #r = aux
      if(v > lastR*lastR and v < (lastR+r)*(lastR+r)): return True
      lastR = lastR + 2*r
      #i = i+2*r
   cond = False
   if(randint(0,1000)>700): cond = True
   return False or cond

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
         for k in range(0,25,sep):
             i2 = i-maxX/2.0
             j2 = j-maxY/2.0
             k2 = k-maxZ/2.0
             if(randint(0,100)>randint(90,100)):
                if(isin(i2,j2)):
                    points2[h] = i
                    h = h+1
                    points2[h] = j
                    h = h+1
                    points2[h] = k
                    h = h+1

l = h
print "Making Bubbles"
print "Total: ", h
for h in range(0,l,3):
    r = 2#randint(1,2)
    x = points2[h] - maxX/2
    y = points2[h+1] - maxY/2
    z = points2[h+2] - maxZ/2
    #if(x*x+y*y<200 and randint(0,1000) > 500): r = randint(2,3)
    if(randint(0,1000) > 995): r = 11
    if(h%6000 == 0): print h
    for i in range(points2[h]-r-1,points2[h]+r+1):
        for j in range(points2[h+1]-r-1,points2[h+1]+r+1):
             for k in range(points2[h+2]-r-1,points2[h+2]+r+1):
                 i2 = i-points2[h]+randint(1,2)
                 j2 = j-points2[h+1]+randint(1,2)
                 k2 = k-points2[h+2]+randint(1,2)
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
         if(j2*j2/3000+k2*k2/3000>1):
            field[i][j][k] = np.uint8(0)
         #if( j > 120):
         #   field[i][j][k] = np.uint8(0)
                

plt.imshow(field[2], cmap=matplotlib.cm.gray)
plt.show()

rowsPerSlice = maxY

for i in range(maxZ):
    I2 = Image.frombuffer('L',(maxX,maxY), np.array(field[:,:,i]).astype(np.uint8),'raw','L',0,1)
    I.paste(I2,(0,rowsPerSlice*i))

I.save('textures/imagen.png')
