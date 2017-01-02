# CS 251
# Spring 2015
#------------------------------------

# File: analysis.py
# Author/Editor: Anthony Karalekas
# Collaboration: B.Doyle, S.Parrott
# Date: Mar. 6, 2016
# Assignment: Project 4

#------------------------------------

# Edited by Tony Karalekas
# CS251 Spring 2015
# Project 2 

import Tkinter as tk
import tkFont as tkf
import math
import random
import numpy as np
from data import *


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
	
	mins =  mx.min(axis = 0)
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
	
if __name__=="__main__":
	d = Data("MLBPitching.csv")
	
	print "Here is our Data Matrix:"
	print(d.matrix_data)
	
	print "Data range:"
	print(data_range(['W','L', 'ERA'], d))
	
	print "Mean:"
	print(mean(['W','L', 'ERA'], d))
	
	print "Standard Deviation:"
	print(stdev(['W','L', 'ERA'], d))

	print "Normalize Column Separatley:"
	print(normalize_columns_separately(['W','L', 'ERA'], d))
	
	print "Normalize Column Together:"
	print(normalize_columns_together(['W','L', 'ERA'], d))
	
	print "Sum:"
	print(sum(['W','L', 'ERA'], d))
	
	print "Round:"
	print(round(['W','L', 'ERA'], d))
	
