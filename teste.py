from scipy import misc
import time
import png
import subprocess
import os

# DADOS
x=[]
y=[]
x_train = []
x_test = []
y_train = []
y_test = []
#####################################3

################## INFORMACOES GERAIS DAS IMAGENS #############
channels = 1
w = 0
h = 0

##################INFORMACOES DE TREINAMENTO###################
totImages = 0 #Numero de imagens lidas
totClasses = -1 #Numero de classes diferentes
percent_train = 0.8
################################################################

class ConvNetInterval(object):
	def load(self):
		try:
			pathFiles = "dataset.txt"
			fileProcess = open(pathFiles,'w')

			#Realiza o levantamento de todo dataset presente na pasta
			p = subprocess.Popen(["ls", "-R"],stdout = fileProcess)
			allFiles = open(pathFiles,'r')

			#tempo para gerar o processo acima
			time.sleep(3)

			classes = -1
			print "... find all data"
			folderName = ""
			for line in allFiles:
				#Verifica existencia de um diretorio
				if('./' in line):
					if(classes!=-1):
						print str(classes)+": "+folderName+" ... OK"
					classes+=1
					folderName = line[2:len(line)-2]+"/"

				elif((classes!=-1)and(len(line)!=1)): #realiza a leitura de cada imagem, presente em cada diretorio
					#como as classes sao os diretorios, entao cada imagem contem sua classe
					y.append(classes)
					imageName = folderName+line
					imageName = imageName.replace("\n","")
					rd = png.Reader(imageName)

					#responsavel por pegar todas as informacoes a respeito da imagem, inclusive cada pixel
					w, h, pixels, metadata = rd.read_flat()
					newImage = []		
					for i in range(0,len(pixels),2):
						newImage.append(pixels[i])
					#adiciona a imagem ao conjunto de dados, representando dessa maneira uma imagem greyscale
					x.append(newImage)
					
			print str(classes)+": "+folderName+" ... OK"
			totClasses = classes
			totImages = len(x)
			print " "
			print "... load dataset completed"
			

		except ValueError:
			print "now you should have two png files"






a = ConvNetInterval()
a.load()
#print w
#print h
#pixels[len(pixels)-1]= 20
#print pixels

#print len(pixels)
#print metadata
