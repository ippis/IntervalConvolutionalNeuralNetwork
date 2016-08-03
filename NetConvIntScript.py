from scipy import misc
import time
import png
import subprocess
import os
import random
import numpy as np
from initIntervals import *
from Erros import *
from sklearn.neural_network import MLPClassifier

# DADOS
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
		self.x = []
		self.y = []
	def divList(self,x,y):
		aux = []
		for i in range(len(x)):
			aux.append(x[i]/y)
		return aux
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
			# print "... find all data"
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
					self.y.append(classes)
					imageName = folderName+line
					imageName = imageName.replace("\n","")
					rd = png.Reader(imageName)

					#responsavel por pegar todas as informacoes a respeito da imagem, inclusive cada pixel
					self.w, self.h, pixels, metadata = rd.read_flat()
					newImage = []
					for i in range(0,len(pixels),2):
						newImage.append(IReal(pixels[i]))

					#adiciona a imagem ao conjunto de dados, representando dessa maneira uma imagem greyscale
					aux = []
					aux.append(newImage)
					self.x.append(aux)

			print str(classes)+": "+folderName+" ... OK"
			totClasses = classes
			totImages = len(self.x)

			#combined = zip(self.x, self.y)
			#random.shuffle(combined)
			#self.x = []
			#self.y = []
			#self.x[:], self.y[:] = zip(*combined)

			# print " "
			# print "... load dataset completed"


		except ValueError:
			print "now you should have two png files"


	def media(self,x):
		value = IReal(0.0)
		for i in xrange(len(x)):
			value += x[i]
		value = value / len(x)

		vari = IReal(0.0)
		for k in xrange(len(x)):
			vari+= powI((x[k] - value),2)

		print value
		vari = vari/(len(x)-1)
		print vari

	def ConvLayer(self,x,filter,bias,w2,h2,w1,h1,file,answer):
		#w1 e h1 sao assimensoes da saida
		# filtro consiste em um ou mais filtros (uma lista)
		# x delimita a imagem ou featuremap corrente
		print str(w2)+"X"+str(h2)
		outputFeatureMap = []
		filterDimension = int((len(filter)**(1.0/2.0)))

		arq1 = open(answer+"A1", 'a')
		arq2 = open(answer+"R1", 'a')
		arq3 = open(answer+"A2", 'a')
		arq4 = open(answer+"R2", 'a')
		fileNumbers = open(answer+"NUM", 'a')
		value = 0.0

		aux = []
		for fil in xrange(0,len(filter)):
			absoluto1 = 0.0
			absoluto2 = 0.0
			relativo = 0.0
			relativo2 = 0.0
			#Serve para variar entre os feature maps de uma imagem
			for indexFeatureMap in xrange(0,len(x)):
				#Para criar um feature map exatamente do valor correto tanto i quanto j, so iram variar para as posicoes que estarao criando
				for i in xrange(0,(h2)):
					for j in xrange(0,(w2)):
						value = IReal(0.0)
						#Realiza a convolucao do featuremap com o filtro, compensando pois ambos sao declarados como listas
						for k in xrange(0,filterDimension):

							for r in xrange(0,filterDimension):
								value+= (x[indexFeatureMap][j + r+(i*w2)+(k*w1)] * filter[fil][k*filterDimension])

							outputFeatureMap.append(value)
							a = float(file.pop(0))
							
							fileNumbers.write(str(a)+";"+str(value.inf)+";"+str(value.sup)+"\n")

							aux1,aux2 =  absolutError(a,value)
							absoluto1 += aux1
							absoluto2 += aux2
							aux3,aux4 = relativeError(a,value)
							relativo += aux3
							relativo2 += aux4

			absoluto1 = absoluto1 / len(outputFeatureMap)
			absoluto2 = absoluto2 / len(outputFeatureMap)
			relativo = relativo / len(outputFeatureMap)
			relativo2 = relativo2 / len(outputFeatureMap)
			arq1.write(str(absoluto1)+"\n")
			arq3.write(str(absoluto2)+"\n")
			arq2.write(str(relativo)+"\n")
			arq4.write(str(relativo2)+"\n")


			aux.append(outputFeatureMap)
			#self.media(outputFeatureMap)
			outputFeatureMap = []

		return aux


	def fullConnectedLayer(self,x,y,learnRate):
		answer = []
		x_train = []
		y_train = []
		x_test =[]
		y_test = []
		tam = len(x[0])
		for i in xrange(len(x)):
			avarage = [0.0]*len(x[0][0])
			avarage = initInterval(avarage,0.0)
			for j in xrange(len(x[0])):
				#Calcula a media de todos os campos de mesma coordenada de todos os featuremaps refentes a uma imagem
				for k in xrange(len(x[0][0])):
					avarage[k]+=x[0][j][k]

			x.pop(0)

			answer.append(self.divList(avarage,tam))

			avarage = []

		for i in range(int(len(answer)*learnRate)):
			x_train.append(answer.pop(0))
			y_train.append(y[i])



		for k in range(i+1,(len(x_train)+len(answer))):
			y_test.append(y[k])


		return x_train,answer,y_train,y_test

	def __calculatePontoMedio(self,x):
		newValues = []
		for i in xrange(len(x)):
			aux = []
			for k in xrange(len(x[0])):
				value = 0.0
				value = (x[0][k].inf + x[0][k].sup)/2.0
				aux.append(value)
			x.pop(0)
			newValues.append(aux)

		return newValues


	def __verifyTest(self,predictArray,y):
		correct = 0
		incorrect = 0
		for i in xrange(len(y)):
			## print(str(predictArray[i])+" "+str(y[i]))

			#Verifica porcentagem de acerto
			if(predictArray[i]==y[i]):
				correct+=1
			else:
				incorrect+=1

		self.__statistics(correct,incorrect)

	#v1 indica as corretas
	#v2 indica as incorretas
	def __statistics(self,v1,v2):
		#Total de gestos no conjunto de testes

		print("########################################")
		print("# ")
		print("#     Estatisticas de Treinamento")
		print("# ")
		print("#  Corretas "+str(v1))
		print("#  Incorretas "+str(v2))
		pc = 0.0
		pc = float(v1)/(v1+v2)
		print("#  % Predicoes corretas: "+str(pc))

		erro = 0.0
		erro = float(v2)/(v1+v2)
		print("#  % Erro: "+str(erro))
		print("########################################")


	# S indentifica o tamanho do passo para a realizacao da convolucao
	# p consiste no numero de zeros a ser preenchido na borda da imagem (1, adiciona 2 linhas e 2 colunas com zeros no inicio e no fim)
	# f indica a dimensao do filtro (lembrando que deve ser quadrada)

	def evaluateNetConv(self,fil,n_epochs,learn_rate,nameFile,f=3,s=1,p=0,totalFilters=1):
		#O filtro e criado a partir de uma tripla (centro da distribuicao, desvio padrao, quantidade de numeros)
		qtdNumFilter = f**2.0
		w2 = self.w
		h2 = self.h

		#Leitura para geracao dos erros absolutos e cada imagem
		arq = open(nameFile, 'r')
		texto = arq.readlines()
		## Responsavel pela criacao dos filtros atraves de uma gaussiana
		filter = fil
		bias = np.random.randint(0,2,2) #varia entre 0 ou 1
		#for i in xrange(0,totalFilters):
		#	aux =[]
		#	aux = np.random.normal(0,1,qtdNumFilter) #cria o filtro randomicamente com uma distribuicao normal (gaussian)
		#	aux = initInterval(aux,0.00000000001)
		#	filter.append(aux)
		#Fim filtro


		x_init = list(self.x)
		y_init = list(self.y)
		for i in xrange(0,n_epochs):
			#Atualiza para as dimensoes das imagens a serem trabalhadas no momento
			x_new = []

			# print "... running epoch "+str(i)
			self.w = w2
			self.h = h2

			#Calculo das novas dimensoes das imagens, considerando sempre o trabalho com imagens em grayscale
			w2 = (self.w - f + 2*p)/s + 1
			h2 = (self.h - f + 2*p)/s + 1
			#como sao imagens em grayscale entao a dimensao e sempre 1
			for k in xrange(len(x_init)):
				x_aux = []

				#Primeira camada de convolucao
				x_aux = self.ConvLayer(x_init.pop(0),filter,bias,w2,h2,self.w,self.h,texto,str(i)+str(0))

				#Nova atualizacao de valores
				w_aux = (w2 - f + 2*p)/s + 1
				h_aux = (h2 - f + 2*p)/s + 1

				#Segunda camada de convolucao
				x_new.append(self.ConvLayer(x_aux,filter,bias,w_aux,h_aux,w2,h2,texto,str(i)+str(1)))

			#Atualiza para a anova epoca
			w2 = w_aux
			h2 = h_aux
			x_init = list(x_new)

		#Inicio da preparacao para MLP
		x_new = []

		# print "... full connected layer"
		x_train, x_test, y_train, y_test = self.fullConnectedLayer(x_init,y_init,learn_rate)
		#Free memory
		x_init = []
		y_init = []

		self.y = []

		# print "... calculate ponto medio training set"
		x_train = self.__calculatePontoMedio(x_train)

		# print "... building training model"
		clf = MLPClassifier(algorithm='l-bfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
		# print "... training"
		clf.fit(x_train,y_train)

		# print "... validation"
		x_test = self.__calculatePontoMedio(x_test)
		classPredictndArray = clf.predict(x_test)
		self.__verifyTest(classPredictndArray,y_test)
