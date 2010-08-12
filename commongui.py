#!/usr/bin/env python

import wx, wx.html, wx.combo
import cfg
import CogSub

class ProbDialog(wx.Dialog):
	"""Simple dialog to obtain probability estimate"""
	def __init__(self, parent, title, msg):
		wx.Dialog.__init__(self, parent, -1, title)
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(wx.StaticText(self, -1, msg), 1)
		self.est = wx.SpinCtrl(self, -1, "0")
		sizer.Add(self.est, 1)
		sizer.Add(wx.Button(self, wx.ID_OK, "OK"), 1)
		self.SetSizerAndFit(sizer)

class InfoDialog(wx.Dialog):
	""" A simple dialogue to display an html file """
	def __init__(self, parent, title, htmlfile, okaytext="Start Game"):
		wx.Dialog.__init__(self, parent, wx.ID_ANY, title)
		
		# create the sizers
		sizer = wx.BoxSizer(wx.VERTICAL)
		buttonsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		# create the html view window
		self.html = wx.html.HtmlWindow(self, wx.ID_ANY, size=(320, 320))
		self.html.SetBorders(10)
		self.set_html_file(htmlfile)
		
		# create the buttons
		buttonflag = wx.SizerFlags().Align(wx.ALIGN_RIGHT).Border(wx.ALL, 10)
		buttonsizer.AddF(wx.Button(self, wx.ID_CANCEL), buttonflag)
		buttonsizer.AddF(wx.Button(self, wx.ID_OK, okaytext), buttonflag)
		
		# put it all together
		sizer.AddF(self.html, wx.SizerFlags(0).Expand().Border(wx.ALL, 10) )
		sizer.AddF(buttonsizer, buttonflag)
		
		self.SetSizerAndFit(sizer)
	
	def set_html_file(self, htmlfile):
		self.html.LoadFile(htmlfile)


# The payout table class

class PayoutTable(wx.Panel):
	""" A class to display the payout information """
	def __init__(self, parent, settings):
		wx.Panel.__init__(self, parent)
		
		# copy the values over to class variables
		self.settings = settings
		
		# make a pretty static box to enclose everything
		self.boxsizer = wx.StaticBoxSizer(wx.StaticBox(self, label="Payout Table"), wx.VERTICAL)
		
		# create the payout table frame and sizer
		self.payoutgrid = wx.FlexGridSizer(1, len(self.settings.betsizes) + self.settings.numReels + 1, 2, 2)
		
		# populate the table with the initial settings
		self.update()
		
		self.boxsizer.AddF(self.payoutgrid, wx.SizerFlags().Expand().Border(wx.ALL,10))
		self.SetSizerAndFit(self.boxsizer)

	def update(self, settings=None):
	
		if (settings):
			self.settings = settings
	
		# clear the old grid and recreate it
		self.payoutgrid.Clear(True)
		self.payoutgrid.SetCols(len(self.settings.betsizes) + self.settings.numReels + 1)
	
		# the top row just has headers
		# but the label and reels columns don't have headers
		for i in range(0,1+self.settings.numReels):
			self.payoutgrid.AddStretchSpacer()

		# bolden the header labels
		hfont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
		hfont.SetWeight(wx.FONTWEIGHT_BOLD)
		
		flag = wx.SizerFlags(1).Align(wx.ALIGN_CENTRE).Border(wx.LEFT|wx.RIGHT, 5)
		
		for b in self.settings.betsizes:
			label = wx.StaticText(self, wx.ID_ANY, "%s %s" % (b, self.settings.currency))
			label.SetFont(hfont)
			self.payoutgrid.AddF(label, flag)
		
		for i in range(min(self.settings.numPayouts, len(self.settings.combos))):
			# create the array of values = the bets times the payout for this combo
			values = []
			for b in self.settings.betsizes:
				values.append(self.settings.payouts[i]*b)
			icons = self.settings.combos[i]
			
			# if there's a mismatch between the number of symbols and the combos
			# available, either limit them or pad them
			if len(icons) > self.settings.numReels:
				icons = icons[0:self.settings.numReels]	
			
			# the bell seems to be the default in the combo boxes
			if len(icons) < self.settings.numReels:
				for i in range(self.settings.numReels - len(icons)):
					icons.append(cfg.IM_BELL)
				
			self.payoutgrid.AddF(wx.StaticText(self, wx.ID_ANY, "Payout " + str(i+1) + ":"), flag)

			for icon in icons:
				img = wx.Image(icon)
				try:
					img = img.Scale(cfg.SLOT_SIZE[0], cfg.SLOT_SIZE[1], 1)
				except:
					pass
				bitmap = wx.BitmapFromImage(img)
				bitmap.SetHeight(cfg.SLOT_SIZE[0])
				bitmap.SetWidth(cfg.SLOT_SIZE[1])
				icon = wx.StaticBitmap(self, wx.ID_ANY, bitmap)
				self.payoutgrid.AddF(icon, flag)
			
			for v in values:
				self.payoutgrid.AddF(wx.StaticText(self, wx.ID_ANY, "%s" % v), flag)
		
		self.Fit()

def makeBitmap(filename, scale=()):
	#make wx.Bitmap of an image from a file, and optionally scale it
	img = wx.Image(filename)
	if scale:
		try:
			img = img.Scale(scale[0], scale[1], 1)
		except:
			pass
	bitmap = wx.BitmapFromImage(img)
	if scale:
		bitmap.SetHeight(scale[0])
		bitmap.SetWidth(scale[1])
	return bitmap
