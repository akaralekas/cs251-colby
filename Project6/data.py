# CS 251
# Spring 2015
#------------------------------------

# File: data.py
# Author/Editor: Anthony Karalekas
# Collaboration: J.Saul, B.Doyle, S.Parrott
# Help: CP Majgaard
# Date: Apr. 3, 2016
# Assignment: Project 6

#------------------------------------

# Edited by Tony Karalekas
# CS251 Spring 2015
# Project 5

import Tkinter as tk
import tkFont as tkf
import math
import random
import csv
import numpy as np

#first line of our data file will be headers
#second line of our data file will be types
#everything else will be data

# integer -9999 is a convention used to show there is missing data

# allowing # to comment in data files is very nice

# Lab to read in Raw_Data

# create a class to build and manage the data
class Data:

	def __init__(self, filename = None):
		
		#create and init fields and variables
		self.raw_headers = [] #(list of all headers)
		self.raw_types = [] #(list of all types)
		self.raw_data = [] #list of lists of all data. Each row is a list of strings)
		self.header2raw = {} #(dictionary mapping header string to index of column in raw data)
		
		#Project2 Task1
		self.matrix_data = np.matrix([]) # matrix of numeric data
		self.header2matrix = {} # dictionary mapping header string to index of column in matrix data
		
		if filename != None:
			self.read(filename)
		
	def read(self, filename):
		fp = file(filename, 'rU')
		cread = csv.reader(fp)
		
		self.raw_headers = cread.next() #returns the next row as a list of strings.
		self.raw_types = cread.next()
		self.raw_data = []

		for row in cread:
			self.raw_data.append(row)
			#print row
		
		
		#Project2 Task1
		# worked with Julia Saul, help from Bruce & CP
		convert_data = []
		num_col = 0
		self.header2matrix = {}
		
		for i in range(len( self.raw_data)):
			rowList=[]
			for j in range(len(self.raw_headers)):
				if self.raw_types[j] == "numeric":
					rowList.append(float(self.raw_data[i][j]))	
				#second dictionary that maps headers to corresponding columns
				#advice from Bruce to reduce amount of code
				#assign this within the for loop to create new numeric indices
			convert_data.append(rowList)
		num_col = 0
		i = 0
		for types in self.raw_types:
			if types == "numeric":
				self.header2matrix[self.raw_headers[i]] = num_col
				num_col += 1
			i +=1
		#the matrix of the numeric data		
		self.matrix_data = np.matrix(convert_data)
		
		self.header2raw = {}
		for i in range(len(self.raw_headers)):
			#key = headers
			#value = index
			self.header2raw[self.raw_headers[i]] = i
		
	#Lab 2, Task 3
	#Accessor Methods
	def get_raw_headers(self): 
		#returns a list of all of the headers.
		return self.raw_headers
		
	def get_raw_type(self): 
		#returns a list of all of the types.
		return self.raw_types
		
	def get_raw_num_columns(self): 
		#returns the number of columns in the raw data set
		return len(self.raw_headers)
		
	def get_num_rows(self): 
		#returns the number of rows in the data set. 
		#this should be identical to the number of rows in the numeric data, 
		#so you can get away with writing just one function for this purpose.
		return len(self.raw_data)
		
	def get_raw_row(self, row): 
		#returns a row of data (the type is list) given a row index (int).
		return self.raw_data[row]
		
	def get_raw_value(self, row, header):
		#takes a row index (an int) and column header (a string) 
		#and returns the raw data at that location. (The return type will be a string)
		return self.raw_data[row][self.header2raw[header]]
	
	#(list of headers of columns with numeric data)
	def get_headers(self):
		headers = []
		for i in range(len(self.raw_headers)):
			if self.raw_types[i] == 'numeric':
				headers.append(self.raw_headers[i])
		return headers
				
	#returns the number of columns of numeric data
	def get_num_columns(self): 
		numcols = 0
		for i in range(len(self.raw_headers)):
			if self.raw_types[i] == 'numeric':
				numcols += 1
		return numcols
				
	#take a row index and returns a row of numeric data
	def get_row(self, row_ind):
		return self.matrix_data[row_ind]
	
	#takes a row index (int) and column header (string) and returns the data in the numeric matrix.
	def get_value(self, row, header):
		return self.matrix_data[row][header]
		
	#At a minimum, this should take a list of columns headers and 
	#return a matrix with the data for all rows but just the specified columns. 
	#It is optional to also allow the caller to specify a specific set of rows.
	##help from bruce and julia saul
	def get_data(self, col_headers):
		mx = []
		num = 0
		for item in col_headers:
			index = self.header2matrix[item]
			
			for i in range(len(self.raw_data)):
			
				if i == 0:
					mx.append([self.matrix_data[i, index]])
				else:
					mx[num].append(self.matrix_data[i, index])
			num += 1
		return np.matrix(mx).T	
		
	def printAll(self):
		for i in range(len(self.raw_data)):
			print self.raw_data[i]
	
			
	def testingMethods(self):
		d = Data("testdata1.csv")
		print "Getting headers:"
		print d.get_headers()
		print "Getting the number of columns:"
		print d.get_num_columns()
		print "Getting a row:"
		print d.get_row(2)
		print "Getting a value:"
		print "Getting data:"
	
	def testingAnalysis(self):
		d = Data("testdata1.csv")
		print "Data range:"
		print data_range(['thing2' , 'thing3'], self)
		print "Find mean:"
		print mean(['thing2' , 'thing3'], self)
		print "Find standard deviation:"
		print stdev(['thing2' , 'thing3'], self)
		print "Normalizing columns seperately:"
		print normalize_columns_separately(['thing2' , 'thing3'], self)
		print "Normalizing columns together:"
		print normalize_columns_together(['thing2' , 'thing3'], self)
		
		
if __name__=="__main__":
	d = Data("testdata1.csv")
	d.testingMethods()
	d.testingAnalysis()
	

	
		
		
		
		
		
		