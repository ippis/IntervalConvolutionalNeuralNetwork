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

        dist = float(pixel)
        for viz in neighborhood:
            aux = (math.fabs(pixel - float(viz)))/2
            if(aux!=0 and aux < dist):
                dist = aux
            aux = 0

        inf = pixel
        sup = pixel

        if (dist != float(pixel)):
            inf = pixel-dist if (pixel - dist) >= 0 else 0
            sup = pixel+dist if (pixel + dist) <= 255 else 255
        #print str(pixel)+" "+str(inf)+" "+str(sup)
        return inf,sup

    def __createIntervalImage(self,min,max):
        img = Image.new('L', (512,512))
        img.putdata(min)
        img.save('minImage.png')

        img2 = Image.new('L', (512,512))
        img2.putdata(max)
        img2.save('maxImage.png')
