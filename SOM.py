import numpy
import decimal

class SOM():

	def __init__(self,N,maxK,tolerance,Tdistance,floatGamma,alfaInicial,alfaFinal,variableGamma):

		self.N = N
		self.centers = []
		self.centersNames = []
		self.trainingVectors = []
		self.maxK = maxK
		self.tolerance = tolerance
		self.gammaK = floatGamma
		self.Tdistance = float(Tdistance)
		self.alfaInicial = alfaInicial
		self.alfaFinal = alfaFinal
		self.variableGamma = variableGamma
	
	def getGammaK(self):
		
		if(self.variableGamma == True):
			return self.getVariableGamma()
		return self.gammaK

	def getVariableGamma(self):
		return 1.0/(float(10)+float(self.k)+1.0)

	def setGammaK(self,floatGamma):
		self.gammaK = floatGamma

	def addInitialCenter(self,cVector,cName):

		self.centers.append(cVector)
		self.centersNames.append(cName)

	def addTrainingVector(self,tVector):

		self.trainingVectors.append(tVector)

	def trainCenter(self,xVector,updateIndex,vecinity):

		return self.updateCenter(updateIndex,xVector,vecinity)

	def updateCenter(self,index,xVector,vecinity):

		
		aux = self.centers[index]
		#self.centers[index] = numpy.add(self.centers[index],(numpy.dot(self.getGammaK(),numpy.dot(vecinity,numpy.subtract(xVector,self.centers[index])))))
		self.centers[index] = numpy.add(self.centers[index],numpy.dot(numpy.dot(self.getGammaK(),vecinity),numpy.subtract(xVector,self.centers[index])))
		tolerance = numpy.linalg.norm(numpy.subtract(self.centers[index],aux))
		
		return tolerance

	def doTraining(self):

		toleranceBreak = False

		for k in range(self.maxK):
			self.k=k
			for tVector in self.trainingVectors:
				nup = 0
				for i in range(len(self.centers)):

					vecinity = self.calculateVecinity(tVector,self.centers[i],k)
					
					if(vecinity > self.Tdistance):
						tolerance = self.trainCenter(tVector,i,vecinity)
						nup+=1

					if(vecinity > self.Tdistance and tolerance < self.tolerance):
						toleranceBreak = True
						print "Iteraciones rotas por limite de tolerancia"
						break

				if(nup == 0 ):
					for i in range(len(self.centers)):
						vecinity = self.calculateVecinity(tVector,self.centers[i],k)
						tolerance = self.trainCenter(tVector,i,vecinity)
				if(toleranceBreak == True):
					break
			if(toleranceBreak==True):
				break		
		
			


	def calculateVecinity(self,v1,v2,k):

		'''En los apuntes los elevados a k empiezan desde la iteracion 1... En el codigo empiezan desde 0, por eso se pone k+1'''
		ak = numpy.dot(self.alfaInicial,numpy.power((self.alfaFinal/self.alfaInicial),((k+1)/float(self.maxK))))
		dividend = numpy.power(numpy.linalg.norm(numpy.subtract(v1,v2)),2.0)
		divisor = numpy.dot(2.0,numpy.power(ak,2.0))

		vecinity = numpy.exp(numpy.dot(-1.0,(dividend/divisor)))

		return vecinity

	def getCenters(self):
		return self.centers

	def clasify(self,vector):

		return self.centersNames[self.nearestCenter(vector)]

	def nearestCenter(self,xVector):

		mini = float('inf')
		index = None
		for i in range(len(self.centers)): 
			dist = numpy.linalg.norm(numpy.subtract(xVector,self.centers[i]))
			if(dist < mini):
				mini = dist
				index = i
		return index

if __name__ == "__main__":
	toleranceLimit = numpy.power(10.0,-6)
	som = SOM(N = 2,maxK = 5,tolerance = toleranceLimit,Tdistance = 0.2,floatGamma = 0,alfaInicial = 1.0,alfaFinal = 0.8,variableGamma = True)
	#centers
	som.addInitialCenter([1.0,4.0],"Clase 1")
	som.addInitialCenter([7.0,2.0],"Clase 2")
	#training vectors
	som.addTrainingVector([1.0,3.0])
	som.addTrainingVector([1.0,5.0])
	som.addTrainingVector([2.0,2.0])
	som.addTrainingVector([6.0,3.0])
	som.addTrainingVector([6.0,4.0])
	som.addTrainingVector([7.0,3.0])

	som.doTraining()
	print ">>>>>>> Ejemplo diapo 25"
	print ">>> Centros finales"
	print som.getCenters()
	vector = [6.0,2.0]
	print ">>> El vector ", vector ," pertenece a la clase ", som.clasify(vector)