from PythonMagick import *
import sys
import Image as im
import subprocess
import time
import Image
import os
import PythonMagick


class imgTransform(object):
	
	
	def initialize(self,nameFile,geometry):
		listOfFiles = open(nameFile,'r')
		folders=self.createFolders(listOfFiles)
		self.editingImages(folders,geometry)
		
		
	def createFolders(self,listOfFiles):
		findFolder = 0
		allFolders = []
		for lines in listOfFiles:
			if('./' in lines):
				findFolder+=1
				folder = []
				nameFolder = lines.replace("./","")
				folder.append(nameFolder.replace(":\n",""))
				allFolders.append(folder)		
			elif(findFolder!=0):
				allFolders[findFolder-1].append(lines.replace("\n",""))
		return allFolders
	
	def editingImages(self,folders,geometry):
		
		for folds in folders:
			nameFold = ""
			positionFor = 0
			for imgs in folds:
				
				if(positionFor==0):
					nameFold = imgs
				elif(len(imgs)):
					img=Image.open(nameFold+'/'+imgs).convert('LA')
				
					size = 66,72
					
					img = img.resize((66,72))
					img.save(nameFold+'/'+imgs)
						
					
				positionFor+=1	
						
				
				
						
if __name__ == '__main__':	
	try:
		#Executa comando ls recursivo automaticamente e grava no arquivo lista.txt
		allFiles = open('file_list.txt','w')
		p = subprocess.Popen(["ls", "-R"],stdout = allFiles)
		time.sleep(3)
		processImg = imgTransform()
		processImg.initialize('file_list.txt',sys.argv[1])
	except ValueError:
		print "now you should have two png files"
