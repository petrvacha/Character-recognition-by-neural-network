# -*- coding: utf-8 -*-
###############################################################################
#
# Autor: Petr Vácha
#	Název: Backpropagation NN
#
###############################################################################
import math
import picture
import sys, os
import perceptron

firstLayer = 6
hiddenLayer = 11
lastLayer = 10
mi = 0.5


directory = "./tset/"
directoryTest = "./cset/"

if len(sys.argv) == 3:
		if sys.argv[1] == "digit":
			directory = "./tset/"
			directoryTest = "./cset/"
		elif sys.argv[1] == "hand":
			directory = "./tsada/"
			directoryTest = "./csada/"
		mi = float(sys.argv[2])
elif len(sys.argv) != 1:
	sys.stderr.write("ERROR: Bad arguments.\n")
	sys.exit()
	

##directory = "./tsada/"
##directoryTest = "./csada/"

inputPerceptrons = []
hiddenPerceptrons = []
lastPerceptrons = []
vectors = {}


###############################################################################
def learn(firstLayer =4, hiddenLayer =7, lastLayer =10, lamda =0.5, mi =0.6):
	tset = os.listdir(directory)
	##print tset
	##sys.exit()##
	
	for n in tset:
		p = picture.Picture(os.path.join(directory, n))
		v = p.getVector()
		filename = n.split(".")
		vectors[filename[0]] = v
	##	p.printVector(5)
	##	print

	GlobalErr = 0.0
	iteration = 0
	while (GlobalErr == 0.0 or GlobalErr > 1.8 and iteration < 500):
		if  iteration == 10 or iteration == 25 or iteration == 50 or iteration == 100 or iteration % 200 == 0:
			print iteration, u"Globální chyba: ", GlobalErr
		iteration = iteration+1
		##if GlobalErr:
		##	print lastPerceptrons[0].getOutput(), lastPerceptrons[1].getOutput(), lastPerceptrons[2].getOutput(), lastPerceptrons[5].getOutput()

		GlobalErr = 0
		for k in vectors.keys():
			for i in range(firstLayer):
				if len(inputPerceptrons) < firstLayer:
					f = perceptron.Perceptron(len(vectors[k]), lamda)
					inputPerceptrons.append(f)
				for y in range(len(vectors[k])):
					inputPerceptrons[i].setInput(y+1, vectors[k][y])
				inputPerceptrons[i].computeBaseFunction()
				inputPerceptrons[i].computeOutput()

			for i in range(hiddenLayer):
				if len(hiddenPerceptrons) < hiddenLayer:
					h = perceptron.Perceptron(firstLayer, lamda)
					hiddenPerceptrons.append(h)
				for y in range(firstLayer):
					hiddenPerceptrons[i].setInput(y+1, inputPerceptrons[y].getOutput())
				hiddenPerceptrons[i].computeBaseFunction()
				hiddenPerceptrons[i].computeOutput()

			for i in range(lastLayer):
				if len(lastPerceptrons) < lastLayer:
					l = perceptron.Perceptron(hiddenLayer, lamda)
					lastPerceptrons.append(l)
				for y in range(hiddenLayer):
					lastPerceptrons[i].setInput(y+1, hiddenPerceptrons[y].getOutput())
				lastPerceptrons[i].computeBaseFunction()
				lastPerceptrons[i].computeOutput()

			Err = 0
			for i in range(lastLayer):
				if i == int(k[0]):
					Err = Err + (1 - lastPerceptrons[i].getOutput())**2
					lastPerceptrons[i].setDelta((1 - lastPerceptrons[i].getOutput())*lamda*lastPerceptrons[i].getOutput()*(1 - lastPerceptrons[i].getOutput()))
				else:
					Err = Err + (0 - lastPerceptrons[i].getOutput())**2
					lastPerceptrons[i].setDelta((0 - lastPerceptrons[i].getOutput())*lamda*lastPerceptrons[i].getOutput()*(1 - lastPerceptrons[i].getOutput()))
			GlobalErr = GlobalErr + 0.5 * Err

	####Backpropagation
			for i in range(hiddenLayer):
				suma = 0
				for sd in range(lastLayer):
					suma = suma + lastPerceptrons[sd].getDelta() * lastPerceptrons[sd].getWeight(i+1)

				hiddenPerceptrons[i].setDelta(suma * lamda * hiddenPerceptrons[i].getOutput() * (1 - hiddenPerceptrons[i].getOutput()))

			for i in range(firstLayer):
				suma = 0
				for sd in range(hiddenLayer):
					suma = suma+ hiddenPerceptrons[sd].getDelta() * hiddenPerceptrons[sd].getWeight(i+1)

				inputPerceptrons[i].setDelta(suma * lamda * inputPerceptrons[i].getOutput() * (1 - inputPerceptrons[i].getOutput()))

			for i in range(0, firstLayer):
				for sd in range(0, inputPerceptrons[i].getNumberInput()):
					inputPerceptrons[i].setWeight(sd, inputPerceptrons[i].getWeight(sd) + mi * inputPerceptrons[i].getDelta() * inputPerceptrons[i].getInput(sd))

			for i in range(0, hiddenLayer):
				for sd in range(0, hiddenPerceptrons[i].getNumberInput()):
					hiddenPerceptrons[i].setWeight(sd, hiddenPerceptrons[i].getWeight(sd) + mi * hiddenPerceptrons[i].getDelta() * hiddenPerceptrons[i].getInput(sd))

			for i in range(0, lastLayer):
				for sd in range(0, lastPerceptrons[i].getNumberInput()):
					lastPerceptrons[i].setWeight(sd, lastPerceptrons[i].getWeight(sd) + mi * lastPerceptrons[i].getDelta() * lastPerceptrons[i].getInput(sd))


###############################################################################
def checkNN():
	print u"Výsledek naučené neuronové sítě:"
	for k in vectors.keys():
		for i in range(firstLayer):
			for y in range(len(vectors[k])):
				inputPerceptrons[i].setInput(y+1, vectors[k][y])
			inputPerceptrons[i].computeBaseFunction()
			inputPerceptrons[i].computeOutput()

		for i in range(hiddenLayer):
			for y in range(firstLayer):
				hiddenPerceptrons[i].setInput(y+1, inputPerceptrons[y].getOutput())
			hiddenPerceptrons[i].computeBaseFunction()
			hiddenPerceptrons[i].computeOutput()

		for i in range(lastLayer):
			for y in range(hiddenLayer):
				lastPerceptrons[i].setInput(y+1, hiddenPerceptrons[y].getOutput())
			lastPerceptrons[i].computeBaseFunction()
			lastPerceptrons[i].computeOutput()

		max = 0.0
		for y in range(lastLayer):
			if max < lastPerceptrons[y].getOutput():
				max = lastPerceptrons[y].getOutput()

		for y in range(lastLayer):
			if int(k[0]) == y:
				if max == lastPerceptrons[y].getOutput():
					print k, "OK", lastPerceptrons[y].getOutput()
				else:
					print k, "FAIL", lastPerceptrons[y].getOutput()

###############################################################################
def testNN():
	vectors = {}
	print u"Test neuronové sítě:"
	tset = os.listdir(directoryTest)

	for n in tset:
		p = picture.Picture(os.path.join(directoryTest, n))
		v = p.getVector()
		filename = n.split(".")
		vectors[filename[0]] = v

	for k in vectors.keys():
		for i in range(firstLayer):
			for y in range(len(vectors[k])):
				inputPerceptrons[i].setInput(y+1, vectors[k][y])
			inputPerceptrons[i].computeBaseFunction()
			inputPerceptrons[i].computeOutput()

		for i in range(hiddenLayer):
			for y in range(firstLayer):
				hiddenPerceptrons[i].setInput(y+1, inputPerceptrons[y].getOutput())
			hiddenPerceptrons[i].computeBaseFunction()
			hiddenPerceptrons[i].computeOutput()

		for i in range(lastLayer):
			for y in range(hiddenLayer):
				lastPerceptrons[i].setInput(y+1, hiddenPerceptrons[y].getOutput())
			lastPerceptrons[i].computeBaseFunction()
			lastPerceptrons[i].computeOutput()

		max = 0.0
		for y in range(lastLayer):
			if max < lastPerceptrons[y].getOutput():
				max = lastPerceptrons[y].getOutput()

		for y in range(lastLayer):
			if int(k[0]) == y:
				if max == lastPerceptrons[y].getOutput():
					print k, "OK", lastPerceptrons[y].getOutput()
				else:
					print k, "FAIL", lastPerceptrons[y].getOutput()



learn(firstLayer, hiddenLayer, lastLayer, 0.5, mi)
checkNN()
testNN()
		
