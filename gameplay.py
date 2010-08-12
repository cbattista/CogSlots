#!/usr/bin/env python

import sys
import wx
import cfg
import commongui
from Settings import Settings
import SlotReels
from CogSub import Subject
import pickle

class GamePlayGUI(wx.Frame):
	""" The main gameplay GUI class """
	def __init__(self, parent, settings="", subject="", *args, **kwargs):
		# create the parent class
		wx.Frame.__init__(self, parent, *args, **kwargs)

		#initialize the game settings
		if settings:
			self.settings = settings
		else:
			f = open("settings/default.set", "r")
			self.settings = pickle.load(f)
			f.close()
		

		if subject:
			self.subject = subject
		else:
			self.subject= Subject()
		#create a Slots object
		self.slots = self.settings.slots
		self.round = 1

		# the pretty background - not working properly yet
		#self.background = wx.ArtProvider.GetBitmap(cfg.IM_BACKGROUND)
		self.SetOwnBackgroundColour(cfg.FELT_GREEN)
		
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
		self.sizer.AddF(wx.StaticBitmap(self, wx.ID_ANY, wx.ArtProvider.GetBitmap(
			cfg.IM_ORNAMENT_LEFT, size=(40,80))), centeredflag)
		
		self.sizer.AddF(payoutpanel, wx.SizerFlags(1).Expand().Border(wx.ALL, 10))
		self.sizer.AddF(wx.StaticBitmap(self, wx.ID_ANY, wx.ArtProvider.GetBitmap(
			cfg.IM_ORNAMENT_RIGHT, size=(40,80))), centeredflag)
			
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
		
		# show thyself
		self.Centre()
		self.Show(True)
		self.Refresh()
		self.Update()

	
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
		self.balance = self.settings.seed - self.settings.betsizes[0]
		self.debtallowed = self.settings.debt
		self.currency = self.settings.currency
		self.numrounds = self.settings.rounds
		self.betsizes = self.settings.betsizes	

	def num_val(self, text):
		if text is '':
			return self.num_val('0')
		if self.currency is 'dollars':
			return int(text)
		elif self.currency is 'credits':
			return int(text)
	
	def create_spinning_wheel(self, sizer, before=2, after=1):
		#NOTE: this will be the real spinning gui stuff

		self.slotButtons = []
		span = range(-before,after+1)

		reelBox = wx.GridSizer(3, self.settings.numReels)

		
		for i in span:
			for r in self.slots.reels:
				#create reel image
				bmpfile = r.getIndex(i)
				bmp = commongui.makeBitmap(bmpfile, (50, 50))
				#put it on a button
				if i == 0:
					button = wx.BitmapButton(self, -1, bmp)
					button.SetBackgroundColour(cfg.WINNING_GOLD)
				else:
					button = wx.BitmapButton(self, -1, bmp)
				#add this to the list to access when spinning occurs
				self.slotButtons.append(button)
				reelBox.Add(button)

		sizer.Add(reelBox)
	
	def spin(self):
		imageList, payline = self.slots.spin(2)
		pcount = 1
		for p in payline:
			self.subject.inputData(self.round, 'Reel %s' % pcount, p)
			pcount += 1

		for sb, img in zip(self.slotButtons, imageList):
			bmp = commongui.makeBitmap(img, (50, 50))
			sb.SetBitmapLabel(bmp)

		if payline in self.settings.combos:
			self.subject.inputData(self.round, 'outcome', 'WIN')
			return self.settings.combos.index(payline)

		self.subject.inputData(self.round, 'outcome', 'LOSS')
		return 0


	# Callbacks!
	def OnChangeWager(self, event, name):
		wager = self.wagertext.GetValue()

		i = self.betsizes.index(int(wager))

		# if we can't increase beyond zero, stop doing anything
		if 'increase' in name:
			if (i + 1) >= len(self.betsizes):
				return

			self.wagerstep = self.betsizes[i+1]

			if self.balance < self.wagerstep and not self.debtallowed:
				return 
			#self.balance -= self.wagerstep - int(wager)
			wager = self.wagerstep
		
		elif 'decrease' in name:
			if i == 0:
				return

			self.wagerstep = self.betsizes[i-1]

			# we can't automatically win money!
			if wager < self.wagerstep:
				return
			self.balance += int(wager) - self.wagerstep
			wager = self.wagerstep
		
		self.wagertext.SetValue(str(wager))
		self.balancetext.SetValue(str(self.balance))
	
	def OnSpin(self, event):
		win = self.spin()
		wager = int(self.wagertext.GetValue())


		payout = self.settings.payouts[win]
		payout = int(payout)

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
					self.subject.inputData(self.round, 'estimate', est)
			else:
				self.subject.inputData(self.round, 'estimate', "NA")
		else:
			self.subject.inputData(self.round, 'estimate', "NA")

		self.round += 1

		self.Refresh()
		self.Update()


		if self.balance <= 0 and self.settings.debt == False:
			self.gameOver()

		# Check to see if the maximum number of rounds has been reached 
		if self.round > self.settings.rounds:
			self.gameOver()
		
				
	def gameOver(self):
		self.subject.printData()
		#wx.MessageBox("Game over!")
		self.subject.preserve()
		self.Destroy()
	
		
	def OnSize(self, event):
		#self.background = wx.ArtProvider.GetBitmap(cfg.IM_BACKGROUND, size=self.GetSize())
		event.Skip()
		self.Refresh(False)
		
if __name__ == "__main__":
	app = wx.App(False)
	mainframe = GamePlayGUI(None)
	app.MainLoop()

