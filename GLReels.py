"""
GL algo

Drawing

1.  Get the size of the client window.
2.  Determine size of cylinder such that the appropriate amount of symbols to be displayed, are displayed.  Also determine the size necessary to fit all the reels.
3.  Create a texture out of the symbols that corresponds with the appropriate sizing.
4.  Wrap Reel in textures.

Animating

1.  Randomly determine the order in which each reel will stop.
2.  Spin the suckas...

"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import wx
import os
import cfg
import math

# Rotations for cube. 
zrot = 0.0
xrot = 0.0
yrot = 90.0

def LoadTextures():
	global textures
	global stops
	global images
	
	count = 0
	
	images = list(set(stops))
	
	print images, stops
	
	textures = glGenTextures(len(images))
	
	print textures
	
	for i in images:
	
		imgpath = os.path.join(os.getcwd(), "images", i)
		print imgpath
			
		image = wx.Image(imgpath)

		ix = image.GetSize()[0]
		iy = image.GetSize()[1]
		image = image.GetData()

		# Create Texture	

		glBindTexture(GL_TEXTURE_2D, int(textures[count]))   # 2d texture (x and y size)

		print count
		
		glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
		glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
		glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGB, GL_UNSIGNED_BYTE, image)
		
		count += 1


# A general OpenGL initialization function.  Sets all of the initial parameters. 
def InitGL(Width, Height):				# We call this right after our OpenGL window is created.
		
	LoadTextures()

	glEnable(GL_TEXTURE_2D)
	glClearColor(0.0, 0.0, 0.0, 0.0)	# This Will Clear The Background Color To Black
	glClearDepth(1.0)					# Enables Clearing Of The Depth Buffer
	glDepthFunc(GL_LESS)				# The Type Of Depth Test To Do
	glEnable(GL_DEPTH_TEST)				# Enables Depth Testing
	glShadeModel(GL_SMOOTH)				# Enables Smooth Color Shading
	
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()					# Reset The Projection Matrix
										# Calculate The Aspect Ratio Of The Window
	gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

	glMatrixMode(GL_MODELVIEW)

	glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1.0))		# Setup The Ambient Light 
	glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))		# Setup The Diffuse Light 
	glLightfv(GL_LIGHT0, GL_POSITION, (0.0, 0.0, 2.0, 1.0))	# Position The Light 
	glEnable(GL_LIGHT0)					# Enable Light One 
	
	# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
	if Height == 0:						# Prevent A Divide By Zero If The Window Is Too Small 
		Height = 1

	glViewport(0, 0, Width, Height)		# Reset The Current Viewport And Perspective Transformation
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
	glMatrixMode(GL_MODELVIEW)

def drawCylinder(stops = [], radius=1):
	
	global images, textures
	
	faces = len(stops)
	theta = (2 * math.pi) / faces
	quad_width = (2 * radius * math.sin(theta/2)) / 2
	
	a = 0
	b = 0
	
	lastz = a + radius
	lasty = b

		
	for f in range(1, faces+1):
	
		face = stops[f-1]
		
		texture_num = images.index(face)
		angle = theta * f
	
		z = a + (radius * math.cos(angle))
		y = b + (radius * math.sin(angle))
		
		#print texture_num, textures[texture_num]

		glBindTexture(GL_TEXTURE_2D, int(textures[texture_num]))

		glBegin(GL_QUADS)
	
		glTexCoord2f(1.0, 1.0); glVertex3f(quad_width, lasty, lastz)
		glTexCoord2f(0.0, 1.0); glVertex3f(-quad_width, lasty, lastz)
		glTexCoord2f(0.0, 0.0); glVertex3f(-quad_width, y, z)
		glTexCoord2f(1.0, 0.0); glVertex3f(quad_width, y, z)
		
		lastz = z
		lasty = y
	
		glEnd() #done drawing the reel
		
	
	# The main drawing function. 
def DrawGLScene():
	global xrot, yrot, zrot, textures, texture_num, quadratic, light, stops
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)	# Clear The Screen And The Depth Buffer

	glLoadIdentity()					# Reset The View
	glTranslatef(0.0,0.0,-5.0)			# Move Into The Screen

	
	#glBindTexture(GL_TEXTURE_2D, int(textures[texture_num]))

	#glEnable(GL_LIGHTING)
	
	glRotatef(xrot,1.0,0.0,0.0)	
	
	drawCylinder(stops, 1)
	
	#glBindTexture(GL_TEXTURE_2D, textures[0])

	xrot  = xrot + 1				# X rotation

	#  since this is double buffered, swap the buffers to display what just got drawn. 
	glutSwapBuffers()
	
def main():

	global window
	global stops
	glutInit(sys.argv)

	stops = [cfg.IM_CHERRIES, cfg.IM_BELL, cfg.IM_BAR, cfg.IM_CLOVER, cfg.IM_BELL, cfg.IM_BAR, cfg.IM_CHERRIES, cfg.IM_BELL, cfg.IM_BAR, cfg.IM_CLOVER, cfg.IM_BELL, cfg.IM_BAR]
	
	# Select type of Display mode:   
	#  Double buffer 
	#  RGBA color
	# Alpha components supported 
	# Depth buffer
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	
	# get a 640 x 480 window 
	glutInitWindowSize(640, 480)
	
	# the window starts at the upper left corner of the screen 
	glutInitWindowPosition(0, 0)
	
	# Okay, like the C version we retain the window id to use when closing, but for those of you new
	# to Python (like myself), remember this assignment would make the variable local and not global
	# if it weren't for the global declaration at the start of main.
	window = glutCreateWindow("GLReels.py")

	# Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
	# set the function pointer and invoke a function to actually register the callback, otherwise it
	# would be very much like the C version of the code.	
	glutDisplayFunc(DrawGLScene)
	
	# Uncomment this line to get full screen.
	# glutFullScreen()

	# When we are doing nothing, redraw the scene.
	glutIdleFunc(DrawGLScene)
	
	# Register the function called when our window is resized.
	glutReshapeFunc(ReSizeGLScene)
	
	# Initialize our window. 
	InitGL(640, 480)

	# Start Event Processing Engine	
	glutMainLoop()


# Print message to console, and kick off the main to get it rolling.
print "Hit ESC key to quit."
main()
