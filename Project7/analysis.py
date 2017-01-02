# CS 251
# Spring 2016
#------------------------------------

# File: analysis.py
# Author/Editor: Anthony Karalekas
# Collaboration: S.Parrott, J.Saul, B.Doyle
# Help: CP Majgaard
# Date: Apr. 18, 2016
# Assignment: Project 7

#------------------------------------

# Edited by Tony Karalekas
# CS251 Spring 2016
# Project 7

import Tkinter as tk
import tkFont as tkf
import math
import random
import numpy as np
from data import *
import scipy.stats as sc
import scipy.cluster.vq as vq
import PCAData
import copy

values = []
#Takes in a list of column headers and 
#the Data object and returns a list of 2-element lists 
#with the minimum and maximum values for each column. 
#The function is required to work only on numeric data types.

#Help from Bruce
# help from CP majgaard
def data_range(column_headers, data):
	colNum = []
	mx = data.matrix_data
	
	for col in column_headers:
		colNum.append(data.header2matrix[col])	
	
	mins =	mx.min(axis = 0)
	maxs = mx.max(axis = 0)
	
	data_range = [] 
	for col in colNum:
		pair = []
		pair.append(mins.item(col))
		pair.append(maxs.item(col))
		data_range.append(pair)
	return data_range
		
	

# Takes in a list of column headers and 
# the Data object and returns a list of 
# the mean values for each column. 
# Use the built-in numpy functions to execute this calculation.
#Help from Bruce
#help from CP majgaard
def mean(column_headers, data):
	colNum = []
	mx = data.matrix_data
	
	for col in column_headers:
		colNum.append(data.header2matrix[col])
	
	mean = mx.mean(axis=0)
	means = []
	for col in colNum:
		means.append(mean.item(col))
		
	return means
# takes in a list of column headers and the Data object 
# and returns a list of the standard deviation for each specified column. 
# Use the built-in numpy functions to execute this calculation.
#Help from Bruce
#help from CP majgaard
def stdev(column_headers, data):
	colNum = []
	mx = data.matrix_data
	
	for col in column_headers:
		colNum.append(data.header2matrix[col])
	
	devs = mx.std(axis=0, ddof =1)
	stdev = []
	for col in colNum:
		stdev.append(devs.item(col))
		
	return stdev

# takes in a list of column headers and the Data object and 
# returns a matrix with each column normalized so its minimum value is 
# mapped to zero and its maximum value is mapped to 1.
# worked alongside CP Majgaard
def normalize_columns_separately( column_headers, data):
	a = data.get_data(column_headers)
	
	def operation(a):
		min = np.min(a)
		max = np.max(a)
		return (a-min)/(max-min) 
		
	return np.apply_along_axis(operation,0, a)


# Takes in a list of column headers and the Data object and 
# returns a matrix with each entry normalized so that the minimum value 
# (of all the data in this set of columns) is mapped to zero and 
# its maximum value is mapped to 1.
# worked alongside CP Majgaard
def normalize_columns_together(column_headers, data):	
	a = data.get_data(column_headers)
	min = np.min(a)
	max = np.max(a)
	
	return (a-min)/(max-min)

#EXTENSION 1
#sums the data in each column
def sum(column_headers, data):	
	colNum = []
	mx = data.matrix_data
	
	for col in column_headers:
		colNum.append(data.header2matrix[col])
	
	sum = mx.sum(axis=0)
	sums = []
	for col in colNum:
		sums.append(sum.item(col))
		
	return sums
	
#EXTENSION 2
#round to nearest
def round(column_headers, data):	
	a = data.get_data(column_headers)
	round = a.round(1)
	return round
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#======Project 5, Task 3===========
#help from bruce
def linear_regression(d, ind, dep):
  # assign to y the column of data for the dependent variable
  # assign to A the columns of data for the independent variables
  #	   It's best if both y and A are numpy matrices
  # add a column of 1's to A to represent the constant term in the 
  #	   regression equation.	 Remember, this is just y = mx + b (even 
  #	   if m and x are vectors).
	y = d.get_data(dep)
	A = d.get_data(ind)
	z1 = np.ones((d.get_num_rows(), 1))
	A = np.hstack((A, z1))
	print A
  # assign to AAinv the result of calling numpy.linalg.inv( np.dot(A.T, A))
  #	   The matrix A.T * A is the covariance matrix of the independent
  #	   data, and we will use it for computing the standard error of the 
  #	   linear regression fit below.
	AAinv = np.linalg.inv( np.dot(A.T, A))

  # assign to x the result of calling numpy.linalg.lstsq( A, y )
  #	   This solves the equation y = Ab, where A is a matrix of the 
  #	   independent data, b is the set of unknowns as a column vector, 
  #	   and y is the dependent column of data.  The return value x 
  #	   contains the solution for b.
	x = np.linalg.lstsq( A, y )

  # assign to b the first element of x.
  #	   This is the solution that provides the best fit regression
  # assign to N the number of data points (rows in y)
  # assign to C the number of coefficients (rows in b)
  # assign to df_e the value N-C, 
  #	   This is the number of degrees of freedom of the error
  # assign to df_r the value C-1
  #	   This is the number of degrees of freedom of the model fit
  #	   It means if you have C-1 of the values of b you can find the last one.
	b = x[0]
	N = y.shape[0]
	C = b.shape[0]
	df_e = N-C
	df_r = C-1

  # assign to error, the error of the model prediction.	 Do this by 
  #	   taking the difference between the value to be predicted and
  #	   the prediction. These are the vertical differences between the
  #	   regression line and the data.
  #	   y - numpy.dot(A, b)
	error = y-np.dot(A, b)

  # assign to sse, the sum squared error, which is the sum of the
  #	   squares of the errors computed in the prior step, divided by the
  #	   number of degrees of freedom of the error.  The result is a 1x1 matrix.
  #	   numpy.dot(error.T, error) / df_e
	sse = np.dot(error.T, error)/ df_e

  # assign to stderr, the standard error, which is the square root
  #	   of the diagonals of the sum-squared error multiplied by the
  #	   inverse covariance matrix of the data. This will be a Cx1 vector.
  #	   numpy.sqrt( numpy.diagonal( sse[0, 0] * AAinv ) )
	stderr = np.sqrt(np.diagonal( sse[0,0] * AAinv) )

  # assign to t, the t-statistic for each independent variable by dividing 
  #	   each coefficient of the fit by the standard error.
  #	   t = b.T / stderr
	t = b.T / stderr

  # assign to p, the probability of the coefficient indicating a
  #	   random relationship (slope = 0). To do this we use the 
  #	   cumulative distribution function of the student-t distribution.	
  #	   Multiply by 2 to get the 2-sided tail.
  #	   2*(1 - scipy.stats.t.cdf(abs(t), df_e))
	p = 2*(1 - sc.t.cdf(abs(t), df_e))

  # assign to r2, the r^2 coefficient indicating the quality of the fit.
  #	   1 - error.var() / y.var()
	r2 = 1 - error.var() / y.var()

  # Return the values of the fit (b), the sum-squared error, the
  #		R^2 fit quality, the t-statistic, and the probability of a
  #		random relationship.
	return b, sse, r2, t, p

#======Project 5, Extension 2==========
#help from Theo S.
def runMultiLR(d, ind, dep):
	print ind, dep
	b, sse, r2, t, p = linear_regression(d, ind, dep)
	print "b:", b
	print "sse:", sse
	print "r2:", r2
	print "t:", t
	print "p:", p
	values.append(b)
	values.append(sse)
	values.append(r2)
	values.append(t)
	values.append(p)
	return b, sse, r2, t, p
	
#======Lab 6, Task 2==========
# This version uses SVD
# help from B.Doyle
def pca(d, headers, normalize=True):
	# assign to A the desired data. Use either normalize_columns_separately
	#	or get_data, depending on the value of the normalize argument.
	if normalize:
		A = normalize_columns_separately(headers, d)
	else:
		A = d.get_data(headers)


	# assign to m the mean values of the columns of A
	m= np.mean(A, axis=0)[0]
	m= np.array(m)
	M= m*np.ones(A.shape)

	# assign to D the difference matrix A - m
	D = A-M

	# assign to U, S, V the result of running np.svd on D, with full_matrices=False
	U, S, V = np.linalg.svd(D, full_matrices=False)

	# the eigenvalues of cov(A) are the squares of the singular values (S matrix)
	#	divided by the degrees of freedom (N-1). The values are sorted.
	N= d.get_num_rows()
	eValues= (S*S)/(N-1)


	# project the data onto the eigenvectors. Treat V as a transformation
	#	matrix and right-multiply it by D transpose. The eigenvectors of A
	#	are the rows of V. The eigenvectors match the order of the eigenvalues.
	pData= np.dot(V, D.T).T

	# create and return a PCA data object with the headers, projected data,
	# eigenvectors, eigenvalues, and mean vector.
	pca_data= PCAData.PCAData(headers, pData, V, eValues, m)
	return pca_data
	
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~PROJECT 7~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#============LAB 7 Work=================

# Add a function to your analysis module that uses Numpy's built-in k-means capabilities.
# It should take as arguments a data set, the headers to use for clustering, and the number of clusters to create.
# It will return the cluster means, the cluster ID of each point, and the representation error.
# import scipy.cluster.vq as vq
# Write the following kmeans_numpy function.
def kmeans_numpy( d, headers, K, whiten = True):
    # '''Takes in a Data object, a set of headers, and the number of clusters to create
    # Computes and returns the codebook, codes, and representation error.
    # '''

    # assign to A the result of getting the data from your Data object
    A = d.get_data(headers)

    # assign to W the result of calling vq.whiten on A
    W= vq.whiten(A)

    # assign to codebook, bookerror the result of calling vq.kmeans with W and K
    codebook, bookerror = vq.kmeans(W, K)

    # assign to codes, error the result of calling vq.vq with W and the codebook
    codes, error = vq.vq(W,codebook)

    # return codebook, codes, and error
    return codebook, codes, error


# To make the above function easier, write two helper functions: kmeans_init and kmeans_classify.

# The kmeans_init should take in the data, the number of clusters K, and an optional set of categories
# (cluster labels for each data point) and return a numpy matrix with K rows, each one repesenting a cluster mean.
# If no categories are given, a simple way to select the means is to randomly choose K data points (rows of the data matrix)
# to be the first K cluster means.If you are given an Nx1 matrix of categories/labels, then compute the mean values of
# each category and return those as the initial set of means. You can assume the categories are zero-indexed and range from 0 to K-1.
def kmeans_init(d, K, categories= " "):
	if categories != " ":
		print categories
		cats, labels = np.unique( np.asarray( categories.T ), return_inverse = True)
		means = np.matrix(np.zeros((len(cats), d.shape[1])))
		for i in range(len(cats)):
			means[i,:] = np.mean( d[labels==i, :], axis=0)
	else:
		means = np.matrix(np.zeros((K, d[0].size), dtype = np.float))
		maxes = np.matrix(d.max(0))
		mins = np.matrix(d.min(0))
		for i in range(d[0].size):
			for j in range(K):
				means[j, i] = random.uniform(mins[0,i],maxes[0,i])
	return means

#  The kmeans_classify should take in the data and cluster means and return a list or matrix (your choice) of ID values
#  and distances. The IDs should be the index of the closest cluster mean to the data point. The default distance
#  metric should be sum-squared distance to the nearest cluster mean.
def kmeans_classify(data, means):
    idxs = np.matrix(np.zeros((data.T[0].size, 1), dtype = np.int))
    dist = np.matrix(np.zeros((data.T[0].size, 1), dtype = np.float))
    for i in range(data.T[0].size):
        tempdists = []
        pt = data[i]
        for j in range(means.T[0].size):
            m = means[j]
            tempdists.append(np.linalg.norm(m-pt))
        inOrder = copy.copy(tempdists)
        inOrder.sort()
        dist[i,0] = inOrder[0]
        idxs[i,0] = tempdists.index(inOrder[0])
    return (idxs, dist)


def kmeans_algorithm(A, means):
    # set up some useful constants
    MIN_CHANGE = 1e-7
    MAX_ITERATIONS = 100
    D = means.shape[1]
    K = means.shape[0]
    N = A.shape[0]

    # iterate no more than MAX_ITERATIONS
    for i in range(MAX_ITERATIONS):
        # calculate the codes
        codes, errors = kmeans_classify( A, means )

        # calculate the new means
        newmeans = np.zeros_like( means )
        counts = np.zeros( (K, 1) )
        for j in range(N):
            newmeans[codes[j,0],:] += A[j,:]
            counts[codes[j,0],0] += 1.0

        # finish calculating the means, taking into account possible zero counts
        for j in range(K):
            if counts[j,0] > 0.0:
                newmeans[j,:] /= counts[j, 0]
            else:
                newmeans[j,:] = A[random.randint(0,A.shape[0]),:]

        # test if the change is small enough
        diff = np.sum(np.square(means - newmeans))
        means = newmeans
        if diff < MIN_CHANGE:
            break

    # call classify with the final means
    codes, errors = kmeans_classify( A, means )

    # return the means, codes, and errors
    return (means, codes, errors)

# Takes in a Data object, a set of headers, and the number of clusters to create
# Computes and returns the codebook, codes and representation errors.
# If given an Nx1 matrix of categories, it uses the category labels
#  to calculate the initial cluster means.
def kmeans(d, headers, K, whiten=True, categories = ' '):

    # assign to A the result getting the data given the headers
    # if whiten is True
    if whiten:
      # assign to W the result of calling vq.whiten on the data--> Normalized
        A= d.get_data(headers)
        W= vq.whiten(A)
    # else
    else:
      # assign to W the matrix A--> unnormalized
        A = d.get_data(headers)
        W = A


    # assign to codebook the result of calling kmeans_init with W, K, and categories
    codebook = kmeans_init(W, K, categories)


    # assign to codebook, codes, errors, the result of calling kmeans_algorithm with W and codebook
    codebook, codes, errors = kmeans_algorithm(W, codebook)

    # return the codebook, codes, and representation error
    return codebook, codes, errors

#======Project 5, Task 4===========
#Test Function
if __name__=="__main__":
	d = Data('data-clean.csv')
	b, sse, r2, t, p = linear_regression(d, ['X0', 'X1'], 'Y')
	print "b:", b
	print "sse:", sse
	print "r2:", r2
	print "t:", t
	print "p:", p
	
	
