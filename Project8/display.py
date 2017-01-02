# Skeleton Tk interface example
# Written by Bruce Maxwell
# Modified by Stephanie Taylor
#
# CS 251
# Spring 2015
#------------------------------------

# File: display.py
# Author/Editor: Anthony Karalekas
# Collaboration: S.Parrott, J.Saul, B. Doyle
# Worked alongside S.Parrot throughout 
# Help: CP Majgaard
# Date: Apr. 24, 2016
# Assignment: Project 8

#------------------------------------

# Edited by Tony Karalekas
# Apr. 3, 2016
# CS251 Spring 2016
# Project 6

#imports
import Tkinter as tk
import tkFont as tkf
import math
import random
import view as v
import numpy as np
import tkFileDialog as tkFD
import data
import analysis
import scipy.stats as sc
import matplotlib.pyplot
import copy


# create a class to build and manage the display
class DisplayApp:

	def __init__(self, width, height):

		# create a tk object, which is the root window
		self.root = tk.Tk()

		# width and height of the window
		self.initDx = width
		self.initDy = height

		# set up the geometry for the window
		self.root.geometry( "%dx%d+50+30" % (self.initDx, self.initDy) )

		# set the title of the window
		self.root.title("Tony's Data Dots")

		# set the maximum size of the window for resizing
		self.root.maxsize( 1600, 900 )

		# setup the menus
		self.buildMenus()
		
		self.xaxisLegend = None
		self.yaxisLegend = None
		self.zaxisLegend = None
		self.colorLegend = None
		self.sizeLegend = None
		self.shapeLegend = None
		
		#=======Project 5, Extension 2======
		#legends of values to be put on canvas
		self.bLegend = None
		self.sseLegend = None
		self.r2Legend = None
		self.tLegend = None
		self.pLegend = None

		# build the controls
		self.buildControls()

		# build the Canvas
		self.buildCanvas()

		# bring the window to the front
		self.root.lift()

		# - do idle events here to get actual canvas size
		self.root.update_idletasks()

		# now we can ask the size of the canvas
		print self.canvas.winfo_geometry()

		# set up the key bindings
		self.setBindings()

		# set up the application state
		self.objects = [] # list of data objects that will be drawn in the canvas
		self.data = None # will hold the raw data someday.
		self.baseClick = None # used to keep track of mouse movement
		
		self.baseExtent = None

				
#------------------------------------#Project3, Task1		
		#task1.a
		self.view = v.View()
		
		#task1.b
		self.axesEndpoints = np.matrix( [[0, 0, 0, 1], #x_origin
										 [1, 0, 0, 1], #x_endpoint
										 [0, 0, 0, 1], #y_origin
										 [0, 1, 0, 1], #y_endpoint
										 [0, 0, 0, 1], #z_origin
										 [0, 0, 1, 1]] ) #z_endpoint
		#task1.c
		self.axes = []
		
		#~~~~~~~~~~~~~~~~Project 4, Task 3~~~~~~~~~~~~~~~
		self.headers = []
		
		#stores the data points while they are being updated in updatePoints
		#created in buildPoints to convert data to matrix
		self.data2matrix = None
		
		#=======Lab 5, Task 8========
		#graphical objects associated with a linear regression
		self.regLine = None
		self.lineLabel = None
		#=======Lab 5, Task 2========
		self.LRobjects = []
		self.LRendpoints = None
		
		self.buildAxes()
		self.updateAxes()
		
		self.pcaList = []
		self.clusterCount = 0
		self.colors = ["#ACFFCC","#FD1F74","#20FF57","#5F60E0","#BBF14E",
						"#C64288","#73B302","#F98DD9","#BACC0F","#A4B9FE","#1CA03A","#FE6340",
						"#27F1CF","#AD5407","#93CBF6","#578616","#E8CAFD","#87F898","#FA726D",
						"#42E39C","#ED8798","#11885D","#F2B656","#4F73A4","#EAFDD4","#A05551",
						"#CAD5F6","#47899A","#FBF2E6","#96749C"]
				
		
	def buildMenus(self):
		
		# create a new menu
		menu = tk.Menu(self.root)

		# set the root menu to our new menu
		self.root.config(menu = menu)

		# create a variable to hold the individual menus
		menulist = []

		# create a file menu
		filemenu = tk.Menu( menu )
		menu.add_cascade( label = "File", menu = filemenu )
		menulist.append(filemenu)

		# create another menu for kicks
		cmdmenu = tk.Menu( menu )
		menu.add_cascade( label = "Analysis", menu = cmdmenu )
		menulist.append(cmdmenu)

		# menu text for the elements
		# the first sublist is the set of items for the file menu
		# the second sublist is the set of items for the option menu
		## Task 1, Project 1
	#~~~~~~~~~~~~Project3, Extension 3~~~~~~~~~~~~~~
	#EXTENSION3(P3), Reset Menu Command
		menutext = [ [ 'Open \xE2\x8C\x98-O', 'Reset \xE2\x8C\x98-R', 'Clear \xE2\x8C\x98-N', 'Quit \xE2\x8C\x98-Q' ],
					 [ 'Linear Regression', 'Save Reg Analysis', 'Multiple LR', 'PCA Analysis', 'Clustering Analysis', 'Fix Color' ] ]

		# menu callback functions (note that some are left blank,
		# so that you can add functions there if you want).
		# the first sublist is the set of callback functions for the file menu
		# the second sublist is the set of callback functions for the option menu
	#EXTENSION3(P3), continued...
		menucmd = [ [self.handleOpen, self.resetAxes, self.clearData, self.handleQuit],
					[self.handleLinearRegression, self.saveAnalysis, self.handleMultipleLinearRegression, self.handlePCA, self.handleCluster, self.colorFix] ]
		
		# build the menu elements and callbacks
		for i in range( len( menulist ) ):
			for j in range( len( menutext[i]) ):
				if menutext[i][j] != '-':
					menulist[i].add_command( label = menutext[i][j], command=menucmd[i][j] )
				else:
					menulist[i].add_separator()

	# create the canvas object
	def buildCanvas(self):
		self.canvas = tk.Canvas( self.root, width=self.initDx, height=self.initDy )
		self.canvas.pack( expand=tk.YES, fill=tk.BOTH )
		return

	# build a frame and put controls in it
	def buildControls(self):

		### Control ###
		# make a control frame on the right
		rightcntlframe = tk.Frame(self.root)
		rightcntlframe.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.Y)

		# make a separator frame
		sep = tk.Frame( self.root, height=self.initDy, width=2, bd=1, relief=tk.SUNKEN )
		sep.pack( side=tk.RIGHT, padx = 2, pady = 2, fill=tk.Y)

		# use a label to set the size of the right panel
		label = tk.Label( rightcntlframe, text="Control Panel", width=20 )
		label.pack( side=tk.TOP, pady=10 )

		# make a menubutton
		self.colorOption = tk.StringVar( self.root )
		self.colorOption.set("black")
		colorMenu = tk.OptionMenu( rightcntlframe, self.colorOption, 
										"black", "blue", "red", "green" ) # can add a command to the menu
		colorMenu.pack(side=tk.TOP)

		
		# EXTENSION 1(project 1)
		# make a new menubutton for numberOption
		# this dropdown menu allows you to control how many dots there are
		self.numOption = tk.StringVar( self.root )
		self.numOption.set("200")
		numMenu = tk.OptionMenu( rightcntlframe, self.numOption, 
										"200", "150", "100", "50", "25", "10" ) # can add a command to the menu
		numMenu.pack(side=tk.TOP)		# EXTENSION 1
		
		
		# EXTENSION 3(project 1)
		# make a new menubutton for sizeOption
		# this dropdown menu allows you to chose the size of the data dot
		self.sizeOption = tk.StringVar( self.root )
		self.sizeOption.set("3")
		sizeMenu = tk.OptionMenu( rightcntlframe, self.sizeOption, 
										"12", "10", "7", "5", "3" ) # can add a command to the menu
		sizeMenu.pack(side=tk.TOP)
		
		# make a button in the frame
		# and tell it to call the handleButton method when it is pressed.
		# Color Button
		button1 = tk.Button( rightcntlframe, text="Update Color", 
							   command=self.handleButton1 )
		button1.pack(side=tk.TOP)  # default side is top
		
		# Lab 1, Task 3b
		# Make button for Data Points
		button2 = tk.Button( rightcntlframe, text="Create Points", 
							   command=self.createRandomDataPoints )
		button2.pack(side=tk.TOP)  # default side is top
		
		#--------Lab4, Task3---------
		button3 = tk.Button( rightcntlframe, text="Plot Data", 
							   command=self.handleChooseAxes )
		button3.pack(side=tk.TOP)  # default side is top
		
		#======Project 6, Task 1========
		
		#label for PCA Box
		PCAlabel = tk.Label( rightcntlframe, text = "PCA Analysis:" , width=20 )
		PCAlabel.pack( side=tk.TOP, pady=1 )
		
		#PCA analysis box
		self.pcaBox = tk.Listbox( rightcntlframe, selectmode = tk.BROWSE )
		self.pcaBox.pack(side=tk.TOP, pady=5)
		
		#Buttons for analysis functions
		#plotting button
		plotPCA = tk.Button( rightcntlframe, text = "Plot PCA", 
									command = self.handlePCAPlot)
		plotPCA.pack(side=tk.TOP, pady=0)
	
		#display button
		displayPCA = tk.Button( rightcntlframe, text = "Display Info", 
									command = self.handlePCAinfo)
		displayPCA.pack(side=tk.TOP, pady=0)
		
		#delete button
		deletePCA = tk.Button( rightcntlframe, text = "Delete PCA", 
									command = self.handlePCAdelete)
		deletePCA.pack(side=tk.TOP, pady=0)
		
#---------Project 4, Extension 3---------
		#EXTENSIONN3
		text = tk.StringVar()
		leg = tk.Label( rightcntlframe, textvariable = text, width=20 )
		leg.pack( side=tk.TOP, pady=10 )
		text.set("Legend:")
		
		#Creates a legend for the X-axis
		self.xaxisLegend = tk.StringVar()
		leg = tk.Label( rightcntlframe, textvariable = self.xaxisLegend, width=20 )
		leg.pack( side=tk.TOP, pady=10 )
		self.xaxisLegend.set("Have not chosen X-axis")
		
		#Creates a legend for the Y-axis
		self.yaxisLegend = tk.StringVar()
		leg = tk.Label( rightcntlframe, textvariable = self.yaxisLegend, width=20 )
		leg.pack( side=tk.TOP, pady=10 )
		self.yaxisLegend.set("Have not chosen Y-axis")
		
		#Creates a legend for the Z-axis
		self.zaxisLegend = tk.StringVar()
		leg = tk.Label( rightcntlframe, textvariable = self.zaxisLegend, width=20 )
		leg.pack( side=tk.TOP, pady=10 )
		self.zaxisLegend.set("Have not chosen Z-axis")
		
		#Creates a legend for the color
		self.colorLegend = tk.StringVar()
		leg = tk.Label( rightcntlframe, textvariable = self.colorLegend, width=20 )
		leg.pack( side=tk.TOP, pady=10 )
		self.colorLegend.set("Have not chosen Color")
		
		#Creates a legend for the size
		self.sizeLegend = tk.StringVar()
		leg = tk.Label( rightcntlframe, textvariable = self.sizeLegend, width=20 )
		leg.pack( side=tk.TOP, pady=10 )
		self.sizeLegend.set("Have not chosen Size")
		
		#Creates a legend for the shape
		self.shapeLegend = tk.StringVar()
		leg = tk.Label( rightcntlframe, textvariable = self.shapeLegend, width=20 )
		leg.pack( side=tk.TOP, pady=10 )
		self.shapeLegend.set("Have not chosen Size")
		
		
		return


	def setBindings(self):
		# bind mouse motions to the canvas
		self.canvas.bind( '<Button-1>', self.handleMouseButton1 )
		self.canvas.bind( '<B1-Motion>', self.handleMouseButton1Motion )
		
		self.canvas.bind( '<Button-2>', self.handleMouseButton2 )
		self.canvas.bind( '<Control-Button-1>', self.handleMouseButton2 )
		self.canvas.bind( '<Control-B1-Motion>', self.handleMouseButton2Motion )
		self.canvas.bind( '<B2-Motion>', self.handleMouseButton2Motion )
		
		self.canvas.bind( '<Button-3>', self.handleMouseButton3 )
		self.canvas.bind( '<Shift-Button-1>', self.handleMouseButton3 )
		self.canvas.bind( '<Shift-B1-Motion>', self.handleMouseButton3Motion )
		self.canvas.bind( '<B3-Motion>', self.handleMouseButton3Motion )
		
		# bind command sequences to the root window
		self.root.bind( '<Command-q>', self.handleQuit )
		self.root.bind( '<Command-n>', self.clearData )
		self.root.bind( '<Command-o>', self.handleOpen )
		self.root.bind( '<Command-r>', self.resetAxes )
	
#~~~~~~~~~~~~Project3, Extension 3~~~~~~~~~~~~~~~
	#EXTENSION3(P3), Reset Button
	def resetAxes(self, event=None):
		print "Resetting Axes"
		self.view.reset()
		self.updateAxes()

	def handleQuit(self, event=None):
		print 'Terminating'
		self.root.destroy()

#---------Lab4 work-----------------#Lab4, Task2			
	def handleOpen(self, event=None):
		print "Opening File"
		fn = tkFD.askopenfilename( parent=self.root, 
										title= 'Filename', initialdir='.' )
		self.data = data.Data()
		self.data.read(fn)
		#~~~~~~~~~~~~~~~~Project 4, Task 2~~~~~~~~~~~~~~~~~
		#Task 2 -- Same functions that handleChooseAxes does
		self.headers = self.data.get_headers()


	#---------Lab4 work-----------------#Lab4 Task3
	#~~~~~~~~~~~~~~~~Project 4, Task 2~~~~~~~~~~~~~~~~~~~~
	def handleChooseAxes(self, event = None):
		print "Handling Plot Data"
		#~~~~~~Project 4, Extension 2~~~~~~~~~
		#Extension 2 - Functionality
		#If no file is read in yet, it will ask user to select a file to be read
		if len(self.headers) == 0:
			print "Please Select A File First"
			self.handleOpen()
		print "List of headers: {}".format(self.headers)
		CA = AxesLabels(self.root, self.headers)
		self.buildPoints(CA.result, CA.resultC[0], CA.resultS[0], CA.resultSP[0])
		
	#Project 1, Task 1
	def clearData(self, event=None):
		print 'Clearing Data'
		for i in self.objects:
			self.canvas.delete(i)
		#makes the points an empty list after deleting points
		self.objects = []
		#===Project 5, Task 1+2 continue==
		#clears the reg line and label when you clear
		for j in self.LRobjects:
			self.canvas.delete(j)
		self.bLegend.config(text = "")
		self.sseLegend.config(text = "")
		self.tLegend.config(text = "")
		self.pLegend.config(text = "")
		self.r2Legend.config(text = "")
		self.LRobjects = []
		
	#~~~~~~~~~~~~Project4, Extension 4~~~~~~~~~~~~~~~~~~~~~
	#I added this to BOTH delete the points/clear the canvas AND reset the axes
	def totalReset(self, event=None):
		print 'Totally Resetting'
		for i in self.objects:
			self.canvas.delete(i)
		self.resetAxes()
		self.objects = []

	def handleButton1(self):
		for obj in self.objects:
			self.canvas.itemconfig(obj, fill=self.colorOption.get() )
		print 'handling command button:', self.colorOption.get()

	def handleMenuCmd1(self):
		print 'handling menu command 1'

	def handleMouseButton1(self, event):
		print 'handle mouse button 1: %d %d' % (event.x, event.y)
		self.baseClick = (event.x, event.y)

#-------------------------------------#Project3, Task2
	#called if the first button of a real mouse is pressed and the mouse is moving
	#----Process for Panning (notes from Class w/Stephanie)
	#task2.a
	def handleMouseButton1Motion(self,event):
		
		#calculate the difference
		dx = float(event.x - self.baseClick[0])
		dy = float(event.y - self.baseClick[1])
		
		# dx = dx / self.canvas.winfo_width()
		dx = dx / self.view.screen[0,0]
		dy = dy / self.view.screen[0,1]
		dx = dx * self.view.extent[0,0]
		dy = dy * self.view.extent[0,1]
	
		delta0 = dx
		delta1 = dy 
	
		self.view.vrp = self.view.vrp + delta0*self.view.u + delta1*self.view.vup
	
		self.updateAxes()
	
		self.baseClick = ( event.x, event.y)
	
#-------------------------------------#Project3, Task2		
	#task2.d
	def handleMouseButton2(self, event):
		self.baseClick2 = (event.x, event.y)
		self.cloneView = self.view.clone()
		print 'handle mouse button 2: %d %d' % (event.x, event.y)
	
	#called if the second button of mouse has been pressed and the mouse is moving.
	def handleMouseButton2Motion(self, event):
		diff = ( event.x - self.baseClick2[0], event.y - self.baseClick2[1])
		
		delta0 = (-diff[0])/(1.0*self.canvas.winfo_height())*math.pi
		delta1 = (diff[1])/(1.0*self.canvas.winfo_width())*math.pi
		
		degx = delta0*(180/math.pi)
		degy = delta1*(180/math.pi)
		
		self.view = self.cloneView.clone()
		self.view.rotateVRC(delta0, delta1)
		self.updateAxes()
		
		
#------------------------------------#Project3, Task2
	#called if the third button of a real mouse is pressed
	#----Process for Scaling (notes from Class w/Stephanie)
	#task2.b
	def handleMouseButton3(self, event):
		self.baseClick = (event.x, event.y)
		self.baseExtent = self.view.extent.copy() #help from Theo S
		#print 'hwllo'
		#help from Stephanie during office hours
	
	def handleMouseButton3Motion(self, event):
		#print "got here"
		dy = event.y - self.baseClick[1]
		k = 1.0 / self.canvas.winfo_height()
		print k
		f = 1.0 + k * dy
		f = max( min(f, 3.0), 0.1)
		self.view.extent = self.baseExtent * f
		self.updateAxes()
		

	#======Lab 5, Task 4=========
	def handleLinearRegression(self, event = None):
		if len(self.headers) == 0:
			print "Please Select A File First"
			self.handleOpen()
		#Prompt User for Variables
		lr = LinearRegression(self.root, self.headers)
		#Clear Existing Points From Window and Resets Canvas
		self.totalReset()
		#Clear Any Existing Data Fits
		self.LRobjects = []
		#Update Axes
		self.updateAxes()
		#Call Build LR
		self.buildLinearRegression(lr.result[0], lr.result[1])
	
	#======Lab 5, Task 5=========
	def buildLinearRegression(self, independent, dependent):
		dx = 5
		dy = 5

		#task5.1
		#Extract Results and Assign them to Variables
		xvar = independent
		yvar = dependent
		#normalize columns separately
		a = analysis.normalize_columns_separately([xvar], self.data)
		b = analysis.normalize_columns_separately([yvar], self.data)
		c = np.hstack((a, b))

		#task5.2
		#add a third column of zeros to the matrix
		z1 = np.zeros((self.data.get_num_rows(), 1))
		d = np.hstack((c, z1))

		#task5.3
		#add a fourth column of zeros to the matrix
		z2 = np.ones((self.data.get_num_rows(), 1))
		self.data2matrix = np.hstack((d, z2))

		#task5.4
		#build the VTM
		vtm = self.view.build()
		#multiply it by data points
		tp = (vtm*self.data2matrix.T).T

		#build points
		for i in range(tp.shape[0]):
			tx = tp[i, 0]
			ty = tp[i, 1]

			pt = self.canvas.create_oval(tx - dx, ty - dy, tx + dx, ty + dy,
												 fill="black", outline='')
			self.objects.append(pt)

		#task5.5
		#calculate linear regression
		xy = self.data.get_data([xvar,yvar])
		#yu = self.data.get_data([yvar])
		###help from Theo S.
		slope, intercept, r_value, p_value, r2 = sc.linregress(xy)
		print slope, intercept, r2
		
		#task5.6
		#get range
		xrange = analysis.data_range([xvar], self.data)
		yrange = analysis.data_range([yvar], self.data)
		
		#task5.7
		#make endpoints
		value1 = ((xrange[0][0] * slope + intercept) - yrange[0][0]) / (yrange[0][1] - yrange[0][0])
		value2 = ((xrange[0][1] * slope + intercept) - yrange[0][0]) / (yrange[0][1] - yrange[0][0])
		print "hi"
		self.LRendpoints = np.matrix([ [0, value1, 0, 1],
										[1, value2, 0, 1] ])
										
		#task5.8
		#multiply the line endpoints by the vtm, 
		#then make tk obj out of endpoints
		points = (vtm * self.LRendpoints.T).T		
		self.regLine = self.canvas.create_line(points[0,0], points[0,1], points[1,0], points[1,1], fill= "Red", width = 3)
		self.LRobjects.append(self.regLine)
		
		#task5.9
		self.lineLabel = tk.Label(self.canvas, text = "Linear Regression:" + str(slope))
		self.lineLabel.place(x=points[1,0], y=points[1,1])
#---------------------------------------------------------------
	#==========Project 5, Task 1==========
	def updateFits(self):
		if self.LRendpoints == None:
			return
		else:
			# build the VTM
			vtm = self.view.build()
			# multiply the axis endpoints by the VTM
			pts = (vtm * self.LRendpoints.T).T
			self.canvas.coords(self.regLine, pts[0,0], pts[0,1], pts[1,0], pts[1,1])
			self.lineLabel.place(x=pts[1,0], y=pts[1,1])
			
#*	#==========Project 5, Extension 2==========
	def handleMultipleLinearRegression(self, event = None):
		if len(self.headers) == 0:
			print "Please Select A File First"
			self.handleOpen()
		#Prompt User for Variables
		mlr = MultipleLinearRegression(self.root, self.headers)
		#Clear Existing Points From Window and Resets Canvas
		self.totalReset()
		#Clear Any Existing Data Fits
		self.LRobjects = []
		#Update Axes
		self.updateAxes()
		
		independent, dependent = mlr.result
		#Call Build LR
		analysis.runMultiLR(self.data, independent, dependent)
		
		self.bLegend = tk.Label(self.canvas, text = "B Value:" + str(analysis.values[0]))
		self.bLegend.place(x=400, y= 50)
		
		self.sseLegend = tk.Label(self.canvas, text = "SSE Value:" + str(analysis.values[1]))
		self.sseLegend.place(x=400, y= 100)
		
		self.r2Legend = tk.Label(self.canvas, text = "R2 Value:" + str(analysis.values[2]))
		self.r2Legend.place(x=400, y= 125)
		
		self.tLegend = tk.Label(self.canvas, text = "T Value:" + str(analysis.values[3]))
		self.tLegend.place(x=400, y= 150)
		
		self.pLegend = tk.Label(self.canvas, text = "P Value:" + str(analysis.values[4]))
		self.pLegend.place(x=400, y= 175)
		
		return 
			
#*	#=======Project 5, Extension 1=============
	#save analysis as .txt file
	def saveAnalysis(self):
		txt_file = open("analysis_results.txt", "w")		
		txt_file.write("RESULTS: B, SSE, R2, T, P," "\n")
		for item in analysis.values:
			txt_file.write("%s\n" % item + "\n") 
	
#------------------------------#Project3, Task1
	#received some help from classmate Theo S.
	#task1.d
	def buildAxes(self):
		vtm = self.view.build()
		pts = (vtm * self.axesEndpoints.T).T
		#-----add axes to list-------
	#~~~~~~~~~~~~Project3, Extension 1~~~~~~~~~~~~~~~~~~~~~
		#EXTENSION1(P3), Colored and Dashed Axes Lines
		self.axes.append(self.canvas.create_line(pts[0,0], pts[0,1], pts[1,0], pts[1,1], fill = 'blue', dash=(4,4)))
		self.axes.append(self.canvas.create_line(pts[2,0], pts[2,1], pts[3,0], pts[3,1], fill = 'red', dash=(4,4)))
		self.axes.append(self.canvas.create_line(pts[4,0], pts[4,1], pts[5,0], pts[5,1], fill = 'green', dash=(4,4)))
		
	#~~~~~~~~~~~~Project3, Extension 2~~~~~~~~~~~~~~~~~~~~~
		#EXTENSION2(P3), Axes Labels
		self.xLabel = tk.Label(self.canvas, text = "X")
		self.xLabel.place(x=pts[1,0], y=pts[1,1])
		
		self.yLabel = tk.Label(self.canvas, text = "Y")
		self.yLabel.place(x=pts[3,0], y=pts[3,1])
		
		self.zLabel = tk.Label(self.canvas, text = "Z")
		self.zLabel.place(x=pts[5,0], y=pts[5,1])
		
		
	#task1.e
	def updateAxes(self):
		vtm = self.view.build()
		pts = (vtm * self.axesEndpoints.T).T
		print pts
		#------update the axes with for new vtm------
		self.canvas.coords(self.axes[0], pts[0,0], pts[0,1], pts[1,0], pts[1,1])
		self.canvas.coords(self.axes[1], pts[2,0], pts[2,1], pts[3,0], pts[3,1])
		self.canvas.coords(self.axes[2], pts[4,0], pts[4,1], pts[5,0], pts[5,1])
		
		#EXTENSION2(P3) Continued...
		self.xLabel.place(x=pts[1,0], y=pts[1,1])
		self.yLabel.place(x=pts[3,0], y=pts[3,1])
		self.zLabel.place(x=pts[5,0], y=pts[5,1])
	
		#Project 4, Task 1
		#easier to call this inside of updateAxes rather than every time in code
		self.updatePoints()
		self.updateFits()
	
	#~~~~~~~~~~~~Project4, Task 1~~~~~~~~~~~~~~~~~~~~~
	def updatePoints(self, event = None):
		if len(self.objects) == 0:
			return
		
		vtm = self.view.build()
		pts = (vtm*self.data2matrix.T).T
		#help from Jay Moore
		for i, point in enumerate(self.objects):
			dx = pts[i,0]
			dy = pts[i,1]
			self.canvas.coords(point, dx-5, dy-5, dx+5, dy+5)
		self.updateFits()
	
	
	#-----------Lab4, Task 5(Lab)-----------------
	#Builds the point we want to graph from a list of selected headers
	#help from Steven Parrott and Jay Moore
	def buildPoints(self, headers, color, size, shapes, event=None):
		selected_headers = headers
		
		if selected_headers[0] == None:
			print "Please Select an X Plot"
			return
		if selected_headers[1] == None:
			print "Please Select a Y Plot"
			return
		if selected_headers[2] == None:
			print "Please Select a Z Plot"
			return
		if color[0] == None:
			print "Please Select a Color"
			return
		if size[0] == None:
			print "Please Select a Size"
			return
		if shapes[0] == None:
			print "Please Select a Shape"
			return

		self.totalReset()
	

		temp = []
		dx = int(size)
		dy = int(size)
		a = analysis.normalize_columns_separately(selected_headers, self.data)

		for i in range(a.shape[0]):
			x = a[i, 0]
			y = a[i, 1]

			if len(selected_headers) == 2:
				z = 0
				self.xaxisLegend.set("X-axis:" + selected_headers[0])
				self.yaxisLegend.set("Y-axis:" + selected_headers[1])
				
			elif len:
				z = a[i, 2]
				self.xaxisLegend.set("X-axis:" + selected_headers[0])
				self.yaxisLegend.set("Y-axis:" + selected_headers[1])
				self.zaxisLegend.set("Z-axis:" + selected_headers[2])
				self.colorLegend.set("Color:" + color)
				self.sizeLegend.set("Size:" + size)
				self.shapeLegend.set("Shape:" + shapes)

			temp.append([x, y, z, 1])
		#Make VTM
		vtm = self.view.build()
		#Convert Data to Matrix
		self.data2matrix = np.matrix(temp)

		print shapes

		tp = (vtm*self.data2matrix.T).T

		for i in range(tp.shape[0]):
			tx = tp[i, 0]
			ty = tp[i, 1]
			tz = tp[i, 2]

			#Extension 1 Continued...
			if shapes == "oval":
				pt = self.canvas.create_oval(tx - dx, ty - dy, tx + dx, ty + dy,
												 fill=color, outline='')
				self.objects.append(pt)
			if shapes == "rectangle":
				pt = self.canvas.create_rectangle(tx - dx, ty - dy, tx + dx, ty + dy,
												 fill=color, outline='')
				self.objects.append(pt)
			if shapes == "arc":
				pt = self.canvas.create_arc(tx - dx, ty - dy, tx + dx, ty + dy,
												 fill=color, outline='')
				self.objects.append(pt)
		return
#==============================
	#project 1
	# Lab 1, Task 3
	# Method that will add data points to the display
	# Task 3, Project 1
	## received helped from cs251 classmate Julia Saul
	def createRandomDataPoints( self, event=None ):
		dialog = ListDialog(self.root)
		if dialog.result == None:
			return
		if dialog.result[0][0] == None:
			return
		if dialog.result[1][0] == None:
			return
			
		for i in range(int(self.numOption.get())):
			if dialog.result[0][0] == 0:
				x = random.randrange(0,self.canvas.winfo_width())
			else:
				x = random.gauss(self.canvas.winfo_width()/6,self.canvas.winfo_width()/10)
				
			if dialog.result[1][0] == 0:
				y = random.randrange(0,self.canvas.winfo_height())
			else:
				y = random.gauss(self.canvas.winfo_width()/6,self.canvas.winfo_width()/10)
		
			# Extension 3, Project 1 continued...
			# replace dx and dy with sizeOption to adjust size of data
			dx = int(self.sizeOption.get())
			dy = int(self.sizeOption.get())
			
			## EXTENSION 2, Project 1
			# this gives the user the option to choose the shape of the data point
			# you can choose a oval, square, or arc shape
			if dialog.result[2][0] == 0:
				pt = self.canvas.create_oval( x-dx, y-dx, x+dx, y+dx,
									fill=self.colorOption.get(), outline='' )
				self.objects.append(pt)
			elif dialog.result[2][0] == 1: 
				pt = self.canvas.create_rectangle( x-dx, y-dx, x+dx, y+dx,
									fill=self.colorOption.get(), outline='' )
				self.objects.append(pt)
			else:
				pt = self.canvas.create_arc( x-dx, y-dx, x+dx, y+dx,
									fill=self.colorOption.get(), outline='' )
				self.objects.append(pt)
		
#---------------------PROJECT 6-----------------------------------
	#TASK ONE Continued
	#HELP FROM CP MAJAGAARD!!

	#Adds points from file chosen in init
	def buildPCA(self, headers, data):
		self.totalReset()

		points = analysis.normalize_columns_separately(headers[0:3], data)
		
		if len(data.get_data_headers()) > 3:
			self.size = analysis.normalize_columns_separately([headers[3]], data)
			
		if len(data.get_data_headers()) > 4:
			self.color = analysis.normalize_columns_together([headers[4]], data)
			
		vtm = self.view.build()
		#make a matrix of only ones
		self.data2matrix = np.ones((points.shape[0], 4))

		if len(data.get_data_headers()) < 3:
			self.data2matrix[:,:-2] = points
			self.data2matrix[:,-2] = np.zeros((points.shape[0]))
		else:
			self.data2matrix[:,:-1] = points
			
		tend = self.data2matrix * vtm.T
		
		dx = int(self.sizeOption.get())
		dy = int(self.sizeOption.get())
		
		for i in range(tend.shape[0]):
			tx = tend[i, 0]
			ty = tend[i, 1]
			tz = tend[i, 2]

			pt = self.canvas.create_oval(tx - dx, ty - dy, tx + dx, ty + dy,
												 fill='black', outline='')
			self.objects.append(pt)
			
		#self.updatePoints()
		#self.updateAxes()
	
	#Project 6, Task 1
	#help from CP
	def handlePCA(self):
		if self.data == None:
			self.handleOpen()
		else:
			col = PCAColDialog(self.root, self.data.get_headers())
			if len(col.result) > 0:
				name = PCANameDialog(self.root)
				if name.result != None:
					headers = []
					headersNumeric = self.data.get_headers()
					for i in col.result[0]:
						headers.append(headersNumeric[i])
					self.pcaList.append(analysis.pca(self.data, headers, normalize=col.result[1]))
					self.pcaBox.insert(tk.END, name.result)
						
					
	#handlePCAPlot method
	def handlePCAPlot(self):
		if len(self.pcaList) > 0:
			idx = self.pcaBox.index(tk.ACTIVE)
			self.buildPCA(self.pcaList[idx].get_data_headers(), self.pcaList[idx])
	
	#handlePCAdelete method		
	def handlePCAdelete(self):
		idx = self.pcaBox.index(tk.ACTIVE)
		self.pcaBox.delete(idx)
		if len(self.pcaList) > 0:
			del self.pcaList[idx]
	
	#help from CP Majgaard
	#look for PCA object user selected, grab the index of what is active
	#then, create list of vectors and values and return 2D list of vecs and vals
	#now, create another list of raw headers(p0, p1, p2) and then copy of get_data_HEADERS!
	#then, in headers, insert eval and evec to the front of the list
	#give array a list of headers and the call the zip method of list to create tuple list
	#end up with a list of formatted strings!
	#then spawn eigen dialog and add the array!
		#python tricks from CP help [zip method]
		#zip method takes list and concatenates list entry-wise to list of tuples
	def handlePCAinfo(self):
		if len(self.pcaList) > 0:
			idx = self.pcaBox.index(tk.ACTIVE)
			vecs = self.pcaList[idx].get_eigenvectors().tolist()
			vals = self.pcaList[idx].get_eigenvalues().tolist()
			rawHeaders = self.pcaList[idx].get_raw_headers()
			headers = copy.copy(self.pcaList[idx].get_data_headers())
			headers.insert(0, "E-Val")
			headers.insert(0, "E-Vec")
			pca_array = []
			pca_array.append(headers)
			#python tricks from CP help [zip method]
			#zip method takes list and concatenates list entry-wise to list of tuples
			for rawHeader, eval, evec in zip(rawHeaders, vals, vecs):
				evec.insert(0, eval)
				evec.insert(0, rawHeader)
				pca_array.append(evec)
			e = EigenDialog(self.root, pca_array)
		
		
#---------------------PROJECT 7-----------------------------------
	#HELP FROM CP MAJAGAARD!!
	def handleCluster(self):
		d = ClusterDialog(self.root, self.data.get_headers())
		if d.result != None and int(d.clusters) > 0:
			headers = []
			for index in d.result:
				headers.append(self.data.get_headers()[index])
			codebook, codes, errors = analysis.kmeans(self.data, headers, int(d.clusters))
			self.clusterCount += 1
			self.data.addColumn("Clusters %d" % (self.clusterCount,), codes)
			self.headers = self.data.get_headers()
	
	#HELP FROM BRUCE!!	
	def colorFix(self):
	#figure out a way to specify a column to base the color of off
		colorColumn = self.data.get_data( ['NB Classification'] )
		# if the data in colorColumn has less than 30 unique values
		unique = np.unique(np.asarray(colorColumn))
		unique = unique.tolist()
		if len(unique) <= 30:
			# for each visual object that has been plotted
			for i, point in enumerate(self.objects):
				# color index is unique.index( colorColumn[i,0] )
				colorIdx = unique.index(colorColumn[i,0])
				# set the color to the color string at that index 
				self.canvas.itemconfigure(point, fill=str(self.colors[colorIdx]))

	def main(self):
		print 'Entering main loop'
		self.root.mainloop()
		
## Task 3a, Project 1
# Copied this code from effbot to create Dialog class
class Dialog(tk.Toplevel):

	def __init__(self, parent, title = None):

		tk.Toplevel.__init__(self, parent)
		self.transient(parent)

		if title:
			self.title(title)

		self.parent = parent

		self.result = None
		
		#~~~~~~~~~~~~~~~~Project 4~~~~~~~~~~~~~~~
		#Task 4
		self.resultC = None
		self.resultS = None
		#Extension 1 continued... adding shape options
		self.resultSP = None

		body = tk.Frame(self)
		self.initial_focus = self.body(body)
		body.pack(padx=5, pady=5)

		self.buttonbox()

		self.grab_set()

		if not self.initial_focus:
			self.initial_focus = self

		self.protocol("WM_DELETE_WINDOW", self.cancel)

		self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
								  parent.winfo_rooty()+50))

		self.initial_focus.focus_set()

		self.wait_window(self)

	# construction hooks

	def body(self, master):
		# create dialog body.  return widget that should have
		# initial focus.  this method should be overridden

		pass

	def buttonbox(self):
		# add standard button box. override if you don't want the
		# standard buttons

		box = tk.Frame(self)

		w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
		w.pack(side=tk.LEFT, padx=5, pady=5)
		w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
		w.pack(side=tk.LEFT, padx=5, pady=5)

		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)

		box.pack()

	#
	# standard button semantics

	def ok(self, event=None):

		if not self.validate():
			self.initial_focus.focus_set() # put focus back
			return

		self.withdraw()
		self.update_idletasks()

		self.apply()

		self.cancel()

	def cancel(self, event=None):

		# put focus back to the parent window
		self.parent.focus_set()
		self.destroy()

	# command hooks

	def validate(self):

		return 1 # override

	def apply(self):

		pass # override
		
#~~~~~~~~~~~~~~~~Project 4, Task 2~~~~~~~~~~~~~~~
#Lab 4 - Task 3
#worked with Steve Parrott
class AxesLabels(Dialog):

	def __init__(self, parent, headers):
		self.colors = ["red", "blue", "gray", "green", "yellow", "orange"]
		self.size = ["10", "7", "5", "3"]
		self.shapes = ["oval", "rectangle", "arc"]
		self.headers = headers
		Dialog.__init__(self, parent, "Choose Axes")
		
	def body(self, master):
		
		self.xBox = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		for i in range(len(self.headers)):
			self.xBox.insert(tk.END, self.headers[i])

		self.yBox = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		for j in range(len(self.headers)):
			self.yBox.insert(tk.END, self.headers[j])

		self.zBox = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		for k in range(len(self.headers)):
			self.zBox.insert(tk.END, self.headers[k])

		#box for colors
		self.cBox = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		for l in range(len(self.colors)):
			self.cBox.insert(tk.END, self.colors[l])

		#box for sizes
		self.sBox = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		for m in range(len(self.size)):
			self.sBox.insert(tk.END, self.size[m])

		#~~~~~~~~~~~~Project 4, Extension 1~~~~~~~~~~~~~~~
		#Extension 1 - Shapes
		#box for shapes
		self.spBox = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		for n in range(len(self.shapes)):
			self.spBox.insert(tk.END, self.shapes[n])

		#labels
		tk.Label(master, text = "X-axis").grid(row = 1, column = 1)
		tk.Label(master, text = "Y-axis").grid(row = 1, column = 2)
		tk.Label(master, text = "Z-axis").grid(row = 1, column = 3)
		tk.Label(master, text = "Color").grid(row = 1, column = 4)
		tk.Label(master, text = "Size").grid(row = 1, column = 5)
		tk.Label(master, text = "Shape").grid(row = 1, column = 6)
		
		#pack all the boxes to screen
		self.xBox.grid(row = 2, column = 1)
		self.yBox.grid(row = 2, column = 2)
		self.zBox.grid(row = 2, column = 3)
		self.cBox.grid(row = 2, column = 4)
		self.sBox.grid(row = 2, column = 5)
		self.spBox.grid(row = 2, column = 6)

	#apply all these boxes and rules
	def apply(self):
		self.result = []
		self.resultC = ["gray11"]
		self.resultS = ["10"]
		self.resultSP = ["oval"]
		self.result.append(self.headers[self.xBox.curselection()[0]])
		self.result.append(self.headers[self.yBox.curselection()[0]])
		if len(self.zBox.curselection()) > 0:
			self.result.append(self.headers[self.zBox.curselection()[0]])
		if len(self.cBox.curselection()) > 0:
			self.resultC[0] = (self.colors[self.cBox.curselection()[0]])
		if len(self.sBox.curselection()) > 0:
			self.resultS[0] = (self.size[self.sBox.curselection()[0]])
		if len(self.spBox.curselection()) > 0:
			self.resultSP[0] = (self.shapes[self.spBox.curselection()[0]])

		pass#override

#======Lab 5, Task 4===============
# create a new dialog box for linear regression
class LinearRegression(Dialog):

	def __init__(self, parent, headers):
		self.headers = headers
		Dialog.__init__(self, parent, "Linear Regression")

	def body(self, master):
		self.xBox = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		for i in range(len(self.headers)):
			self.xBox.insert(tk.END, self.headers[i])

		self.yBox = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		for j in range(len(self.headers)):
			self.yBox.insert(tk.END, self.headers[j])

		tk.Label(master, text = "X-axis").grid(row = 1, column = 1)
		tk.Label(master, text = "Y-axis").grid(row = 1, column = 2)
	   
		self.xBox.grid(row = 2, column = 1)
		self.yBox.grid(row = 2, column = 2)


	def apply(self):
		#self.result = [map(int, self.xBox.curselection()), map(int, self.yBox.curselection()), map(int,
		#																							 self.sBox.curselection())]
		self.result = []
		self.result.append(self.headers[self.xBox.curselection()[0]])
		self.result.append(self.headers[self.yBox.curselection()[0]])

		pass  # override

#======Project 5, Extension 2=============
# create a new dialog box for multiple linear regression
class MultipleLinearRegression(Dialog):

	def __init__(self, parent, headers):
		self.headers = headers
		Dialog.__init__(self, parent, "MultipleLinear Regression")

	def body(self, master):
		self.xBox = tk.Listbox(master, selectmode=tk.MULTIPLE, exportselection=0)
		for i in range(len(self.headers)):
			self.xBox.insert(tk.END, self.headers[i])

		self.yBox = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		for j in range(len(self.headers)):
			self.yBox.insert(tk.END, self.headers[j])

		tk.Label(master, text = "Independent").grid(row = 1, column = 1)
		tk.Label(master, text = "Dependent").grid(row = 1, column = 2)
	   
		self.xBox.grid(row = 2, column = 1)
		self.yBox.grid(row = 2, column = 2)


	def apply(self):
		#self.result = [map(int, self.xBox.curselection()), map(int, self.yBox.curselection()), map(int,
		#																							 self.sBox.curselection())]
		self.independent = []
		self.dependent = []
		self.independent.append(self.headers[self.xBox.curselection()[0]])
		self.independent.append(self.headers[self.xBox.curselection()[1]])
		self.dependent.append(self.headers[self.yBox.curselection()[0]])
		self.result = (self.independent, self.dependent)
		pass  # override


## Task 3, Project 1
# Received help from cs251 classmate JSaul
class ListDialog(Dialog):

	def body(self, master):
		self.box1 = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		self.box1.insert(tk.END, "Uniform")
		self.box1.insert(tk.END, "Gaussian")

		self.box2 = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		self.box2.insert(tk.END, "Uniform")
		self.box2.insert(tk.END, "Gaussian")

		self.box3 = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		self.box3.insert(tk.END, "Oval")
		self.box3.insert(tk.END, "Rectangle")
		self.box3.insert(tk.END, "Arc")
				
		self.box1.grid(row = 2, column = 1)
		self.box2.grid(row = 2, column = 2)
		self.box3.grid(row = 2, column = 3)
		
	def apply(self):
		self.result = [map(int,self.box1.curselection()),map(int,self.box2.curselection()),map(int,self.box3.curselection())]
		pass #override


#======Project 6, Task 3=============
# create a new dialog box Eigen Information
class EigenDialog(Dialog):
	def __init__(self, parent, pca_array, title = "Eigen Info:"):
		self.pca_array = pca_array
		Dialog.__init__(self, parent, title = title)
	#help from CP
	def body(self, master):
		for idx, i in enumerate(self.pca_array):
			for idx2, j in enumerate(i):
				if type(j) is float:
					e = tk.Label(master, text = "%.4f" % j)
				else:
					e = tk.Label(master, text = j)
				e.grid(row=idx, column=idx2, sticky=tk.NSEW)
				
#column selection dialog box
#help from CP
class PCAColDialog(Dialog):
	def __init__(self, parent, headers, title = "Choose Columns:"):
		self.headers = headers
		Dialog.__init__(self, parent, title = title)
	
	def body(self, master):
		col = tk.Label(master, text = "Choose Columns:")
		col.pack()
		
		self.colBox = tk.Listbox(master, selectmode=tk.EXTENDED)
		self.colBox.pack()
		
		for i in self.headers:
			self.colBox.insert(tk.END, i)
		self.var = tk.StringVar()
		
		check = tk.Checkbutton(master, text="Normalize", variable=self.var,
							onvalue="True", offvalue="False")
		check.pack()
		check.select()

	def validate(self):
		self.result = (self.colBox.curselection(), self.var.get())
		if len(self.result) > 0:
			return 1
		else:
			return 0
			
#name dialog box
#help from CP
class PCANameDialog(Dialog):
	def body(self, master):
		w = tk.Label(master, text="Name:")
		w.pack()
		
		self.name = tk.Entry(master)
		self.name.pack()
		string = "PCA"
		self.name.insert(0, string)

	def validate(self):
		self.result = self.name.get()
		if self.result != "":
			return 1
		else:
			return 0
			
		
#-----------------PROJECT 7 Boxes-----------------------------
class ClusterDialog(Dialog):
	def __init__(self, parent, headers, title = "Choose Columns:"):
		self.headers = headers
		Dialog.__init__(self, parent, title = title)
	
	def body(self, master):
		col = tk.Label(master, text = "Choose Columns:")
		col.pack()
		
		self.colBox = tk.Listbox(master, selectmode=tk.EXTENDED)
		self.colBox.pack()
		
		for i in self.headers:
			self.colBox.insert(tk.END, i)
		
		w = tk.Label(master, text="Number of Clusters")
		w.pack()
		
		self.clusterBox = tk.Entry(master)
		self.clusterBox.pack()
		
	def validate(self):
		self.result = list(self.colBox.curselection())
		self.clusters = self.clusterBox.get()
		if len(self.result) > 0:
			return 1
		else:
			return 0

if __name__ == "__main__":
	dapp = DisplayApp(1200, 675)
	dapp.main()
