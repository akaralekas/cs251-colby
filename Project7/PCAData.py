# CS 251
# Spring 2016
#------------------------------------

# File: PCAData.py
# Author/Editor: Anthony Karalekas
# Collaboration: S.Parrott, J.Saul, B.Doyle
# Help: CP Majgaard
# Date: Apr. 3, 2016
# Assignment: Project 6

#------------------------------------

# Edited by Tony Karalekas
# CS251 Spring 2016
# Project 6


#imports
import numpy as np
import data
import scipy.stats as sc
from copy import *

#Executing a PCA analysis creates three things. 
#First, it generates the eigenvectors, which specify a new basis, 
# or set of axes, for the data. 
#Second, it generates the eigenvalues, which 
# indicate how important each eigenvector is to representing the data. 
#Third, projecting the data from its original data space 
# into the PCA space generates a set of transformed data.

#-----Lab 6 Work------
class PCAData(data.Data):
	def __init__(self, headers, pdata, evecs, evals, mean):
		#inherit our original data.py class
		data.Data.__init__(self)	
		
		#store eval, evec, menas, headers in new fields
		self.evals = evals #Holds the Eigen values 
		self.evecs = evecs #Holds Eigen Vectors
		self.data_mean = mean #Holds Mean Data values
		self.ogHeaders = headers
		
		self.matrix_data = pdata 
					
		#fill out everything else defined in Data __init__
		#help from Bruce Maxwell and B.Doyle
		#fill out raw data
		for i in range(self.matrix_data.shape[0]):
			row = []
			for j in range(self.matrix_data.shape[1]):
				row.append( str(self.matrix_data[i,j]) )
			self.raw_data.append(row)

		#help from B.Doyle, Theo Satloff and Bruce Maxwell
		# fill out header2matrix and header2raw
		for i, value in enumerate(headers):
			header = eval("'PCA' + str(i)")
			self.raw_headers.append(header)
			self.raw_types.append('numeric')
			self.header2raw[value] = i
			self.header2matrix[header] = i

	def get_eigenvalues(self):
		evals= np.matrix(deepcopy(self.evals))
		return evals

	def get_eigenvectors(self):
		evecs = deepcopy(self.evecs)
		return evecs

	def get_data_means(self):
		dmean = deepcopy(self.data_mean)
		return dmean

	def get_data_headers(self):
		ogHeaders = deepcopy(self.ogHeaders)
		return ogHeaders
