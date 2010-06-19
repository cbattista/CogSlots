#!/usr/bin/env python

import wx, wx.html
import cfg

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

# Some functions
def create_payout_row(parent, payoutgrid, index, icons, value, maxpayouts = 2): # and payouts/symbols etc
	
	flag = wx.SizerFlags(1).Align(wx.ALIGN_RIGHT)
	payoutgrid.AddF(wx.StaticText(parent, wx.ID_ANY, "Payout " + str(index) + ":"), flag)

	for icon in icons:
		img = wx.Image(icon)
		img = img.Scale(cfg.SLOT_SIZE[0], cfg.SLOT_SIZE[1], 1)
		bitmap = wx.BitmapFromImage(img)
		bitmap.SetHeight(cfg.SLOT_SIZE[0])
		bitmap.SetWidth(cfg.SLOT_SIZE[1])
		icon = wx.StaticBitmap(parent, wx.ID_ANY, bitmap)
		payoutgrid.Add(icon)

	for v in value[0:maxpayouts]:
		payoutgrid.AddF(wx.StaticText(parent, wx.ID_ANY, "%s" % v), flag)

def create_payout_table(parent, currency, bets, maxpayouts = 2):
	# create the payout table frame and sizer
	payoutgrid = wx.FlexGridSizer(1, maxpayouts + 4, 10, 10)
	
	# the top row just has headers
	# but the first four columns don"t have headers
	for i in range(0,4):
		payoutgrid.AddStretchSpacer()

	for b in bets[0:2]:	
		payoutgrid.Add(wx.StaticText(parent, wx.ID_ANY, "%s %s" % (b, currency.title())), wx.ALIGN_CENTRE)

	return payoutgrid

def makeBitmap(filename, scale=()):
	#make wx.Bitmap of an image from a file, and optionally scale it
	img = wx.Image(filename)
	if scale:
		img = img.Scale(scale[0], scale[1], 1)
	bitmap = wx.BitmapFromImage(img)
	if scale:
		bitmap.SetHeight(scale[0])
		bitmap.SetWidth(scale[1])
	return bitmap
