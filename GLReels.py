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
xrot = [0.0, 0.0, 0.0]
yrot = 90.0
#xpos = [-.65, 0, .65]
inc = 0

def fitScreen():
	#get viewport origin and extent
	global xpos, inset

	viewport = glGetIntegerv(GL_VIEWPORT)
	x = viewport[0]
	y = viewport[1]
	width = viewport[2]
	height = viewport[3]
	
	#get modelview & projection matrix information
	modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
	projection = glGetDoublev(GL_PROJECTION_MATRIX)
	
	reels = len(allstops)
	
	reelWidth = windowSize[0] / reels
	
	winY = windowSize[1]/2
	
	count = 1
	#coords = []
	xpos = []
	
	for r in range(reels):
		winX = reelWidth * count - (reelWidth/2)
		#winZ = glReadPixels(winX, winY, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
		#print winZ
		c = gluUnProject(winX, winY, 0, modelview, projection, viewport)
		print c
		xpos.append(c[0])
		count+=1
	
	inset = c[2]
	

def LoadTextures():
	global textures
	global allstops
	global images
	
	count = 0
	
	stops = []
	
	for s in allstops:
		stops = stops + s
	
	images = list(set(stops))
	
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
	
	fitScreen()
	
	# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
	if Height == 0:						# Prevent A Divide By Zero If The Window Is Too Small 
		Height = 1

	glViewport(0, 0, Width, Height)		# Reset The Current Viewport And Perspective Transformation
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
	glMatrixMode(GL_MODELVIEW)

def drawCylinder(reelStops = [], radius=1, xshift=0, xrot=0, stopAt=0):
	
	#global images, textures
	
	faces = len(reelStops)
	theta = (2 * math.pi) / faces
	quad_width = (2 * radius * math.sin(theta/2)) / 2
	stopAngle = theta * stopAt - (theta/2)
	
	a = 0
	b = 0
	
	lastz = a + radius
	lasty = b

	glRotatef(xrot,1.0,0.0,0.0)
		
	for f in range(1, faces+1):
	
		face = reelStops[f-1]
		
		texture_num = images.index(face)
		angle = theta * f
	
		z = a + (radius * math.cos(angle))
		y = b + (radius * math.sin(angle))
		
		#print texture_num, textures[texture_num]

		glBindTexture(GL_TEXTURE_2D, int(textures[texture_num]))

		glBegin(GL_QUADS)
	
		glTexCoord2f(1.0, 1.0); glVertex3f(quad_width + xshift, lasty, lastz)
		glTexCoord2f(0.0, 1.0); glVertex3f(-quad_width + xshift, lasty, lastz)
		glTexCoord2f(0.0, 0.0); glVertex3f(-quad_width + xshift, y, z)
		glTexCoord2f(1.0, 0.0); glVertex3f(quad_width + xshift, y, z)
		
		lastz = z
		lasty = y
	
		glEnd() #done drawing the reel
		
	glRotatef(-xrot,1.0,0.0,0.0)
	return stopAngle
	
	# The main drawing function. 
def DrawGLScene():
	global xrot, xpos, textures, texture_num, quadratic, light, inc, settle, radius, inset
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)	# Clear The Screen And The Depth Buffer
	
	#inset = -5.0
	
	glLoadIdentity()					# Reset The View
	glTranslatef(0.0,0.0,inset)			# Move Into The Screen

	
	#glBindTexture(GL_TEXTURE_2D, int(textures[texture_num]))

	#glEnable(GL_LIGHTING)
	
	stopAngles = []
	
	radius = 1.5
	
	for s, p, r, stop in zip(allstops, xpos, xrot, stopAt):
		sa = drawCylinder(s, radius, p, r, stop)
		stopAngles.append(sa)
	#drawCylinder(allstops[1], 1.5, 0, xrot)
	#drawCylinder(allstops[2], 1.5, .65, xrot)
	
	#glBindTexture(GL_TEXTURE_2D, textures[0])

	
	
	if xrot[0] >= 1440:
		settle = True
		xrot = map(lambda x: x % 360, xrot)
		
	if settle:
		inc = inc - 1
		if inc < 1:
			inc = 1
		count = 0
		for xr, sa in zip(xrot, stopAngles):
			#print xr, sa
			if int(xr % 360) == int(sa):
				xrot[count] = xr
			else:
				xrot[count] = xr + inc
			count += 1
	else:
		xrot = map(lambda x: x + inc, xrot)
	
	
	#inc = inc - 0.05
	#print inc

	#  since this is double buffered, swap the buffers to display what just got drawn. 
	glutSwapBuffers()

def keyPressed(key, x, y):
	global inc, settle
	# If escape is pressed, kill everything.
	if key == 's':
		settle = False
		#xrot = map(lambda x: x % 360, xrot)
		#SPIN!
		inc = 30	
	
	
def main():

	global window
	global allstops, stopAt, settle, windowSize
	glutInit(sys.argv)

	allstops = [[cfg.IM_CHERRIES, cfg.IM_BAR, cfg.IM_CLOVER, cfg.IM_BELL, cfg.IM_BELL, cfg.IM_BAR, cfg.IM_CHERRIES, cfg.IM_BELL, cfg.IM_BAR, cfg.IM_CLOVER, cfg.IM_BELL, cfg.IM_BAR, cfg.IM_CHERRIES, cfg.IM_CHERRIES, cfg.IM_CHERRIES], [cfg.IM_BELL, cfg.IM_BAR, cfg.IM_CLOVER, cfg.IM_BELL, cfg.IM_BAR, cfg.IM_CHERRIES, cfg.IM_BELL, cfg.IM_BAR, cfg.IM_CLOVER, cfg.IM_BELL, cfg.IM_BAR, cfg.IM_CHERRIES, cfg.IM_CHERRIES, cfg.IM_CHERRIES, cfg.IM_CHERRIES], [cfg.IM_CHERRIES, cfg.IM_BELL, cfg.IM_BAR, cfg.IM_CLOVER, cfg.IM_BELL, cfg.IM_BAR, cfg.IM_CHERRIES, cfg.IM_BELL, cfg.IM_BAR, cfg.IM_CLOVER, cfg.IM_CHERRIES, cfg.IM_CHERRIES, cfg.IM_CHERRIES, cfg.IM_BELL, cfg.IM_BAR]]
		
	stopAt = [-1, -1, -1]
	settle = False
	
	windowSize = (480, 640)

	#Set Display Mode
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	
	glutInitWindowSize(windowSize[0], windowSize[1])
	
	# the window starts at the upper left corner of the screen 
	glutInitWindowPosition(0, 0)
	
	window = glutCreateWindow("GLReels.py")

	# Register the drawing function with glut
	glutDisplayFunc(DrawGLScene)
	
	# When we are doing nothing, redraw the scene.
	glutIdleFunc(DrawGLScene)
	
	# Register the function called when our window is resized.
	glutReshapeFunc(ReSizeGLScene)
	
	glutKeyboardFunc(keyPressed)
	
	# Initialize our window. 
	InitGL(windowSize[0], windowSize[1])
	
	# Start Event Processing Engine	
	glutMainLoop()

main()
