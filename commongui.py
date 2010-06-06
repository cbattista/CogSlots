#!/usr/bin/env python

import wx, wx.html
import cfg
import random # just for now

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
		wx.Dialog.__init__(self, parent, wx.ID_ANY, title)

# Some functions
def create_payout_row(parent, payoutgrid, index): # and payouts/symbols etc, see TODO below
	#TODO: I'm not sure how your symbols and payouts classes are supposed to work, I'll leave
	# that stuff up to you.  For now, I'll fake it with random cherries.
	
	flag = wx.SizerFlags(1).Align(wx.ALIGN_RIGHT)
	payoutgrid.AddF(wx.StaticText(parent, wx.ID_ANY, "Payout " + str(index) + ":"), flag)
	payoutgrid.Add(wx.StaticBitmap(parent, wx.ID_ANY, 
		wx.ArtProvider.GetBitmap(cfg.IM_CHERRIES, size=cfg.SLOT_SIZE)))
	payoutgrid.Add(wx.StaticBitmap(parent, wx.ID_ANY,
		wx.ArtProvider.GetBitmap(cfg.IM_CHERRIES, size=cfg.SLOT_SIZE)))
	payoutgrid.Add(wx.StaticBitmap(parent, wx.ID_ANY, 
		wx.ArtProvider.GetBitmap(cfg.IM_CHERRIES, size=cfg.SLOT_SIZE)))
	#NOTE: again, a temporary number until there"s real data
	credits = random.randrange(10, 1000)
	payoutgrid.AddF(wx.StaticText(parent, wx.ID_ANY, "%d" %credits), flag)
	payoutgrid.AddF(wx.StaticText(parent, wx.ID_ANY, "%d" %(credits*2)), flag)

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
