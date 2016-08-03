#Librarys
import png
from initIntervals import *
import math
from PIL import Image



class IntervalImage():
    def __init__(self,width,height):
        self.w = width
        self.h = height

    def neighborhood4(self,image):
        mini = []
        maxi = []
        min = -1
        max = -1
        imageInterval = []
        for i in xrange(self.h):
            for k in xrange(self.w):
                neighborhood = []
                # O O O
                # 0 x 0
                # 0 0 0
                try:
                    neighborhood.append(image[(i*self.w)+k])
                except IndexError:
                    None

                # O O O
                # x 0 0
                # 0 0 0
                try:
                    if(k!=0):
                        neighborhood.append(image[((i*self.w)+k)-1])

                except IndexError:
                    None

                # O O O
                # 0 0 x
                # 0 0 0
                try:
                    if(k!=self.w-1):
                        neighborhood.append(image[((i*self.w)+k)+1])
                except IndexError:
                    None

                # O O O
                # 0 0 0
                # 0 x 0
                try:
                    neighborhood.append(image[(i*self.w)+k+self.w])
                except IndexError:
                    None

                # O x O
                # 0 0 0
                # 0 0 0

                try:
                    neighborhood.append(image[(i*self.w)+k-self.w])
                except IndexError:
                    None


                min,max = self.__distNeighborhood(neighborhood)
                imageInterval.append(IReal(min,max))
        #        mini.append(min)
        #        maxi.append(max)

        #self.__createIntervalImage(mini,maxi)
        return imageInterval

    def neighborhood8(self,image):
        mini = []
        maxi = []
        min = -1
        max = -1
        imageInterval = []
        for i in xrange(self.h):
            for k in xrange(self.w):
                neighborhood = []

                # O O O
                # 0 x 0
                # 0 0 0
                try:
                    neighborhood.append(image[(i*self.w)+k])
                except IndexError:
                    None

                # O O O
                # x 0 0
                # 0 0 0
                try:
                    if(k!=0):
                        neighborhood.append(image[((i*self.w)+k)-1])

                except IndexError:
                    None

                # O O O
                # 0 0 x
                # 0 0 0
                try:
                    if(k!=self.w-1):
                        neighborhood.append(image[((i*self.w)+k)+1])
                except IndexError:
                    None

                # O O O
                # 0 0 0
                # 0 x 0
                try:
                    neighborhood.append(image[(i*self.w)+k+self.w])
                except IndexError:
                    None

                # O x O
                # 0 0 0
                # 0 0 0

                try:
                    neighborhood.append(image[(i*self.w)+k-self.w])
                except IndexError:
                    None

                # x O O
                # 0 0 0
                # 0 0 0
                try:
                    if(k!=0):
                        neighborhood.append(image[(i*self.w)+k-self.w-1])
                except IndexError:
                    None

                # O O x
                # 0 0 0
                # 0 0 0
                try:
                    if(k!=self.w-1):
                        neighborhood.append(image[(i*self.w)+k-self.w+1])

                except IndexError:
                    None

                # O O O
                # 0 0 0
                # 0 0 x

                try:
                    if(k!=self.w-1):
                        neighborhood.append(image[(i*self.w)+k+self.w+1])

                except IndexError:
                    None

                # O O O
                # 0 0 0
                # x 0 0
                try:
                    if(k!=0):
                        neighborhood.append(image[(i*self.w)+k+self.w-1])
                except IndexError:
                    None

                min,max = self.__distNeighborhood(neighborhood)
                imageInterval.append(IReal(min,max))
                mini.append(min)
                maxi.append(max)

        self.__createIntervalImage(mini,maxi)
        return imageInterval


    def __distNeighborhood(self,neighborhood):

        pixel = neighborhood[0] #PIXEL INICIAL

        dist = pixel
        for viz in neighborhood:
            aux = math.fabs(pixel - viz)
            if(aux!=0 and aux < dist):
                dist = aux
            aux = 0


        inf = pixel-dist
        sup = pixel+dist
        #print str(pixel)+" "+str(inf)+" "+str(sup)
        return inf,sup

    def __createIntervalImage(self,min,max):
        img = Image.new('L', (512,512))
        img.putdata(min)
        img.save('minImage.png')

        img2 = Image.new('L', (512,512))
        img2.putdata(max)
        img2.save('maxImage.png')


rd = png.Reader("lena.png")


w, h, pixels, metadata = rd.read_flat()
a = IntervalImage(w,h)
print w
print h
newImage = []
for i in range(len(pixels)):
	newImage.append(pixels[i])

a.neighborhood8(newImage)
