from scipy import misc
import time
import png
import subprocess
import os
import numpy as np


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

##################INFORMACOES DE TREINAMENTO###################
totImages = 0 #Numero de imagens lidas
totClasses = -1 #Numero de classes diferentes
percent_train = 0.8
################################################################

class ConvNetInterval(object):
	def __init__(self):
		self.w = 0
		self.h = 0
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
					self.w, self.h, pixels, metadata = rd.read_flat()
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
			print x[0]
			print len(x[0])

		except ValueError:
			print "now you should have two png files"

	def ConvLayer(self,x,filter,bias,w2,h2,w1,h1):
		#w1 e h1 sao assimensoes da saida
		# filtro consiste em um ou mais filtros (uma lista)
		# x delimita a imagem ou featuremap corrente

		outputFeatureMap = []
		filterDimension = int((len(filter)**(1.0/2.0)))

		value = 0.0
		#Para criar um feature map exatamente do valor correto tanto i quanto j, so iram variar para as posicoes que estarao criando
		for i in xrange(0,(h2)):
			for j in xrange(0,(w2)):
				value = 0.0
				#Realiza a convolucao do featuremap com o filtro, compensando pois ambos sao declarados como listas
				for k in xrange(0,filterDimension):

					for r in xrange(0,filterDimension):
						value+= x[j + r+(i*w2)+(k*w1)] * filter[k*filterDimension]

				outputFeatureMap.append(value+bias)

		return outputFeatureMap

	# S indentifica o tamanho do passo para a realizacao da convolucao
	# p consiste no numero de zeros a ser preenchido na borda da imagem (1, adiciona 2 linhas e 2 colunas com zeros no inicio e no fim)
	# f indica a dimensao do filtro (lembrando que deve ser quadrada)

	def evaluateRealConv(self,n_epochs,learn_rate,f=3,s=1,p=0,totalFilters=1):
		#O filtro e criado a partir de uma tripla (centro da distribuicao, desvio padrao, quantidade de numeros)
		qtdNumFilter = f**2.0
		w2 = self.w
		h2 = self.h
		filter = np.random.normal(0,1,qtdNumFilter*totalFilters) #cria o filtro randomicamente com uma distribuicao normal (gaussian)
		bias = np.random.randint(0,2,1) #varia entre 0 ou 1

		x_init = list(x)
		for i in xrange(0,n_epochs):
			#Atualiza para as dimensoes das imagens a serem trabalhadas no momento
			x_new = []

			print "... running epoch "+str(i)
			self.w = w2
			self.h = h2

			#Calculo das novas dimensoes das imagens, considerando sempre o trabalho com imagens em grayscale
			w2 = (self.w - f + 2*p)/s + 1
			h2 = (self.h - f + 2*p)/s + 1
			#como sao imagens em grayscale entao a dimensao e sempre 1
			for k in xrange(0,len(x)):
				x_aux = []

				#Primeira camada de convolucao
				x_aux = self.ConvLayer(x_init[k],filter,bias[0],w2,h2,self.w,self.h)

				#Nova atualizacao de valores
				w_aux = (w2 - f + 2*p)/s + 1
				h_aux = (h2 - f + 2*p)/s + 1

				#Segunda camada de convolucao
				x_new.append(self.ConvLayer(x_aux,filter,bias[0],w_aux,h_aux,w2,h2))

			#Atualiza para a anova epoca
			w2 = w_aux
			h2 = h_aux
			x_init = list(x_new)
		print(w2)
		print(h2)
		print(len(x_init))

a = ConvNetInterval()
a.load()

a.evaluateRealConv(1,0.8,2,1,0,1)
