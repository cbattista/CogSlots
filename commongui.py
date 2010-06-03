#!/usr/bin/env python

import wx

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
def create_payout_table(parent, currency):
	# create the payout table frame and sizer
	payoutgrid = wx.FlexGridSizer(1, 6, 10, 10)
	
	# the top row just has headers
	# but the first four columns don"t have headers
	for i in range(0,4):
		payoutgrid.AddStretchSpacer()
	
	payoutgrid.Add(wx.StaticText(parent, wx.ID_ANY, "10 " + currency.title()), wx.ALIGN_CENTRE)
	payoutgrid.Add(wx.StaticText(parent, wx.ID_ANY, "20 " + currency.title()), wx.ALIGN_CENTRE)

	return payoutgrid
