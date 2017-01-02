# Skeleton Tk interface example
# Written by Bruce Maxwell
# Modified by Stephanie Taylor
#
# CS 251
# Spring 2015
#------------------------------------

# File: display.py
# Author/Editor: Anthony Karalekas
# Help: B.Doyle, S.Parrott, CP
# Date: Feb. 28, 2016
# Assignment: Project 3

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
		menutext = [ [ '-', 'Clear	\xE2\x8C\x98-N', 'Quit	\xE2\x8C\x98-Q' ],
					 [ 'Command 1', '-', '-' ] ]

		# menu callback functions (note that some are left blank,
		# so that you can add functions there if you want).
		# the first sublist is the set of callback functions for the file menu
		# the second sublist is the set of callback functions for the option menu
		menucmd = [ [None, self.clearData, self.handleQuit],
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

		return


	def setBindings(self):
		# bind mouse motions to the canvas
		self.canvas.bind( '<Button-1>', self.handleMouseButton1 )
		self.canvas.bind( '<Control-Button-1>', self.handleMouseButton2 )
		self.canvas.bind( '<Button-2>', self.handleMouseButton2 )
		self.canvas.bind( '<B1-Motion>', self.handleMouseButton1Motion )
		self.canvas.bind( '<B2-Motion>', self.handleMouseButton2Motion )
		self.canvas.bind( '<Control-B1-Motion>', self.handleMouseButton2Motion )
		self.canvas.bind( '<Button-2>', self.handleMouseButton3 )

		# bind command sequences to the root window
		self.root.bind( '<Command-q>', self.handleQuit )
		self.root.bind( '<Command-n>', self.clearData )

	def handleQuit(self, event=None):
		print 'Terminating'
		self.root.destroy()
		
	#Project 1, Task 1
	def clearData(self, event=None):
		print 'Clearing Data'
		self.canvas.delete('all')

	def handleButton1(self):
		for obj in self.objects:
			self.canvas.itemconfig(obj, fill=self.colorOption.get() )
		print 'handling command button:', self.colorOption.get()

	def handleMenuCmd1(self):
		print 'handling menu command 1'

	def handleMouseButton1(self, event):
		print 'handle mouse button 1: %d %d' % (event.x, event.y)
		self.baseClick = (event.x, event.y)

	def handleMouseButton2(self, event):
		self.baseClick = (event.x, event.y)
		print 'handle mouse button 2: %d %d' % (event.x, event.y)
	
	## Task 2, Project 1	
	def handleMouseButton3(self, event):
		self.baseClick = (event.x, event.y)
		print 'handle mouse button 3: %d %d' % (event.x, event.y)
		
		dx = 3
		rgb = "#%02x%02x%02x" % (random.randint(0, 255), 
							 random.randint(0, 255), 
							 random.randint(0, 255) )
		oval = self.canvas.create_oval( event.x - dx,
									event.y - dx, 
									event.x + dx, 
									event.y + dx,
									fill = rgb,
									outline='')
									
		self.objects.append( oval )

	# This is called if the first mouse button is being moved
	def handleMouseButton1Motion(self, event):
		# calculate the difference
		diff = ( event.x - self.baseClick[0], event.y - self.baseClick[1] )
		## Task 2, Project 1
		for obj in self.objects:
			loc = self.canvas.coords(obj)
			self.canvas.coords( obj, 
						loc[0] + diff[0], 
						loc[1] + diff[1], 
						loc[2] + diff[0],
						loc[3] + diff[1] )

		# update base click
		self.baseClick = ( event.x, event.y )
		print 'handle button1 motion %d %d' % (diff[0], diff[1])

			
	# This is called if the second button of a real mouse has been pressed
	# and the mouse is moving. Or if the control key is held down while
	# a person moves their finger on the track pad.
	def handleMouseButton2Motion(self, event):
		print 'handle button 2 motion'

#------------------------------#Project3, Task1
	#task1.d
	def buildAxes(self):
		vtm = self.view.build()
		pts = (vtm * self.axesEndpoints.T).T
	
		#-----add axes to list-------
		self.axes.append(self.canvas.create_lines(pt[0,0], pt[0,1], pt[1,0], pt[1,1], fill = 'blue', dash=(4,4)))
		self.axes.append(self.canvas.create_lines(pt[2,0], pt[2,1], pt[3,0], pt[3,1], fill = 'red', dash=(4,4)))
		self.axes.append(self.canvas.create_lines(pt[4,0], pt[4,1], pt[5,0], pt[5,1], fill = 'green', dash=(4,4)))
		
		
	#task1.e
	def updateAxes(self):
		vtm = self.view.build()
		pts = (vtm * self.axesEndpoints.T).T
		
		#-----
		self.canvas.coords(self.axes[0], pt[0,0], pt[0,1], pt[1,0], pt[1,1])
		self.canvas.coords(self.axes[1], pt[2,0], pt[2,1], pt[3,0], pt[3,1])
		self.canvas.coords(self.axes[2], pt[4,0], pt[4,1], pt[5,0], pt[5,1])

	
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
		
			# Extension 3 continued...
			# replace dx and dy with sizeOption to adjust size of data
			dx = int(self.sizeOption.get())
			dy = int(self.sizeOption.get())
			
			## EXTENSION 2
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
		
		#Extension 2 continued...
		self.box3 = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		self.box3.insert(tk.END, "Oval")
		self.box3.insert(tk.END, "Sqaure")
		self.box3.insert(tk.END, "Arc Shape")
		
		self.box1.pack(side=tk.TOP)
		self.box2.pack(side=tk.TOP)
		self.box3.pack(side=tk.TOP)
		
	def apply(self):
		self.result = [map(int,self.box1.curselection()),map(int,self.box2.curselection()),map(int,self.box3.curselection())]
		pass #override

if __name__ == "__main__":
	dapp = DisplayApp(1200, 675)
	dapp.main()
