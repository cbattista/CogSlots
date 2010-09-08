import cfg
import math

def drawCylinder(stops = [], radius=1):
	faces = len(stops)
	theta = (2 * math.pi) / faces
	quad_width = 2 * radius * math.sin(theta/2) 
	
	a = 0
	b = 0
	
	lastx = a + radius
	lasty = b
	
	for f in range(1, faces+1):
		angle = theta * f
		x = a + (radius * math.cos(angle))
		y = b + (radius * math.sin(angle))
		print "QUAD:", lastx, lasty, x, y
		lastx = x
		lasty = y

stops = [cfg.IM_CHERRIES, cfg.IM_BELL, cfg.IM_BAR, cfg.IM_CLOVER]

drawCylinder(stops, 2)
