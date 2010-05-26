#!/usr/bin/env python

import sys
import wx, wx.html
import cfg

import random # this is just temporary

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

class GamePlayGUI(wx.Frame):
	""" The main gameplay GUI class """
	def __init__(self, parent, *args, **kwargs):
		# create the parent class
		wx.Frame.__init__(self, parent, *args, **kwargs)
		self.SetBackgroundColour(wx.GREEN)
		
		# get the user params from the database
		self.get_user_params()
		
		# create the flexy sizer that everything fits into
		self.sizer = wx.FlexGridSizer(3, 3, 10, 10)
		for i in range(0,3):
			self.sizer.AddGrowableRow(i)
			self.sizer.AddGrowableCol(i)
		
		# populate the payout sizer with values from the database
		payouttable = self.create_payout_table()
		
		# create the first row
		centeredflag = wx.SizerFlags(1).Align(wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER)
		self.sizer.AddF(wx.StaticBitmap(self, wx.ID_ANY, wx.ArtProvider.GetBitmap(
			cfg.IM_ORNAMENT_LEFT, size=(40,80))), centeredflag)
		self.sizer.AddF(payouttable, centeredflag)
		self.sizer.AddF(wx.StaticBitmap(self, wx.ID_ANY, wx.ArtProvider.GetBitmap(
			cfg.IM_ORNAMENT_RIGHT, size=(40,80))), centeredflag)
			
		# create the text boxes
		wagersizer, self.wagertext = self.create_labeled_num_box("Wager")
		winsizer, self.wintext = self.create_labeled_num_box("Win")
		balancesizer, self.balancetext = self.create_labeled_num_box("Balance", str(self.balance))
		
		# the buttons will have to go in a separate sub-sizer
		bottomflag = wx.SizerFlags(1).Align(wx.ALIGN_BOTTOM|wx.ALIGN_CENTER)
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
		
		# create the initial instructions dialog
		dialog = InfoDialog(self, "Welcome to " + cfg.program_name, cfg.introfile)
		
		if (dialog.ShowModal() == wx.ID_CANCEL):
			sys.exit(0)
		
		# show thyself
		self.Centre()
		self.Show(True)
		
	def create_payout_table(self):
		# create the payout table frame and sizer
		payoutsizer = wx.StaticBoxSizer(wx.StaticBox(self), wx.VERTICAL)
		payoutgrid = wx.FlexGridSizer(1, 6, 10, 10)
		
		# the top row just has headers
		# but the first four columns don"t have headers
		for i in range(0,4):
			payoutgrid.AddStretchSpacer()
		
		payoutgrid.Add(wx.StaticText(self, wx.ID_ANY, "10 Credits"), wx.ALIGN_CENTRE)
		payoutgrid.Add(wx.StaticText(self, wx.ID_ANY, "20 Credits"), wx.ALIGN_CENTRE)
		
		#NOTE: this should be "while payout data available from database"
		flag = wx.SizerFlags(1).Align(wx.ALIGN_RIGHT)
		payoutnum = 1
		while payoutnum < 5:
			payoutgrid.AddF(wx.StaticText(self, wx.ID_ANY, "Payout %d" %payoutnum), flag)
			#NOTE: I would put in a switch statement here depending on what icons are desired
			payoutgrid.Add(wx.StaticBitmap(self, wx.ID_ANY, 
				wx.ArtProvider.GetBitmap(cfg.IM_CHERRIES, size=cfg.SLOT_SIZE)))
			payoutgrid.Add(wx.StaticBitmap(self, wx.ID_ANY,
				wx.ArtProvider.GetBitmap(cfg.IM_CHERRIES, size=cfg.SLOT_SIZE)))
			payoutgrid.Add(wx.StaticBitmap(self, wx.ID_ANY, 
				wx.ArtProvider.GetBitmap(cfg.IM_CHERRIES, size=cfg.SLOT_SIZE)))
			#NOTE: again, a temporary number until there"s real data
			credits = random.randrange(10, 1000)
			payoutgrid.AddF(wx.StaticText(self, wx.ID_ANY, "%d" %credits), flag)
			payoutgrid.AddF(wx.StaticText(self, wx.ID_ANY, "%d" %(credits*2)), flag)
			payoutnum += 1
		
		payoutsizer.AddF(payoutgrid, wx.SizerFlags(1).Expand())
		return payoutsizer
	
	def create_labeled_num_box(self, label, defaultvalue="0"):
		box = wx.StaticBoxSizer(wx.StaticBox(self), wx.VERTICAL)
		box.AddF(wx.StaticText(self, wx.ID_ANY, label), wx.SizerFlags().Centre())
		textbox = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_READONLY|wx.TE_RIGHT)
		box.AddF(textbox, wx.SizerFlags().Centre())
		textbox.SetValue(defaultvalue)
		return box, textbox
	
	def get_user_params(self):
		#NOTE: this is stuff that should be retrieved from the database
		self.balance = 50
		self.debtallowed = False
		self.currency = 'dollars'
		self.wagerstep = 10
		self.numrounds = 5
	
	def num_val(self, text):
		if text is '':
			return self.num_val('0')
		if self.currency is 'dollars':
			return float(text)
		elif self.currency is 'credits':
			return int(text)
	
	def create_spinning_wheel(self, sizer):
		#NOTE: this will be the real spinning gui stuff
		sizer.AddStretchSpacer()
	
	# Callbacks!
	def OnChangeWager(self, event, name):
		wager = self.num_val(self.wagertext.GetValue())
		
		# if we can't increase beyond zero, stop doing anything
		if "increase" in name:
			if self.balance < self.wagerstep and not self.debtallowed:
				return
			wager += self.wagerstep
			self.balance -= self.wagerstep
		
		elif "decrease" in name:
			# we can't automatically win money!
			if wager < self.wagerstep:
				return
			wager -= self.wagerstep
			self.balance += self.wagerstep
		
		self.wagertext.SetValue(str(wager))
		self.balancetext.SetValue(str(self.balance))
	
	def OnSpin(self, event):
		wager = self.num_val(self.wagertext.GetValue())
		if wager < self.wagerstep:
			return
			
		#NOTE: actual spinning and winning would occur...
		win = random.randint(0,1)
		if win is 1:
			self.balance += wager*2
			# Update the balance text box with the current balance
			self.balancetext.SetValue(str(self.balance))
			self.wintext.SetValue(str(wager))
		elif win is 0:
			self.wintext.SetValue(str(-wager))
		
		# Reset the wager to zero
		self.wagertext.SetValue('0')
		
		# Check to see if the maximum number of rounds has been reached 
		self.numrounds -= 1
		if self.numrounds is 0:
			wx.MessageBox("Game over!")
			
if __name__ == "__main__":
	app = wx.App(False)
	mainframe = GamePlayGUI(None)
	app.MainLoop()
