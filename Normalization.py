class Normalization(object):
    @staticmethod
    def minMaxEqualizer(list):
        listaNormalizada = []
        for image in list:
            imagemNormalizada = []
            maxValue = max(image)
            minValue = min(image)

            for pixel in image:
                nPixel = 0.0
                nPixel = (pixel - minValue)/ (maxValue - minValue)
                imagemNormalizada.append(nPixel)
            listaNormalizada.append(imagemNormalizada)

        return listaNormalizada
