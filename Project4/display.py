# Skeleton Tk interface example
# Written by Bruce Maxwell
# Modified by Stephanie Taylor
#
# CS 251
# Spring 2015
#------------------------------------

# File: display.py
# Author/Editor: Anthony Karalekas
# Help: S.Parrott, Jay Moore
# Date: Mar. 6, 2016
# Assignment: Project 4

#------------------------------------

# Edited by Tony Karalekas
# Feb. 28, 2016
# CS251 Spring 2015
# Project 3 

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
		
		self.buildAxes()
		self.updateAxes()
				
		
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
		menu.add_cascade( label = "Command", menu = cmdmenu )
		menulist.append(cmdmenu)

		# menu text for the elements
		# the first sublist is the set of items for the file menu
		# the second sublist is the set of items for the option menu
		## Task 1, Project 1
	#~~~~~~~~~~~~Project3, Extension 3~~~~~~~~~~~~~~
	#EXTENSION3(P3), Reset Menu Command
		menutext = [ [ 'Open \xE2\x8C\x98-O', 'Reset \xE2\x8C\x98-R', 'Clear \xE2\x8C\x98-N', 'Quit \xE2\x8C\x98-Q' ],
					 [ 'Command 1', '-', '-' ] ]

		# menu callback functions (note that some are left blank,
		# so that you can add functions there if you want).
		# the first sublist is the set of callback functions for the file menu
		# the second sublist is the set of callback functions for the option menu
	#EXTENSION3(P3), continued...
		menucmd = [ [self.handleOpen, self.resetAxes, self.clearData, self.handleQuit],
					[self.handleMenuCmd1, None, None] ]
		
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

#---------Lab4 work-----------------#Lab4, Task4
	# def handleChooseAxes(self, event=None):
#		print "choosing axes"
#		d = data.Data()
#		headers = []
#		for i in range(len(d.get_headers())):
#			headers.append(i)
#		return headers
	
	#Project 1, Task 1
	def clearData(self, event=None):
		print 'Clearing Data'
		for i in self.objects:
			self.canvas.delete(i)
		#makes the points an empty list after deleting points
		self.objects = []
		
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
		 


#========================================================================================
#======================OLD CODE FROM PROJECT 1============================================
# 
# Task 2, Project 1 
# def handleMouseButton3(self, event):
#		self.baseClick = (event.x, event.y)
#		print 'handle mouse button 3: %d %d' % (event.x, event.y)
#		
#		dx = 3
#		rgb = "#%02x%02x%02x" % (random.randint(0, 255), 
#							 random.randint(0, 255), 
#							 random.randint(0, 255) )
#		oval = self.canvas.create_oval( event.x - dx,
#									event.y - dx, 
#									event.x + dx, 
#									event.y + dx,
#									fill = rgb,
#									outline='')
#									
#		self.objects.append( oval )
#
#
#
#This is called if the first mouse button is being moved
# def handleMouseButton1Motion(self, event):
#		# calculate the difference
#		diff = ( event.x - self.baseClick[0], event.y - self.baseClick[1] )
#		## Task 2, Project 1
#		for obj in self.objects:
#			loc = self.canvas.coords(obj)
#			self.canvas.coords( obj, 
#						loc[0] + diff[0], 
#						loc[1] + diff[1], 
#						loc[2] + diff[0],
#						loc[3] + diff[1] )
# 
#		# update base click
#		self.baseClick = ( event.x, event.y )
#		print 'handle button1 motion %d %d' % (diff[0], diff[1])
#========================================================================================
#========================================================================================



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


## Task 3, Project 1
# Received help from cs251 classmate JSaul
class ListDialog(Dialog):

	def body(self, master):
		
		self.xLabel = tk.Label(master, text ="X				Y				Z")
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

		self.xLabel.pack(side=tk.TOP)
		self.box1.pack(side=tk.LEFT)
		self.box2.pack(side=tk.LEFT)
		self.box3.pack(side=tk.LEFT)
		
	def apply(self):
		self.result = [map(int,self.box1.curselection()),map(int,self.box2.curselection()),map(int,self.box3.curselection())]
		pass #override

if __name__ == "__main__":
	dapp = DisplayApp(1200, 675)
	dapp.main()
