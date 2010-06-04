#!/usr/bin/env python

import sys
import wx
import cfg
import commongui

class GamePlayGUI(wx.Frame):
	""" The main gameplay GUI class """
	def __init__(self, parent, *args, **kwargs):
		# create the parent class
		wx.Frame.__init__(self, parent, *args, **kwargs)
		
		# the pretty background - not working properly yet
#		self.background = wx.ArtProvider.GetBitmap(cfg.IM_BACKGROUND)
		self.SetBackgroundColour((0,153,0))
		
		# get the user params from the database
		self.get_user_params()
		
		# create the flexy sizer that everything fits into
		self.sizer = wx.FlexGridSizer(3, 3, 10, 10)
		for i in range(0,3):
			self.sizer.AddGrowableRow(i)
			self.sizer.AddGrowableCol(i)
		
		# populate the payout sizer with values from the database
		payoutgrid = commongui.create_payout_table(self, self.currency)
		payouttable = wx.StaticBoxSizer(wx.StaticBox(self), wx.VERTICAL)
		for i in range (1,8):
			commongui.create_payout_row(self, payoutgrid, i)
		payouttable.AddF(payoutgrid, wx.SizerFlags().Border(wx.ALL, 5))
		
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
	
		# these bindings are for the not-quite-functional background
	#	self.Bind(wx.EVT_BUTTON, self.OnSpin, self.spinbtn)
	#	self.Bind(wx.EVT_PAINT, self.OnPaint)
	#	self.Bind(wx.EVT_SIZE, self.OnSize)
		
		# create the initial instructions dialog
		dialog = commongui.InfoDialog(self, "Welcome to CogSlots", 'introtext.html')
		
		if (dialog.ShowModal() == wx.ID_CANCEL):
			sys.exit(0)
		
		# show thyself
		self.Centre()
		self.Show(True)
	
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
		if 'increase' in name:
			if self.balance < self.wagerstep and not self.debtallowed:
				return
			wager += self.wagerstep
			self.balance -= self.wagerstep
		
		elif 'decrease' in name:
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
	
	def OnPaint(self, event):
		dc = wx.BufferedPaintDC(self, self.background)
		
	def OnSize(self, event):
		self.background = wx.ArtProvider.GetBitmap(cfg.IM_BACKGROUND, size=self.GetSize())
		event.Skip()
		self.Refresh(False)
		
if __name__ == "__main__":
	app = wx.App(False)
	mainframe = GamePlayGUI(None)
	app.MainLoop()
