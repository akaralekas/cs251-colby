# CS 251
# Spring 2016
#--------------------------------------

# File: view.py
# Author/Editor: Anthony Karalekas
# Collaboration: S.Parrott
# Help: CP Majgaard
# Date: Apr. 24, 2016
# Assignment: Project 8

#--------------------------------------

# Edited by Tony Karalekas
# CS251 Spring 2016
# Lab 5

#~~~~imports~~~~~
import Tkinter as tk
import tkFont as tkf
import math
import random
import csv
import numpy as np
import copy

#-----lab notes------
#create 3 line segments in data space
#(0,0,0) = origin
#(0,1,0) = y
#(1,0,0) = x
#(0,0,1) = z

#be able to manipulate the line segments in space
#length of the line segments is dependent upon the orientation of the view

#T(tx, ty, tz) = translation matrix size 4x4 with tx,ty,tz, 1 in last column
#S(sx, sy, sz) = matrix with the scale factors along the diagonal 

#===============================================================================

#View class that holds the current viewing parameters 
#and can build a view transformation matrix [VTM] based on the parameters.
class View:

	def __init__(self):
		#Lab3, Task1
		# ====init fields=====
		
		#simply call reset function in constructor to init values
		self.reset()
		
	#function that initializes everything/all values
	#these are my init_fields, but this can be used to reset during project 
	def reset(self):
		#a NumPy matrix with the default value [0.5, 0.5, 1].
		self.vrp = np.matrix([0.5, 0.5, 1])
		#a NumPy matrix with the default value [0, 0, -1].
		self.vpn = np.matrix([0, 0, -1])
		#a NumPy matrix with the default value [0, 1, 0].
		self.vup = np.matrix([0, 1, 0])
		#a NumPy matrix with the default value [-1, 0, 0].
		self.u = np.matrix([-1, 0, 0])
		#a list or NumPy matrix with the default value [1, 1, 1]
		self.extent = np.matrix([1, 1, 1])
		#a list or NumPy matrix with the default value [400, 400]
		self.screen = np.matrix([400,400])
		#a list or NumPy matrix with the default value [20, 20]
		self.offset = np.matrix([20,20])

	#a simple normalize function, a normalized vector has unit length
	#Lab3, Task2.4	
	def normalize(self, vector):
		Vx = vector[0,0]
		Vy = vector[0,1]
		Vz = vector[0,2]
		length = math.sqrt( Vx*Vx + Vy*Vy + Vz*Vz )
		
		return vector / length
		
	#Lab3, Task2
	#uses the current viewing parameters to return a view matrix
	def build(self):
		#4x4 identity matrix, basis for the view matrix
		#VIEW TRANSLATION MATRIX
		vtm = np.identity( 4, float )
		
		#translation1 matrix to move the VRP to the origin
		t1 = np.matrix( [[1, 0, 0, -self.vrp[0, 0]],
							[0, 1, 0, -self.vrp[0, 1]],
							[0, 0, 1, -self.vrp[0, 2]],
							[0, 0, 0, 1] ] )
		#then premultiply the vtm by the translation matrix
		vtm = t1 * vtm
		
		#-----------------------------task2.3
		#now calculate the view reference axes tu, tvup, and tvpn
		#1) tu is the cross product (np.cross) of the vup and vpn vectors.
		tu = np.cross(self.vup, self.vpn)
		#2)tvup is the cross product of the vpn and tu vectors.
		tvup = np.cross(self.vpn, tu)
		#3)tvpn is a copy of the vpn vector.
		tvpn = self.vpn
		
		#------------------------------task2.4
		#now normalize the three view reference axes
		tu_norm = self.normalize(tu)
		tvup_norm = self.normalize(tvup)
		tvpn_norm = self.normalize(tvpn)
		
		#------------------------------task2.5
		#copy the orthonormal axes tu, tvup, and tvpn back to self.u, self.vup and self.vpn
		self.u = tu_norm
		self.vup = tvup_norm
		self.vpn = tvpn_norm
		
		#------------------------------task2.6
		#generate the rotation matrix to align the view reference axes 
		# align the axes
		r1 = np.matrix( [[ self.u[0, 0], self.u[0, 1], self.u[0, 2], 0.0 ],
							[ self.vup[0, 0], self.vup[0, 1], self.vup[0, 2], 0.0 ],
							[ self.vpn[0, 0], self.vpn[0, 1], self.vpn[0, 2], 0.0 ],
							[ 0.0, 0.0, 0.0, 1.0 ] ] )
		#then premultiply M(vtm) by the rotation
		vtm = r1 * vtm
		
		#------------------------------task2.7
		#translate the lower left corner of the view space to the origin
		#this is just a translation by half the extent of the view volume in the X & Y view axes
		#new translation2 matrix
		t2 = np.matrix( [[1, 0, 0, 0.5*self.extent[0,0]],
						[0, 1, 0, 0.5*self.extent[0,1]],
						[0, 0, 1, 0],
						[0, 0, 0, 1]] )
		
		#vtm = T( 0.5*extent[0], 0.5*extent[1], 0 ) * vtm				
		#then premultiply vtm by the translation t2				
		vtm = t2 * vtm
		
		#------------------------------task2.8
		#Use the extent and screen size values to scale to the screen.
		#new scalar1 matrix
		s1 = np.matrix( [[(-self.screen[0,0] / self.extent[0,0]), 0, 0, 0],
						[0, (-self.screen[0,1] / self.extent[0,1]), 0, 0],
						[0, 0, (1.0 / self.extent[0,2]), 0],
						[0, 0, 0, 1] ] )
						
		#vtm = S( -screen[0] / extent[0], -screen[1] / extent[1], 1.0 / extent[2] ) * vtm				
		#then premultiply vtm by the scalar s1				
		vtm = s1 * vtm
		
		#------------------------------task2.9
		#translate the lower left corner to the origin and add the view offset
		#gives a little buffer around the top and left edges of the window
		#new translation3 matrix
		t3 = np.matrix( [[1, 0, 0, (self.screen[0,0] + self.offset[0,0])],
						[0, 1, 0, (self.screen[0,1] + self.offset[0,1])],
						[0, 0, 1, 0],
						[0, 0, 0, 1] ] )
		 
		#vtm = T( screen[0] + offset[0], screen[1] + offset[1], 0 ) * vtm
		#then premultiply vtm by the translation t3				
		vtm_final = t3 * vtm
		
		return vtm_final

#Lab 3, Task 3
#------------------------------task3	
	def clone(self):
		copy = View()
		copy.vrp = self.vrp.copy()
		copy.vpn = self.vpn.copy()
		copy.vup = self.vup.copy()
		copy.u = self.u.copy()
		copy.extent = self.extent.copy()
		copy.screen = self.screen.copy()
		copy.offset = self.offset.copy()
		return copy



#================================================================
#-----------------------------#Project3, Task2	
	def rotateVRC(self, angleVUP, angleU):
	
		#task2.c.1
		val = self.vrp + self.vpn * self.extent[0,2] * 0.5 
		t1 = np.matrix( [[1, 0, 0, -val[0,0]],
						 [0, 1, 0, -val[0,1]],
						 [0, 0, 1, -val[0,2]],
						 [0, 0, 0, 1] ] )
	
		#task2.c.2				 
		Rxyz = np.matrix([[self.u[0, 0], self.u[0, 1], self.u[0, 2], 0.0],
						  [self.vup[0, 0], self.vup[0, 1], self.vup[0, 2], 0.0],
						  [self.vpn[0, 0], self.vpn[0, 1], self.vpn[0, 2], 0.0 ],
						  [0, 0, 0, 1] ] )
					 
		#task2.c.3
		r1 = np.matrix( [[math.cos(angleVUP), 0, math.sin(angleVUP), 0],
						 [0, 1, 0, 0],
						 [-math.sin(angleVUP), 0,math.cos(angleVUP), 0],
						 [0, 0, 0, 1] ] )
					 
		#task2.c.4
		r2 =  np.matrix( [[1, 0, 0, 0],
						 [0, math.cos(angleU), -math.sin(angleU), 0],
						 [0, math.sin(angleU), math.cos(angleU), 0],
						 [0, 0, 0, 1] ] )
			
		#task2.c.5
		t2 = np.linalg.inv(t1) #help from Theo S.
					 
		#task2.c.6
		tvrc = np.matrix([[ self.vrp[0, 0], self.vrp[0, 1], self.vrp[0,2], 1.0],
						  [ self.u[0, 0], self.u[0, 1], self.u[0, 2], 0.0 ],
						  [ self.vup[0, 0], self.vup[0, 1], self.vup[0, 2], 0.0 ],
						  [ self.vpn[0, 0], self.vpn[0, 1], self.vpn[0, 2], 0.0 ]] )
	
		#task2.c.7				 
		tvrc = (t2*Rxyz.T*r2*r1*Rxyz*t1*tvrc.T).T
		#print tvrc
	
		#task2.c.8
		self.vrp = tvrc[0, :3]
		self.u = self.normalize(tvrc[1, :3])
		self.vup = self.normalize(tvrc[2, :3])
		self.vpn = self.normalize(tvrc[3, :3])
		#print self.u, self.vup, self.vpn
		#help from Bruce

		
		
if __name__=="__main__":
	v = View()
	print v.build()

		
		
	
	