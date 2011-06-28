# -*- coding: utf-8 -*-
###############################################################################
#
# Autor: Petr Vácha
# Název: Backpropagation NN
#
###############################################################################
import sys, os
import random

#wahy = (0.1, 0.4, -0.5, 0.2, -0.2, -0.3, 0.1, -0.4, 0.2, -0.4, 0.0, 0.5, 0.1)

class Perceptron:
	"""Perceptron"""
	def __init__(self, numberInput, lamda):
		self.__numberInput = numberInput
		self.__weight = [] 
		self.__inpt = []
		self.__outpt = 0
		self.__u = 0
		self.__lamda = lamda
		self.__e = 2.71828182845904523536
		self.setWeight(0, 0)
		self.setInput(0, 1)
		self.setWeights()

	def __repr__(self):
		outStr = ""
		outStr += "weights: "
		outStr += "\n"
		for w in range(len(self.__weight)):
			outStr += str(self.__weight[w])
			outStr += "\n"
		outStr += "input: "
		for i in range(len(self.__inpt)):
			outStr += str(self.__inpt[i])
			outStr += "\n"
		outStr += "u: "
		outStr += str(self.__u)		
		outStr += "\n"
		outStr += "output: "
		outStr += str(self.__outpt)
		outStr += "\n"
		return outStr


	def setWeight(self, index, weight):
		if index < len(self.__weight):
			self.__weight[index] = weight
		else:
			self.__weight.append(weight)

	def setWeights(self):
		for i in range(1, self.__numberInput + 1):
			self.setWeight(i, random.random()-0.5)
			#self.setWeight(i,wahy[i-1]) #debug


	def setInput(self, index, inpt):
		if index < len(self.__inpt):
			self.__inpt[index] = inpt
		else:
			self.__inpt.append(inpt)

	def setOutput(self, outpt):
			self.__outpt = outpt
	
	def setU(self, u=0):
		self.__u = u

	def getNumberInput(self):
		return self.__numberInput
	
	def getU(self):
		return self.__u

	def getWeight(self, index):
		if index < len(self.__weight):
			return self.__weight[index]

	def getInput(self, index):
		if index < len(self.__inpt):
			return self.__inpt[index]

	def getOutput(self):
		return self.__outpt

	def computeBaseFunction(self):
		self.setU()
		for nI in range(0, self.__numberInput + 1):
			self.__u = self.__u + self.getWeight(nI) * self.getInput(nI)

	def computeOutput(self):
		y= 1/(1+self.__e**(-self.__lamda*self.__u)) #sigmoidální aktivační funkce
		self.setOutput(y)

	def setDelta(self, delta):
		self.__delta = delta

	def getDelta(self):
		return self.__delta
