#!/usr/bin/env python

#default libs
import sys
import os
import math
import copy
import time
import pickle
import random

#gl stuff
from OpenGL.GL import *

#wx stuff
import wx
from wx import glcanvas

#cogslots libs
import cfg
import commongui
from Settings import Settings
import SlotReels
from CogSub import Subject
import subjectinfo

def fitScreen():
	#get viewport origin and extent
	global xpos, inset, radius, quad_width, theta

	viewport = glGetIntegerv(GL_VIEWPORT)
		
	#get modelview & projection matrix information
	modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
	projection = glGetDoublev(GL_PROJECTION_MATRIX)
	
	
	reels = len(allstops)
	
	quad_width = windowSize[0] / reels
	
	winY = windowSize[1] / 2
	
	count = 0
	#coords = []
	xpos = []
	#quad_width = 20
	
	for r in range(reels):
		xpos.append([quad_width * (count + 1), quad_width * count, quad_width * count, quad_width * (count + 1)])
		count+=1
	
	faces = len(allstops[0])
	theta = (2 * math.pi) / faces
	radius = quad_width / math.sin(theta/2) / 2
	inset = 0
	

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
	
	for i in images:
	
		imgpath = os.path.join(os.getcwd(), "images", i)
			
		image = wx.Image(imgpath)

		ix = image.GetSize()[0]
		iy = image.GetSize()[1]
		image = image.GetData()

		# Create Texture	

		glBindTexture(GL_TEXTURE_2D, int(textures[count]))   # 2d texture (x and y size)

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
	
	glViewport(0, 0, Width, Height)
	
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()					# Reset The Projection Matrix
	
	# Set up orthographic project here
	
	#glOrtho(GLdouble left, GLdouble right, GLdouble bottom, GLdouble top, GLdouble near, GLdouble far);
	
	glOrtho(0, Width, 0, Height, -1000, 0)
	#gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

	glMatrixMode(GL_MODELVIEW)

	glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1.0))		# Setup The Ambient Light 
	glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))		# Setup The Diffuse Light 
	glLightfv(GL_LIGHT0, GL_POSITION, (0.0, 0.0, 2.0, 1.0))	# Position The Light 
	glEnable(GL_LIGHT0)					# Enable Light One 
	
	fitScreen()
	
def drawCylinder(reelStops = [], xpos=[], xrot=0, stopAt=0):
	
	#global images, textures
	
	faces = len(reelStops)
	#quad_width = (2 * radius * math.sin(theta/2)) / 2
		
	stopAngle = theta * stopAt# - (theta/2)
	
	a = 0
	b = 0
	
	lastz = a + radius
	lasty = b

	#glTranslate(0.0, windowSize[0]/2, 0.0)
	
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
	
		glTexCoord2f(1.0, 1.0); glVertex3f(xpos[0], lasty, lastz)
		glTexCoord2f(0.0, 1.0); glVertex3f(xpos[1], lasty, lastz)
		glTexCoord2f(0.0, 0.0); glVertex3f(xpos[2], y, z)
		glTexCoord2f(1.0, 0.0); glVertex3f(xpos[3], y, z)
		
		lastz = z
		lasty = y
	
		glEnd() #done drawing the reel
		
	glRotatef(-xrot,1.0,0.0,0.0)
		
	deg = math.degrees(stopAngle)
	
	if deg < 0:
		return 360 - abs(deg)
	else:
		return deg

class GamePlayGUI(wx.Frame):
	""" The main gameplay GUI class """
	def __init__(self, parent, settings="", subject="", *args, **kwargs):
		# create the parent class
		wx.Frame.__init__(self, parent, *args, **kwargs)

		#self.SetSize((800, 600))
		bmp = wx.Bitmap('images/background.png')
		#self.background = wx.StaticBitmap(self, -1, bmp, (0,0))
		
		#initialize the game settings
		if settings:
			self.settings = settings
		else:

			dlg = wx.FileDialog(self, "Choose a settings file", os.path.join(os.getcwd(), "settings"), "", "*.set", wx.OPEN)
			if dlg.ShowModal() == wx.ID_OK:
				path = dlg.GetPath()
				f = open(path, "r")
				self.settings = pickle.load(f)
				f.close()
			dlg.Destroy()

		if subject:
			self.subject = subject
		else:
			d = self.settings.subInfo
			getinfo = False
			for k in d.keys():
				if d[k] == True:
					getinfo = True
					
			if getinfo:
				infodialog = subjectinfo.SubjectInfoDialog(self, "Subject Info")
				infodialog.enable_control("Name", d["Name"])
				infodialog.enable_control("Age", d["Age"])
				infodialog.enable_control("Sex", d["Sex"])
				infodialog.enable_control("Handedness", d["Handedness"])
				ans2 = infodialog.ShowModal()
				if ans2 == wx.ID_SAVE:
					#infodialog.save_info()
					infodialog.save_info()
					infodialog.cogsub.expname = self.settings.saveAs
					infodialog.cogsub.session = self.settings.session
					self.subject = infodialog.cogsub
			else:
				self.subject= Subject()
				self.subject.expname = self.settings.saveAs
				self.subject.session = self.settings.session

		fname = "%s_%s_%s_%s" % (self.subject.expname, self.subject.s_id, self.subject.session, self.subject.date)
				
		dlg = wx.FileDialog(self, "Choose a location to save subject data file", os.getcwd(), fname, "*.csv", wx.SAVE)
		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPath()
			self.subject.fpath = path
		dlg.Destroy()

		#create a Slots object
		self.slots = self.settings.slots
		self.round = 1
		self.balance = self.settings.seed
		# the pretty background - not working properly yet
		#self.background = wx.ArtProvider.GetBitmap(cfg.IM_BACKGROUND)
		#self.SetOwnBackgroundColour(cfg.FELT_GREEN)
		
		# get the user params from the database
		self.get_user_params()
		
		# create the flexy sizer that everything fits into
		self.sizer = wx.FlexGridSizer(3, 3, 10, 10)
		for i in range(0,3):
			self.sizer.AddGrowableRow(i)
			self.sizer.AddGrowableCol(i)

			
		# populate the payout sizer with values from the database
		if self.settings.showPayouts:
			payoutpanel = commongui.PayoutTable(self, self.settings)
		else:
			payoutpanel = wx.Panel(self, wx.ID_ANY)
		
		payoutpanel.SetBackgroundColour(cfg.FELT_GREEN)
		
		# create the first row
		centeredflag = wx.SizerFlags(1).Align(wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER)
		self.sizer.AddF(wx.StaticBitmap(self, wx.ID_ANY, commongui.makeBitmap(cfg.IM_ORNAMENT_LEFT, (100,100))), centeredflag)
		
		self.sizer.AddF(payoutpanel, wx.SizerFlags(1).Expand().Border(wx.ALL, 10))
		self.sizer.AddF(wx.StaticBitmap(self, wx.ID_ANY, commongui.makeBitmap(
			cfg.IM_ORNAMENT_RIGHT, (100,100))), centeredflag)
			
		# create the text boxes
		wagersizer, self.wagertext = self.create_labeled_num_box("Wager")
		self.wagertext.SetValue(str(self.settings.betsizes[0]))
		winsizer, self.wintext = self.create_labeled_num_box("Win")
		balancesizer, self.balancetext = self.create_labeled_num_box("Balance", str(self.balance))
		
		# the buttons will have to go in a separate sub-sizer
		bottomflag = wx.SizerFlags(1).Align(wx.ALIGN_BOTTOM|wx.ALIGN_CENTER).Border(wx.ALL, 5)
		buttonsizer = wx.BoxSizer(wx.HORIZONTAL)
		self.increasebtn = wx.Button(self, wx.ID_ANY, "Increase Wager")
		self.decreasebtn = wx.Button(self, wx.ID_ANY, "Decrease Wager")
		self.spinbtn = wx.Button(self, wx.ID_ANY, "SPIN")
		buttonsizer.AddF(self.decreasebtn, bottomflag)
		buttonsizer.AddF(self.spinbtn, bottomflag)
		buttonsizer.AddF(self.increasebtn, bottomflag)
		
		# the second row
		self.sizer.AddF(wagersizer, centeredflag)
		self.create_spinning_wheel(self.sizer)
		self.sizer.AddF(winsizer, centeredflag)
		
		# the third row
		self.sizer.AddF(balancesizer, bottomflag)
		self.sizer.AddF(buttonsizer, bottomflag)
		self.sizer.AddStretchSpacer()
		
		# create an outer sizer to have a nice border
		outersizer = wx.BoxSizer(wx.VERTICAL)
		outersizer.AddF(self.sizer, wx.SizerFlags(1).Expand().Align(
			wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER).Border(wx.ALL, 20));
		self.SetSizerAndFit(outersizer)
		
		# bindings
		self.decreasebtn.Bind(wx.EVT_BUTTON, lambda event, name='decrease':self.OnChangeWager(event, name))
		self.increasebtn.Bind(wx.EVT_BUTTON, lambda event, name='increase':self.OnChangeWager(event, name))
	
		self.Bind(wx.EVT_BUTTON, self.OnSpin, self.spinbtn)
	
		# these bindings are for the not-quite-functional background
		self.Bind(wx.EVT_SIZE, self.OnSize)
		
		# create the initial instructions dialog
		dialog = commongui.InfoDialog(self, "Welcome to CogSlots", 'introtext.html')
		
		if (dialog.ShowModal() == wx.ID_CANCEL):
			sys.exit(0)
		
		#if gamblersFallacy, need to purge near misses from the combos list
		if self.settings.gamblersFallacy:
			newComs = []
			for c in self.settings.combos:
				if cfg.IM_BLANK not in c:
					newComs.append(c)
				
			self.settings.combos = newComs
			
		# show thyself
		self.Centre()
		self.Show(True)
		self.Refresh()
		self.Update()
		
		#starting vars to monitor subject activity
		self.startTime = time.clock()
		self.wagerIncreases = 0
		self.wagerDecreases = 0

	
	def create_labeled_num_box(self, label, defaultvalue="0"):
		panel = wx.Panel(self)
		panel.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
		box = wx.BoxSizer(wx.VERTICAL)
		box.AddF(wx.StaticText(panel, wx.ID_ANY, label), wx.SizerFlags().Centre().Border(wx.TOP|wx.LEFT|wx.RIGHT, 10))
		textbox = wx.TextCtrl(panel, wx.ID_ANY, style=wx.TE_READONLY|wx.TE_RIGHT)
		box.AddF(textbox, wx.SizerFlags().Centre().Border(wx.BOTTOM|wx.LEFT|wx.RIGHT, 10))
		textbox.SetValue(defaultvalue)
		panel.SetSizer(box)
		return panel, textbox
	
	def get_user_params(self):
		#NOTE: this is stuff that should be retrieved from the database
		self.settings.betsizes.sort()
		self.balance = self.settings.seed# - self.settings.betsizes[0]
		self.debtallowed = self.settings.debt
		self.currency = self.settings.currency
		self.numrounds = self.settings.rounds
		self.betsizes = self.settings.betsizes	

	def num_val(self, text):
		if text is '':
			return self.num_val('0')
		return commongui.StringToType(text)
	
	def create_spinning_wheel(self, sizer, before=2, after=1):
		global allstops, xrot, windowSize, stopAt, settle, inc
		allstops = []
		settle = False
		inc = 0
		windowSize = (250, 250)
		
		reels = self.settings.slots.reels
		
		for r in reels:
			symbolList = []
			for s in r.stops:
				symbolList.append(r.symbols[s])
			allstops.append(symbolList)
		
		
		xrot = [0.0] * len(allstops)
		stopAt = [0] * len(allstops)
		
		self.GLinitialized = False
		attribList = (glcanvas.WX_GL_RGBA, # RGBA
					  glcanvas.WX_GL_DOUBLEBUFFER, # Double Buffered
					  glcanvas.WX_GL_DEPTH_SIZE, 24) # 24 bit

		#
		# Create the canvas
		self.reelBox = glcanvas.GLCanvas(self, attribList=attribList)
		self.reelBox.SetSize(windowSize)
		self.reelBox.Refresh(True)
		#
		# Set the event handlers.
		self.reelBox.Bind(wx.EVT_ERASE_BACKGROUND, self.processEraseBackgroundEvent)
		self.reelBox.Bind(wx.EVT_SIZE, self.processSizeEvent)
		self.reelBox.Bind(wx.EVT_PAINT, self.processPaintEvent)
		
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.OnDraw, self.timer)
		
		sizer.AddF(self.reelBox, wx.SizerFlags().Align(wx.ALIGN_CENTER))
	
	def phoneySpin(self):
	
		if self.settings.gamblersFallacy:
			theItem = self.settings.stimList.pop(0)
		else:
			odds = self.settings.override['odds']
			nms = self.settings.override['nearMiss']
			itemList =[]
			index = 0

			for o, nm in zip(odds, nms):
				item = self.settings.combos[index]
				itemList = itemList + ([item] * o)
				if nm:
					newItem = copy.deepcopy(item)
					newItem[0] = cfg.IM_BLANK
					random.shuffle(newItem)
					itemList = itemList + ([newItem] * o)
								
				index = index + 1
				if nm:
					numLoss = 100 - sum(odds) - sum(nms)
				else:
					numLoss = 100 - sum(odds)
				
				
			itemList = itemList + (['LOSS'] * numLoss)
				
			theItem = random.choice(itemList)
		
		if theItem != "LOSS":
			payline = theItem
			while cfg.IM_EMPTY in theItem:
				newItem = random.choice(self.settings.symbols)
				theItem.replace(item, newItem, 1)
				print "switching any"
			#now we need to come up with the actual payline numbers
			stopAt = []
			count = 0
			for item, reel in zip(theItem, self.settings.slots.reels):
				symbolIndex = reel.symbols.index(item)
				indeces = []
				symcount = 0
				for stop in reel.stops:
					if stop == symbolIndex:
						indeces.append(symcount)
					symcount += 1
				
				stopAt.append(random.choice(indeces))
					
				count += 1
				
		else:
			loss = False
			while not loss:
				imageList, payline, stopAt = self.slots.spin()
				outcome = self.judgeOutcome(payline)
				if not outcome:
					loss = True
		
		return payline, stopAt
	
	
	def OnSpin(self, event):
		
		global settle, inc, stopAt
		
		RT = time.clock() - self.startTime
		
		self.subject.inputData(self.round, "RT", RT)
		self.subject.inputData(self.round, "wagerInc", self.wagerIncreases)
		self.subject.inputData(self.round, "wagerDec", self.wagerDecreases)
		
		self.wagerIncreases = 0
		self.wagerDecreases = 0
		
		self.spinbtn.Disable()
		
		if self.settings.gamblersFallacy or self.settings.override['engage']:
			payline,stopAt = self.phoneySpin()
		else:
			imageList, payline, stopAt = self.slots.spin(2)

		self.payline = payline
		
		self.timer.Start(1)
		
		pcount = 1
		for p in payline:
			self.subject.inputData(self.round, 'Reel %s' % pcount, p)
			pcount += 1
		
		settle = False
		#SPIN!
		inc = 30	
		self.spinning = True
		
	def afterSpin(self):
	
		self.startTime = time.clock()
	
		wager = commongui.StringToType(self.wagertext.GetValue())
		win = self.judgeOutcome(self.payline)
		
		if win:
			payout = self.settings.payouts[win-1]
			self.subject.inputData(self.round, 'outcome', 'WIN')
		else:
			payout = 0
			self.subject.inputData(self.round, 'outcome', 'LOSS')

		self.subject.inputData(self.round, 'oldbalance', self.balance)
		self.subject.inputData(self.round, 'wager', wager)
		self.subject.inputData(self.round, 'payout', payout)

		if win:
			self.balance += wager*payout
			self.subject.inputData(self.round, 'delta', wager*payout)
			# Update the balance text box with the current balance
			self.wintext.SetValue(str(wager*payout))
		else:
			self.balance -= wager
			self.wintext.SetValue(str(-wager))
			self.subject.inputData(self.round, 'delta', -wager)

		self.subject.inputData(self.round, 'newbalance', self.balance)

		self.balancetext.SetValue(str(self.balance))
		
		# Reset the wager to zero
		self.wagertext.SetValue(str(self.settings.betsizes[0]))

		if self.settings.probDict['obtain'] == True:
			msg = self.settings.probDict['msg']
			pround = self.settings.probDict['interval']
			if (self.round) % pround == 0:
				dia = commongui.ProbDialog(self, "Probability Estimate", msg)
				outcome = dia.ShowModal()
				if outcome == wx.ID_OK:
					est = dia.est.GetValue()
					est = est.replace(",", "_")
					self.subject.inputData(self.round, 'estimate', est)
			else:
				self.subject.inputData(self.round, 'estimate', "NA")
		else:
			self.subject.inputData(self.round, 'estimate', "NA")

		self.round += 1

		self.Refresh()
		self.Update()

		if self.balance <= 0 and not self.settings.debt:
			self.gameOver("You're out of money.")

		# Check to see if the maximum number of rounds has been reached 
		if self.round > self.settings.rounds:
			self.gameOver("Round limit reached.")
			
		self.subject.printData()
						
	def judgeOutcome(self, payline):
		#if we are dealing with the 'any' symbol, we must account for that
		any = False
		for c in self.settings.combos:
			if cfg.IM_EMPTY in c:
				any = True				
		if any:
			for c in self.settings.combos:
				match = []
				for cc, p in zip(c, payline):
					if cc == cfg.IM_EMPTY or cc == p:
						match.append(self.settings.combos.index(c) + 1)
					else:
						match.append(0)
				if not match.count(0):
					return match[0]
		else:
			if payline in self.settings.combos:
				return self.settings.combos.index(payline) + 1
		return 0
		
	# Callbacks!
	def OnChangeWager(self, event, name):
		wager = self.wagertext.GetValue()
		wager = commongui.StringToType(wager)

		i = self.betsizes.index(wager)

		# if we can't increase beyond zero, stop doing anything
		if 'increase' in name:
			self.wagerIncreases += 1
			if (i + 1) >= len(self.betsizes):
				return

			self.wagerstep = self.betsizes[i+1]

			if (self.balance < self.wagerstep) and not self.settings.debt:
				return 
			self.balance -= self.wagerstep - int(wager)
			wager = self.wagerstep
					
		elif 'decrease' in name:
			self.wagerDecreases += 1
			if i == 0:
				return

			self.wagerstep = self.betsizes[i-1]

			# we can't automatically win money!
			if wager < self.wagerstep:
				return
			self.balance += wager - self.wagerstep
			wager = self.wagerstep
		
		self.wagertext.SetValue(str(wager))
		self.balancetext.SetValue(str(self.balance))
	
	def gameOver(self, msg):
		self.subject.printData()
		self.subject.preserve()
		dlg = wx.MessageDialog(self, msg, "Game over", wx.OK)
		dlg.ShowModal()
		dlg.Destroy()
		self.Destroy()
	
		
	def OnSize(self, event):
		#self.background = wx.ArtProvider.GetBitmap(cfg.IM_BACKGROUND, size=self.GetSize())
		event.Skip()
		self.Refresh(False)
		
	#
	# Canvas Proxy Methods

	def GetGLExtents(self):
		"""Get the extents of the OpenGL canvas."""
		return self.reelBox.GetClientSize()

	def SwapBuffers(self):
		"""Swap the OpenGL buffers."""
		self.reelBox.SwapBuffers()

	#
	# wxPython Window Handlers

	def processEraseBackgroundEvent(self, event):
		"""Process the erase background event."""
		pass # Do nothing, to avoid flashing on MSWin

	def processSizeEvent(self, event):
		"""Process the resize event."""
		if self.reelBox.GetContext():
			# Make sure the frame is shown before calling SetCurrent.
			self.Show()
			self.reelBox.SetCurrent()

			size = self.GetGLExtents()
			self.OnReshape(size.width, size.height)
		event.Skip()

	def processPaintEvent(self, event):
		"""Process the drawing event."""
		self.reelBox.SetCurrent()

		# This is a 'perfect' time to initialize OpenGL ... only if we need to
		if not self.GLinitialized:
			self.OnInitGL()
			self.GLinitialized = True

		self.OnDraw()
		event.Skip()

	#
	# GLFrame OpenGL Event Handlers

	def OnInitGL(self):
		InitGL(windowSize[0], windowSize[1])

	def OnReshape(self, width, height):
		"""Reshape the OpenGL viewport based on the dimensions of the window."""
		glViewport(0, 0, width, height)

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(-0.5, 0.5, -0.5, 0.5, -1, 1)

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

	def OnDraw(self, *args, **kwargs):
		"Draw the window."
		global xrot, textures, texture_num, settle, radius, inset, inc, settle
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)	# Clear The Screen And The Depth Buffer
		
		#inset = -5.0
		
		glLoadIdentity()					# Reset The View
		glTranslatef(0.0,windowSize[1]/2 - quad_width/2,0.0)			# Move Into The Screen

		
		#glBindTexture(GL_TEXTURE_2D, int(textures[texture_num]))

		#glEnable(GL_LIGHTING)
		
		stopAngles = []
			
		for s, p, r, stop in zip(allstops, xpos, xrot, stopAt):
			sa = drawCylinder(s, p, r, stop)
			stopAngles.append(sa)
		#drawCylinder(allstops[1], 1.5, 0, xrot)
		#drawCylinder(allstops[2], 1.5, .65, xrot)
		
		#glBindTexture(GL_TEXTURE_2D, textures[0])
		if xrot[0] > 365 and not settle:
			inc = 21
			
		if xrot[0] > 720 and not settle:
			inc = 14
		
		if xrot[0] > 1080 and not settle:
			inc = 7
		
		
		if xrot[0] > 1440:
			settle = True
			xrot = map(lambda x: x % 360, xrot)

		#print settle
			
		if settle:
			inc = inc - 1
			if inc < 1:
				inc = 1
			count = 0
			stoppedReels = 0
			for xr, sa in zip(xrot, stopAngles):
				if int(xr % 360) == int(sa):
					xrot[count] = xr
					stoppedReels += 1 
				else:
					xrot[count] = xr + inc
					
				if stoppedReels == len(xrot) and self.spinning:
					self.spinbtn.Enable()
					self.spinning = False
					self.afterSpin()
				count += 1
		else:
			xrot = map(lambda x: x + inc, xrot)
		self.SwapBuffers()

		
if __name__ == "__main__":
	app = wx.App(False)
	mainframe = GamePlayGUI(None)
	app.MainLoop()

