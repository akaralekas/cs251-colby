# CS 251
# Spring 2015
#------------------------------------

# File: analysis.py
# Author/Editor: Anthony Karalekas
# Collaboration: S.Parrott, J.Saul
# Help: Bruce, Theo S.
# Date: Mar. 15, 2016
# Assignment: Project 5

#------------------------------------

# Edited by Tony Karalekas
# CS251 Spring 2015
# Project 5

import Tkinter as tk
import tkFont as tkf
import math
import random
import numpy as np
from data import *
import scipy.stats as sc

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
	
	
