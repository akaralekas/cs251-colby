# Template by Bruce Maxwell
# Spring 2015
# CS 251 Project 8
#
# Classifier class and child definitions

# CS 251
# Spring 2016
#----edited by AJKaralekas
#------------------------------------
# File: data.py
# Author/Editor: Anthony Karalekas
# Collaboration: J.Saul, B.Doyle, S.Parrott
# Help: CP Majgaard
# Date: Apr. 24, 2016
# Assignment: Project 8

#------------------------------------

import sys
import data
import analysis as an
import numpy as np

#=============Lab 8 Work====================

class Classifier:

	def __init__(self, type):
		'''The parent Classifier class stores only a single field: the type of
		the classifier.	 A string makes the most sense.
		'''
		self._type = type

	def type(self, newtype = None):
		'''Set or get the type with this function'''
		if newtype != None:
			self._type = newtype
		return self._type
		
#================================================
#================================================	
#~~~~~~~~~~~~Project 8, Task 1~~~~~~~~~~~~~~~~~~~
#================================================
#Write the two functions in the Classifier parent class
# for creating and printing a confusion matirx. 

	#confusion_matrix method should build a numpy matrix showing 
	# the number of data points in a category classified as each output category. 
	def confusion_matrix( self, truecats, classcats ):
		'''Takes in two Nx1 matrices of zero-index numeric categories and
		computes the confusion matrix. The rows represent true
		categories, and the columns represent the classifier output.
		'''
		unique1, mapping = np.unique( np.array(truecats.T), return_inverse=True)
		unique2, mapping = np.unique( np.array(classcats.T), return_inverse=True)

		unique1 = unique1.tolist()
		unique2 = unique2.tolist()

		unique1 += unique2
		unique = np.unique(np.array(unique1)).tolist()

		confmatrix = np.matrix(np.zeros((len(unique), len(unique))))

		for i in range(truecats.shape[0]):
			confmatrix[truecats[i,0],classcats[i,0]] += 1

		return confmatrix
		
	#help from CP majgaard	
	#The confusion_matrix_str method should convert it into
	# a string that does a nice job of printing out the matrix.
	def confusion_matrix_str( self, cmtx ):
		'''Takes in a confusion matrix and returns a string suitable for printing.'''

		#help with design from CP
		s = '%10s|' %("Classif.->")
		for i in range(cmtx.shape[1]):
			s += "%9dC" %(i,)
		s += "\n"
		for i in range(cmtx.shape[0]):
			s += "%9dT|" %(i,)
			for j in range(cmtx.shape[1]):
				s += "%10d" %(cmtx[i,j],)
			s+="\n"
		return s

	def __str__(self):
		'''Converts a classifier object to a string.  Prints out the type.'''
		return str(self._type)

#=============Lab 8, Task 2====================
class NaiveBayes(Classifier):
	'''NaiveBayes implements a simple NaiveBayes classifier using a
	Gaussian distribution as the pdf.
	
	'''

	def __init__(self, dataObj=None, headers=[], categories=None):
		'''Takes in a Data object with N points, a set of F headers, and a
		matrix of categories, one category label for each data point.'''
		# call the parent init with the type
		Classifier.__init__(self, 'Naive Bayes Classifier')

		# store the headers used for classification
		self.headers = headers

		# number of classes and number of features
		self.num_classes = 0
		self.num_features = 0

		# original class labels
		self.class_labels = []

		# unique data for the Naive Bayes: means, variances, scales
		self.class_means = np.matrix([])
		self.class_vars = np.matrix([])
		self.class_scales = np.matrix([])

		# if given data,
			# call the build function

		if dataObj != None:
			self.build(dataObj.getData(self.headers), categories)

	def build( self, A, categories ):
		'''Builds the classifier give the data points in A and the categories'''
		A = np.matrix(A)
		# figure out how many categories there are and get the mapping (np.unique)
		unique, mapping = np.unique( np.array(categories.T), return_inverse=True)
		self.num_classes = unique.size
		self.class_labels = unique
		#print A.shape[1]
		self.num_features = A.shape[1]

		# create the matrices for the means, vars, and scales
		# the output matrices will be categories (C) x features (F)
		self.class_means  = np.matrix(np.zeros((self.num_classes, self.num_features)))
		self.class_vars	  = np.matrix(np.zeros((self.num_classes, self.num_features)))
		self.class_scales = np.matrix(np.zeros((self.num_classes, self.num_features)))

		# compute the means/vars/scales for each class
		for i in range(self.num_classes):
			#print an.mean(None,None,matrix = A[(mapping==i),:])
			self.class_means[i,:] = an.mean(None,None,matrix = A[(mapping==i),:])
			self.class_vars[i,:] = np.var(A[(mapping==i),:], axis=0, ddof=1)

		for i in range(self.class_scales.shape[0]):
			for j in range(self.class_scales.shape[1]):
				self.class_scales[i, j] = (1/np.sqrt (2 * np.pi * self.class_vars[i,j]))
		# store any other necessary information: # of classes, # of features, original labels
		return
		
	def classify( self, A, return_likelihoods=False ):
		'''Classify each row of A into one category. Return a matrix of
		category IDs in the range [0..C-1], and an array of class
		labels using the original label values. If return_likelihoods
		is True, it also returns the NxC likelihood matrix.
		'''

		#error check to see if A has the same number of columns as the class means
		if A.shape[1] != self.class_means.shape[1]:
			print "Yikes!"
			return

		#make a matrix that is N x C to store the probability of each 
		# class for each data point
		P = np.matrix(np.zeros((A.shape[0], self.num_classes)))
		# a matrix of zeros that is N (rows of A) x C (number of classes)

		#calculate the probabilities by looping over the classes
		# with numpy-fu you can do this in one line inside a for loop
		for i in range(self.num_classes):
			P[:,i] = np.prod( np.multiply( self.class_scales[i,:], np.exp(-np.square((A-self.class_means[i,:]))/(2*self.class_vars[i,:]) )), axis=1 )

		#calculate the most likely class for each data point
		cats = np.asarray(np.argmax(P, axis=1))
		c = cats.flatten()

		#use the class ID as a lookup to generate the original labels
		labels = [self.class_labels[i] for i in c.tolist()]
		labels = np.matrix(labels).T

		if return_likelihoods:
			return cats, labels, P

		return cats, labels


	def __str__(self):
		'''Make a pretty string that prints out the classifier information.'''
		s = "\nNaive Bayes Classifier\n"
		for i in range(self.num_classes):
			s += 'Class %d --------------------\n' % (i)
			s += 'Mean	: ' + str(self.class_means[i,:]) + "\n"
			s += 'Var	: ' + str(self.class_vars[i,:]) + "\n"
			s += 'Scales: ' + str(self.class_scales[i,:]) + "\n"

		s += "\n"
		return s

	def write(self, filename):
		'''Writes the Bayes classifier to a file.'''
		# extension
		return

	def read(self, filename):
		'''Reads in the Bayes classifier from the file'''
		# extension
		return

#=============Lab 8, Task 3====================	   
class KNN(Classifier):

	def __init__(self, dataObj=None, headers=[], categories=None, K=None):
		'''Take in a Data object with N points, a set of F headers, and a
		matrix of categories, with one category label for each data point.'''

		# call the parent init with the type
		Classifier.__init__(self, 'KNN Classifier')

		# store the headers used for classification
		self.headers = headers
		# number of classes and number of features
		self.num_classes = 0
		self.num_features = 0
		# original class labels
		self.class_labels = []
		self.class_means = np.matrix([])

		# unique data for the KNN classifier: list of exemplars (matrices)
		self.exemplars = []

		# if given data,
			# call the build function

		if dataObj != None:
			self.build(dataObj.getData(self.headers), categories)

	def build( self, A, categories, K = None ):
		'''Builds the classifier give the data points in A and the categories'''

		# figure out how many categories there are and get the mapping (np.unique)
		unique, mapping = np.unique( np.array(categories.T), return_inverse=True)
		self.num_classes = unique.size
		self.class_labels = unique

		# self.class_means	= np.matrix(np.zeros((self.num_classes, self.num_features)))
		#
		# for i in range(self.num_classes):
		#	  #print an.mean(None,None,matrix = A[(mapping==i),:])
		#	  self.class_means[i,:] = an.mean(None,None,matrix = A[(mapping==i),:])

		# for each category i, build the set of exemplars
		for i in range(self.num_classes):
			# if K is None
			if K == None:
				# append to exemplars a matrix with all of the rows of A where the category/mapping is i
				self.exemplars.append(A[(mapping == i),:])
			# else
			else:
				# run K-means on the rows of A where the category/mapping is i
				codebook = an.kmeans_init(A[(mapping==i),:], K)
				# append the codebook to the exemplars
				self.exemplars.append(codebook)

		return
		
#=============Lab 8, Task 4==================== 
	def classify(self, A, K=3, return_distances=False):
		'''Classify each row of A into one category. Return a matrix of
		category IDs in the range [0..C-1], and an array of class
		labels using the original label values. If return_distances is
		True, it also returns the NxC distance matrix.

		The parameter K specifies how many neighbors to use in the
		distance computation. The default is three.'''

		# error check to see if A has the same number of columns as the class means

		# make a matrix that is N x C to store the distance to each class for each data point
		D = np.matrix(np.zeros((A.shape[0],self.num_classes)))
		# a matrix of zeros that is N (rows of A) x C (number of classes)

		# for each class i
		for i in range(self.num_classes):
			# make a temporary matrix that is N x M where M is the number of examplars (rows in exemplars[i])
			# calculate the distance from each point in A to each point in exemplar matrix i (for loop)
			temp = np.matrix(np.zeros((A.shape[0], self.exemplars[i].shape[0])))
			for exemplar in range(self.exemplars[i].shape[0]):
				temp[:,exemplar] = np.sum(np.square(A - self.exemplars[i][exemplar,:]), axis=1)
			# sort the distances by row
			temp.sort(axis=1)
			# sum the first K columns
			summa = np.sum(temp[:,:K], axis=1)
			# this is the distance to the first class
			D[:,i] = summa

		# calculate the most likely class for each data point
		cats = np.asarray(np.argmin(D, axis=1)) # take the argmin of D along axis 1

		# use the class ID as a lookup to generate the original labels
		c = cats.flatten()
		
		# use the class ID as a lookup to generate the original labels
		labels = [self.class_labels[i] for i in c.tolist()]
		labels = np.matrix(labels).T

		if return_distances:
			return cats, labels, D

		return cats, labels

	def __str__(self):
		'''Make a pretty string that prints out the classifier information.'''
		s = "\nKNN Classifier\n"
		for i in range(self.num_classes):
			s += 'Class %d --------------------\n' % (i)
			s += 'Number of Exemplars: %d\n' % (self.exemplars[i].shape[0])
			s += 'Mean of Exemplars	 :' + str(np.mean(self.exemplars[i], axis=0)) + "\n"

		s += "\n"
		return s


	def write(self, filename):
		'''Writes the KNN classifier to a file.'''
		# extension
		return

	def read(self, filename):
		'''Reads in the KNN classifier from the file'''
		# extension
		return