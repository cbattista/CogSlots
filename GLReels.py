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
from Image import *

# Rotations for cube. 
zrot = 0.0
xrot = 0.0
yrot = 90.0

def LoadTextures():
	global textures
	image = open("images/strip.bmp")
	
	ix = image.size[0]
	iy = image.size[1]
	image = image.tostring("raw", "RGBX", 0, -1)
	
	# Create Texture
	textures = glGenTextures(3)
	glBindTexture(GL_TEXTURE_2D, int(textures[0]))   # 2d texture (x and y size)
	
	glPixelStorei(GL_UNPACK_ALIGNMENT,1)
	glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
	glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

	# Create Linear Filtered Texture 
	glBindTexture(GL_TEXTURE_2D, int(textures[1]))
	glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
	glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
	glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)

	# Create MipMapped Texture
	glBindTexture(GL_TEXTURE_2D, int(textures[2]))
	glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
	glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR_MIPMAP_NEAREST)
	gluBuild2DMipmaps(GL_TEXTURE_2D, 3, ix, iy, GL_RGBA, GL_UNSIGNED_BYTE, image)


# A general OpenGL initialization function.  Sets all of the initial parameters. 
def InitGL(Width, Height):				# We call this right after our OpenGL window is created.
	global quadratic
	
	#LoadTextures()

	quadratic = gluNewQuadric()
	gluQuadricNormals(quadratic, GLU_SMOOTH)		# Create Smooth Normals (NEW) 
	gluQuadricTexture(quadratic, GL_TRUE)			# Create Texture Coords (NEW) 
 
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
	
	# The main drawing function. 
def DrawGLScene():
	global xrot, yrot, zrot, textures, texture_num, object, quadratic, light

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)	# Clear The Screen And The Depth Buffer

	glLoadIdentity()					# Reset The View
	glTranslatef(0.0,0.0,-5.0)			# Move Into The Screen

	glRotatef(xrot,1.0,0.0,0.0)			# Rotate The Cube On It's X Axis
	glRotatef(yrot,0.0,1.0,0.0)			# Rotate The Cube On It's Y Axis
	glRotatef(zrot,0.0,0.0,1.0)			# Rotate The Cube On It's Z Axis
	
	#glBindTexture(GL_TEXTURE_2D, int(textures[texture_num]))

	glEnable(GL_LIGHTING)

	glTranslatef(0.0,0.0,-1.6)			# Center The Cylinder 
	gluCylinder(quadratic,1.0,1.0,1.0,32,32)	# A Cylinder With A Radius Of 0.5 And A Height Of 2 

	glTranslatef(0.0,0.0,1.1)			# Center The Cylinder 
	gluCylinder(quadratic,1.0,1.0,1.0,32,32)

	glTranslatef(0.0,0.0,1.1)			# Center The Cylinder 
	gluCylinder(quadratic,1.0,1.0,1.0,32,32)

	glBindTexture(GL_TEXTURE_2D, textures[2])

	#xrot  = xrot + 0.2				# X rotation
	#yrot = yrot + 0.2				 # Y rotation
	zrot = zrot + 1				 # Z rotation


	#  since this is double buffered, swap the buffers to display what just got drawn. 
	glutSwapBuffers()
	
def main():

	global window
	glutInit(sys.argv)

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
	window = glutCreateWindow("Jeff Molofee's GL Code Tutorial ... NeHe '99")

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
