#!/usr/bin/env python

import sys
import wx, wx.combo, wx.lib.scrolledpanel
import cfg
import commongui
import gameplay

class SetupGUI(wx.Frame):
	""" The interface for the tester to set up parameters """
	def __init__(self, parent, *args, **kwargs):
		# create the parent class
		wx.Frame.__init__(self, parent, *args, **kwargs)

		# the notebook
		self.book = wx.Notebook(self, wx.ID_ANY)
		betspage, betssizer = self.create_page('Bets')
		symbolspage, symbolssizer = self.create_page('Symbols')
		oddspage, oddssizer = self.create_page('Odds')
		infopage, infosizer = self.create_page('Info')

		# same font for all the headers
		hfont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
		hfont.SetWeight(wx.FONTWEIGHT_BOLD)
		hfont.SetPointSize(hfont.GetPointSize()*1.3)

		# and the same border flag/label flag
		self.bflag = wx.SizerFlags().Border(wx.ALL, 5)
		self.eflag = self.bflag.Expand()
		hflag = wx.SizerFlags().Border(wx.LEFT, 10)

		#*******************************************
		# 				The bets page
		#*******************************************
		# Number of rounds
		self.roundsentry = wx.TextCtrl(betspage, wx.ID_ANY, style=wx.TE_RIGHT)
		self.debtallowed = wx.Choice(betspage, wx.ID_ANY, choices=["Allowed", "Not Allowed"])

		# Currency
		self.seedentry = wx.TextCtrl(betspage, wx.ID_ANY, style=wx.TE_RIGHT)
		self.currencytype = wx.Choice(betspage, wx.ID_ANY, choices=["Credits", "Dollars"])

		# Wagers
		self.wagernum = wx.Choice(betspage, wx.ID_ANY, choices=["New"])
		self.amountentry = wx.TextCtrl(betspage, wx.ID_ANY, style=wx.TE_RIGHT)
		self.addbtn = wx.Button(betspage, wx.ID_ANY, "Add")
		self.wagertable = wx.StaticBoxSizer(wx.StaticBox(betspage), wx.VERTICAL)
		self.wagers = []

		# number of rounds stuff
		roundslabel = wx.StaticText(betspage, wx.ID_ANY, "Number of Rounds:")
		roundslabel.SetFont(hfont)
		betssizer.AddF(roundslabel, hflag)
		numroundsbox = wx.BoxSizer(wx.HORIZONTAL)
		numroundsbox.AddF(self.roundsentry, self.bflag)
		numroundsbox.AddF(wx.StaticText(betspage, wx.ID_ANY, "Subject Debt:"), self.bflag)
		numroundsbox.AddF(self.debtallowed, self.bflag)
		betssizer.AddF(numroundsbox, self.bflag)
		betssizer.AddF(wx.StaticLine(betspage), self.eflag)

		# the currency stuff
		currencylabel = wx.StaticText(betspage, wx.ID_ANY, "Currency:")
		currencylabel.SetFont(hfont)
		betssizer.AddF(currencylabel, hflag)
		currencybox = wx.BoxSizer(wx.HORIZONTAL)
		currencybox.AddF(wx.StaticText(betspage, wx.ID_ANY, "Seed Amount:"), self.bflag)
		currencybox.AddF(self.seedentry, self.bflag)
		currencybox.AddF(self.currencytype, self.bflag)
		betssizer.AddF(currencybox, self.bflag)
		betssizer.AddF(wx.StaticLine(betspage), self.eflag)

		# the wager stuff
		wagerlabel = wx.StaticText(betspage, wx.ID_ANY, "Wagers:")
		wagerlabel.SetFont(hfont)
		betssizer.AddF(wagerlabel, hflag)
		wagerbox = wx.BoxSizer(wx.HORIZONTAL)
		wagerbox.AddF(self.wagernum, self.bflag)
		wagerbox.AddF(wx.StaticText(betspage, wx.ID_ANY, "Amount:"), self.bflag)
		wagerbox.AddF(self.amountentry, self.bflag)
		wagerbox.AddF(self.addbtn, self.bflag)
		betssizer.AddF(wagerbox, self.bflag)
		betssizer.AddF(self.wagertable, self.eflag)
		
		# Bindings, woot
		self.Bind(wx.EVT_BUTTON, self.OnAddWager, self.addbtn)
		self.Bind(wx.EVT_CHOICE, self.OnChooseWager, self.wagernum)

		#*******************************************
		# 				The Symbols page
		#*******************************************
		self.autoselect = wx.CheckBox(symbolspage, wx.ID_ANY, "Autoselect")

		# Visible types of symbols
		symbolslabel = wx.StaticText(symbolspage, wx.ID_ANY, "Visible Types of Symbols")
		symbolslabel.SetFont(hfont)
		symbolssizer.AddF(symbolslabel, hflag)
		symbolsbox = wx.BoxSizer(wx.HORIZONTAL)
		for i in range (0, len(cfg.symbols)):
			symbolsbox.AddF(self.create_symbols_checkbox(symbolspage, i), self.bflag)
		symbolssizer.AddF(symbolsbox, self.bflag)
		symbolssizer.AddF(wx.StaticLine(symbolspage), self.bflag)

		# Winning Combinations
		comboslabel = wx.StaticText(symbolspage, wx.ID_ANY, "Winning Combinations")
		comboslabel.SetFont(hfont)
		symbolssizer.AddF(comboslabel, hflag)
		symbolssizer.AddF(self.autoselect, self.bflag)
		symbolssizer.AddF(wx.StaticText(symbolspage, wx.ID_ANY, "Payout (x wager)"), wx.SizerFlags().Align(wx.ALIGN_RIGHT).Border(wx.RIGHT, 15))
		for i in range(0,7):
			symbolssizer.Add(self.create_winning_combo(symbolspage, i))
		symbolssizer.AddF(wx.StaticLine(symbolspage), self.eflag)
		
		#*******************************************
		# 				The Odds page
		#*******************************************
		# Auto
		self.autoodds = wx.CheckBox(oddspage, wx.ID_ANY, "Auto Odds")
		self.autoodds.SetFont(hfont)
		self.autowinningodds = wx.TextCtrl(oddspage, wx.ID_ANY, style=wx.TE_RIGHT)
		self.autolosingodds = wx.TextCtrl(oddspage, wx.ID_ANY, style=wx.TE_RIGHT|wx.TE_READONLY)
		self.autopayout = wx.Choice(oddspage, wx.ID_ANY, choices=["Equal Odds", "Casino Odds", "Linear Odds"])
		
		# Manual
		self.manualodds = wx.CheckBox(oddspage, wx.ID_ANY, "Manual Odds")
		self.manualodds.SetFont(hfont)
		self.payoutodds = []
		for i in range(0,7):
			self.payoutodds.append(wx.TextCtrl(oddspage, wx.ID_ANY, style=wx.TE_RIGHT))
		self.manwinningodds = wx.TextCtrl(oddspage, wx.ID_ANY, style=wx.TE_RIGHT|wx.TE_READONLY)
		self.manlosingodds = wx.TextCtrl(oddspage, wx.ID_ANY, style=wx.TE_RIGHT|wx.TE_READONLY)
		
		# Near Misses
		self.nearmisses = wx.TextCtrl(oddspage, wx.ID_ANY, style=wx.TE_RIGHT)
		self.chance = wx.CheckBox(oddspage, wx.ID_ANY, "Chance")
		
		# Some useful stuff
		percentsign = lambda: wx.StaticText(oddspage, wx.ID_ANY, "%")
		rflag = wx.SizerFlags().Align(wx.ALIGN_RIGHT).Border(wx.ALL, 5)
		
		# Pack together the auto stuff
		oddssizer.AddF(self.autoodds, hflag)
		self.autogrid = wx.FlexGridSizer(3, 3)
		self.autogrid.AddF(wx.StaticText(oddspage, wx.ID_ANY, "Overall Odds of Winning:"), self.bflag)
		self.autogrid.AddF(self.autowinningodds, self.bflag)
		self.autogrid.AddF(percentsign(), self.bflag)
		self.autogrid.AddF(wx.StaticText(oddspage, wx.ID_ANY, "Overall Odds of Losing:"), self.bflag)
		self.autogrid.AddF(self.autolosingodds, rflag)
		self.autogrid.AddF(percentsign(), self.bflag)
		self.autogrid.AddF(wx.StaticText(oddspage, wx.ID_ANY, "Auto Odds Payouts 1-7:"), self.bflag)
		self.autogrid.AddF(self.autopayout, self.bflag)
		oddssizer.AddF(self.autogrid, self.eflag)
		oddssizer.AddF(wx.StaticLine(oddspage), self.eflag)
		
		# pack up the manual stuff
		oddssizer.AddF(self.manualodds, hflag)
		self.manualgrid = wx.FlexGridSizer(7, 6)
		self.manualgrid.AddF(wx.StaticText(oddspage, wx.ID_ANY, "Payout 1:"), self.bflag)
		self.manualgrid.AddF(self.payoutodds[0], self.bflag)
		self.manualgrid.AddF(percentsign(), self.bflag)
		self.manualgrid.AddF(wx.StaticText(oddspage, wx.ID_ANY, "Overall Odds of Winning:"), rflag)
		self.manualgrid.AddF(self.manwinningodds, rflag)
		self.manualgrid.AddF(percentsign(), rflag)
		self.manualgrid.AddF(wx.StaticText(oddspage, wx.ID_ANY, "Payout 2:"), self.bflag)
		self.manualgrid.AddF(self.payoutodds[1], self.bflag)
		self.manualgrid.AddF(percentsign(), self.bflag)
		self.manualgrid.AddF(wx.StaticText(oddspage, wx.ID_ANY, "Overall Odds of Losing:"), rflag)
		self.manualgrid.AddF(self.manlosingodds, rflag)
		self.manualgrid.AddF(percentsign(), rflag)
		
		# the rest don't have anything in the last three columns
		for i in range(2,len(self.payoutodds)):
			self.manualgrid.AddF(wx.StaticText(oddspage, wx.ID_ANY, "Payout " + str(i+1) + ":"), self.bflag)
			self.manualgrid.AddF(self.payoutodds[i], self.bflag)
			self.manualgrid.AddF(percentsign(), self.bflag)
			for x in range(0,3):
				self.manualgrid.AddStretchSpacer()
		
		oddssizer.AddF(self.manualgrid, self.eflag)
		oddssizer.AddF(wx.StaticLine(oddspage), self.eflag)
		
		# Near misses... made more sense to have its own section, as it's used in both manual and auto
		nearmissrow = wx.BoxSizer(wx.HORIZONTAL)
		nearmissrow.AddF(wx.StaticText(oddspage, wx.ID_ANY, "Near Misses:"), self.bflag)
		nearmissrow.AddF(self.nearmisses, self.bflag)
		nearmissrow.AddF(percentsign(), self.bflag)
		nearmissrow.AddF(self.chance, self.bflag)
		oddssizer.AddF(nearmissrow, self.eflag)
		
		# Odds page bindings
		self.Bind(wx.EVT_CHECKBOX, self.OnOddsTypeChecked, self.autoodds)
		self.Bind(wx.EVT_CHECKBOX, self.OnOddsTypeChecked, self.manualodds)
		self.Bind(wx.EVT_CHECKBOX, self.OnChanceChecked, self.chance)
		
		#*******************************************
		# 				The Info page
		#*******************************************
		# subject info
		self.collectname = wx.CheckBox(infopage, wx.ID_ANY, "Name")
		self.collectage = wx.CheckBox(infopage, wx.ID_ANY, "Age")
		self.collectsex = wx.CheckBox(infopage, wx.ID_ANY, "Sex")
		self.collecthandedness = wx.CheckBox(infopage, wx.ID_ANY, "Handedness")
		
		# subjective probability estimate
		self.getprobestimate = wx.CheckBox(infopage, wx.ID_ANY, "Obtain Subject Probability Estimate")
		self.getprobestimate.SetFont(hfont)
		self.estimatetiming = wx.Choice(infopage, wx.ID_ANY, choices=["At Beginning", "At End"])
		self.estimateinterval = wx.TextCtrl(infopage, wx.ID_ANY, style=wx.TE_RIGHT)
		
		# save as
		self.filenamebox = wx.TextCtrl(infopage, wx.ID_ANY)
		self.sessionnumbox = wx.TextCtrl(infopage, wx.ID_ANY, style=wx.TE_RIGHT)
		
		# info collection package
		infolabel = wx.StaticText(infopage, wx.ID_ANY, "Collect Subject Information")
		infolabel.SetFont(hfont)
		infosizer.AddF(infolabel, hflag)
		infosizer.AddF(self.collectname, self.bflag)
		infosizer.AddF(self.collectage, self.bflag)
		infosizer.AddF(self.collectsex, self.bflag)
		infosizer.AddF(self.collecthandedness, self.bflag)
		infosizer.AddF(wx.StaticLine(infopage), self.eflag)
		
		# probability estimate stuff
		infosizer.AddF(self.getprobestimate, hflag)
		self.probrow = wx.BoxSizer(wx.HORIZONTAL)
		self.probrow.AddF(self.estimatetiming, self.bflag)
		self.probrow.AddF(wx.StaticText(infopage, wx.ID_ANY, "of every"), self.bflag)
		self.probrow.AddF(self.estimateinterval, self.bflag)
		self.probrow.AddF(wx.StaticText(infopage, wx.ID_ANY, "rounds"), self.bflag)
		infosizer.AddF(self.probrow, self.eflag)
		infosizer.AddF(wx.StaticLine(infopage), self.eflag)
		
		# Save as
		saveaslabel = wx.StaticText(infopage, wx.ID_ANY, "Save As:")
		saveaslabel.SetFont(hfont)
		infosizer.AddF(saveaslabel, hflag)
		savegrid = wx.FlexGridSizer(2,2)
		savegrid.AddF(wx.StaticText(infopage, wx.ID_ANY, "Filename:"), self.bflag)
		savegrid.AddF(self.filenamebox, self.bflag)
		savegrid.AddF(wx.StaticText(infopage, wx.ID_ANY, "Session Number:"), self.bflag)
		savegrid.AddF(self.sessionnumbox, self.bflag)
		infosizer.AddF(savegrid, self.eflag)
		
		# Bind some stuff
		self.Bind(wx.EVT_CHECKBOX, self.OnGetProbEstimate, self.getprobestimate)
		#*******************************************
		# 				Common Elements
		#*******************************************
		# Payout table
		payoutframe = wx.StaticBoxSizer(wx.StaticBox(self), wx.VERTICAL)
		self.payouttable = commongui.create_payout_table(self, 'credits')
		payoutframe.AddF(self.payouttable, wx.SizerFlags().Expand())
		payoutlabel = wx.StaticText(self, wx.ID_ANY, "Payout Table:")
		payoutlabel.SetFont(hfont)

		# Buttons
		buttonsizer = wx.BoxSizer(wx.HORIZONTAL)
		loadbtn = wx.Button(self, wx.ID_OPEN)
		savebtn = wx.Button(self, wx.ID_SAVE)
		cancelbtn = wx.Button(self, wx.ID_CANCEL)
		okaybtn = wx.Button(self, wx.ID_OK)
		buttonsizer.AddF(loadbtn, self.bflag)
		buttonsizer.AddF(savebtn, self.bflag)
		buttonsizer.AddF(cancelbtn, self.bflag)
		buttonsizer.AddF(okaybtn, self.bflag)

		# the outer sizer to pack everything into
		outersizer = wx.BoxSizer(wx.VERTICAL)
		outersizer.AddF(self.book, self.bflag)
		outersizer.AddF(payoutlabel, hflag.Border(wx.LEFT, 15))
		outersizer.AddF(payoutframe, self.bflag)
		outersizer.AddF(buttonsizer, self.bflag)

		self.SetSizerAndFit(outersizer)
		self.Show(True)
		
	#*******************************************
	# 				Helper Functions
	#*******************************************
	def create_page(self, name):
		# TODO: scrolling doesn't seem to behave
		page = wx.lib.scrolledpanel.ScrolledPanel(self.book)
		self.book.AddPage(page, name)
		sizer = wx.BoxSizer(wx.VERTICAL)
		page.SetSizer(sizer)
		return page, sizer

	def create_symbols_checkbox(self, parent, index):
		sizer = wx.BoxSizer(wx.VERTICAL)
		bmp = wx.StaticBitmap(parent, wx.ID_ANY, wx.ArtProvider.GetBitmap(cfg.symbols[index]))
		checkbox = wx.CheckBox(parent, wx.ID_ANY, cfg.symbolnames[index])
		sizer.AddF(bmp, self.bflag) 
		sizer.AddF(checkbox, self.bflag)
		return sizer

	def create_winning_combo(self, parent, index):
		row = wx.BoxSizer(wx.HORIZONTAL)
		row.AddF(wx.StaticText(parent, wx.ID_ANY, "Payout " + str(index) + ":"), self.bflag)
		comboboxes = []
		# TODO: this makes kinda ugly wide combobox items that can't seem to shrink
		for i in range(0,3):
			comboboxes.append(wx.combo.BitmapComboBox(parent, style=wx.CB_READONLY))
			row.Add(comboboxes[i])
		for combobox in comboboxes:
			for i in range (0, len(cfg.symbols)):
				combobox.Append(cfg.symbolnames[i], wx.ArtProvider.GetBitmap(cfg.symbols[i]))
		row.AddF(wx.TextCtrl(parent), self.bflag)
		return row
	
	def enable_sizer_items(self, sizer, enable):
		for item in sizer.GetChildren():
			window = item.GetWindow()
			if window is not None:
				window.Enable(enable)

	def update_wagers(self):
		parent = self.amountentry.GetParent()
		parent.Layout()
		self.Layout()
		self.Fit()
			
	#*******************************************
	# 				Wager Callbacks
	#*******************************************
	def OnAddWager(self, event):
		wager = self.amountentry.GetValue()
		parent = self.amountentry.GetParent()
		index = len(self.wagers)
		deletebtn = wx.Button(parent, wx.ID_ANY, "Delete")
		self.Bind(wx.EVT_BUTTON, self.OnDeleteWager, deletebtn)
		self.wagernum.Append(str(index+1))

		# create the new sizer
		row = wx.BoxSizer(wx.HORIZONTAL)
		row.AddF(wx.StaticText(parent, wx.ID_ANY, "Wager " + str(index+1) + ":"), self.bflag)
		row.AddF(wx.StaticText(parent, wx.ID_ANY, wager + " " + self.currencytype.GetStringSelection()), self.bflag)
		row.AddF(deletebtn, self.bflag)
		self.wagers.append(row)
		self.wagertable.AddF(row, self.bflag)
		self.update_wagers()

	def OnChooseWager(self, event):
		index = event.GetSelection()
		if index is 0:
			self.addbtn.SetLabel("Add")
			self.addbtn.Unbind(wx.EVT_BUTTON)
			self.Bind(wx.EVT_BUTTON, self.OnAddWager, self.addbtn)

		elif index is not -1:
			self.addbtn.SetLabel("Edit")
			self.Unbind(wx.EVT_BUTTON, self.addbtn)
			# need to subtract one from the index to account for the "New" item
			self.addbtn.Bind(wx.EVT_BUTTON, lambda event : self.OnEditWager(event, index-1))

	def OnDeleteWager(self, event):
		index = -1
		for wager in self.wagers:
			if wager.GetItem(2).GetWindow() is event.GetEventObject():
				index = self.wagers.index(wager)
				
		self.wagertable.Hide(self.wagers[index])
		self.wagers[index].DeleteWindows()
		del self.wagers[index]
		self.wagernum.Delete(index+1)

		# fix the wager numbering
		i = 1
		for wager in self.wagers:
			number = wager.GetItem(0).GetWindow()
			number.SetLabel("Wager " + str(i) + ":")
			self.wagernum.SetString(i, str(i))
			i += 1
		self.update_wagers()
	
	def OnEditWager(self, event, index):
		wagertext = self.wagers[index].GetItem(1).GetWindow()
		wagertext.SetLabel(self.amountentry.GetValue() + " " + self.currencytype.GetStringSelection())
		self.update_wagers()
		
	#*******************************************
	# 				Symbols Callbacks
	#*******************************************
	def OnSymbolChecked(self, event, index):
		# do something to show/hide the icons in the comboboxes
		print "Not yet implemented"
	
	#*******************************************
	# 				Odds Callbacks
	#*******************************************
	def OnChanceChecked(self, event):
		self.nearmisses.Enable(not event.IsChecked())

	def OnOddsTypeChecked(self, event):
		checked = event.IsChecked()
		if event.GetEventObject() is self.autoodds:
			otherbox = self.manualodds
			othergrid = self.manualgrid
			self.enable_sizer_items(self.autogrid, checked)
		elif event.GetEventObject() is self.manualodds:
			otherbox = self.autoodds
			othergrid = self.autogrid
			self.enable_sizer_items(self.manualgrid, checked)
		else:
			return
		otherbox.SetValue(not checked)
		self.enable_sizer_items(othergrid, not checked)
	
	#*******************************************
	# 				Info Callbacks
	#*******************************************
	def OnGetProbEstimate(self, event):
		self.enable_sizer_items(self.probrow, event.IsChecked())

if __name__ == '__main__':
    app = wx.App(False)
    mainframe = SetupGUI(None)
    app.MainLoop()
