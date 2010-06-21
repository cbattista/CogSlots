#!/usr/bin/env python

import sys
import wx, wx.combo, wx.lib.scrolledpanel
import cfg
import commongui
import gameplay
import subjectinfo
from ExpSettings import *

class SetupGUI(wx.Frame):
	""" The interface for the tester to set up parameters """
	def __init__(self, parent, *args, **kwargs):
		# create the parent class
		wx.Frame.__init__(self, parent, *args, **kwargs)

		self.FRAME_SIZE = (800, 700)

		self.settings = Settings()

		# the notebook
		nbH = self.FRAME_SIZE[0] * 0.8
		nbW = self.FRAME_SIZE[1] * 0.4
		self.book = wx.Notebook(self, wx.ID_ANY, size=(nbH, nbW))


		betspage, betssizer = self.create_page('Bets')
		self.betspage = betspage
		symbolspage, symbolssizer = self.create_page('Symbols')
		self.symbolspage = symbolspage
		oddspage, oddssizer = self.create_page('Odds')
		infopage, infosizer = self.create_page('Info')

		# same font for all the headers
		hfont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
		hfont.SetWeight(wx.FONTWEIGHT_BOLD)
		hfont.SetPointSize(hfont.GetPointSize()*1.3)
		self.hfont = hfont

		# and the same border flag/label flag
		self.bflag = wx.SizerFlags().Border(wx.ALL, 5)
		self.eflag = self.bflag.Expand()
		hflag = wx.SizerFlags().Border(wx.LEFT, 10)
		self.hflag = hflag

		#*******************************************
		# 				The bets page
		#*******************************************
		# Number of rounds
		self.roundsentry = wx.TextCtrl(betspage, wx.ID_ANY, style=wx.TE_RIGHT)
		self.seedentry = wx.TextCtrl(betspage, wx.ID_ANY, style=wx.TE_RIGHT)
		self.debtallowed = wx.Choice(betspage, wx.ID_ANY, choices=["Allowed", "Not Allowed"])

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
		self.currencytype = wx.Choice(betspage, wx.ID_ANY, choices=["Credits", "Dollars"])
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

		self.SetBets()

		#*******************************************
		# 				The Symbols page
		#*******************************************
		# Visible types of symbols - DO WE REALLY NEED THIS?
		symbolslabel = wx.StaticText(symbolspage, wx.ID_ANY, "Visible Types of Symbols")
		symbolslabel.SetFont(hfont)
		symbolssizer.AddF(symbolslabel, hflag)
		symbolsbox = wx.BoxSizer(wx.HORIZONTAL)
		for i in cfg.symbols:
			symbolsbox.AddF(self.create_symbols_checkbox(symbolspage, i), self.bflag)
		symbolssizer.AddF(symbolsbox, self.bflag)
		symbolssizer.AddF(wx.StaticLine(symbolspage), self.bflag)

		comboslabel = wx.StaticText(self.symbolspage, wx.ID_ANY, "Winning Combinations")
		comboslabel.SetFont(self.hfont)

		symbolssizer.AddF(comboslabel, self.hflag)		# Winning Combinations
		self.wingrid = wx.FlexGridSizer(8,5,2,2)

		self.SetSymbols(self.wingrid)

		symbolssizer.AddF(self.wingrid, self.eflag)
		symbolssizer.AddF(wx.StaticLine(symbolspage), self.eflag)

		
		
		#*******************************************
		# 				The Odds page
		#*******************************************
		# Auto
		self.autoodds = wx.CheckBox(oddspage, wx.ID_ANY, "Auto Odds")
		self.autoodds.SetFont(hfont)
		self.autowinningodds = wx.TextCtrl(oddspage, wx.ID_ANY, style=wx.TE_RIGHT)
		self.autolosingodds = wx.TextCtrl(oddspage, wx.ID_ANY, style=wx.TE_RIGHT|wx.TE_READONLY)
		self.autowinningodds.SetValue(str(self.settings.winOdds))
		self.autolosingodds.SetValue(str(100 - self.settings.winOdds))
		self.autopayout = wx.Choice(oddspage, wx.ID_ANY, choices=["equal", "casino", "linear"])
		self.autopayout.SetStringSelection(self.settings.odds.kind)

		# Manual
		self.manualodds = wx.CheckBox(oddspage, wx.ID_ANY, "Manual Odds")
		self.manualodds.SetFont(hfont)
		self.payoutodds = []
		
		for o in self.settings.odds.payoutOdds:
			tc = wx.TextCtrl(oddspage, wx.ID_ANY, style=wx.TE_RIGHT)
			tc.SetValue(str(o))
			self.payoutodds.append(tc)
			
			
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
		self.manwinningodds = wx.TextCtrl(oddspage, wx.ID_ANY, style=wx.TE_RIGHT)
		self.manlosingodds = wx.TextCtrl(oddspage, wx.ID_ANY, style=wx.TE_RIGHT|wx.TE_READONLY)
		self.manwinningodds.SetValue(str(self.settings.winOdds))
		self.manlosingodds.SetValue(str(100 - self.settings.winOdds))		
		
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
		savegrid.AddF(self.filenamebox, self.eflag)
		savegrid.AddF(wx.StaticText(infopage, wx.ID_ANY, "Session Number:"), self.bflag)
		savegrid.AddF(self.sessionnumbox, self.eflag)
		infosizer.AddF(savegrid, self.eflag)
		
		# Bind some stuff
		self.Bind(wx.EVT_CHECKBOX, self.OnGetProbEstimate, self.getprobestimate)
		#*******************************************
		# 				Common Elements
		#*******************************************
		# Payout table
		payoutframe = wx.StaticBoxSizer(wx.StaticBox(self), wx.VERTICAL)
		self.payouttable = commongui.create_payout_table(self, 'credits', self.settings.bets.betsizes)

		for i in range(len(self.settings.symbols.combos)):
			payoff = self.settings.symbols.getPayoff(i)
			values = self.settings.payoffs.getPayoffRow(i)

			commongui.create_payout_row(self, self.payouttable, i, payoff[0:3], values)

		payoutframe.AddF(self.payouttable, wx.SizerFlags().Expand())
		payoutlabel = wx.StaticText(self, wx.ID_ANY, "Payout Table:")
		payoutlabel.SetFont(hfont)

		# Buttons
		buttonsizer = wx.BoxSizer(wx.HORIZONTAL)
		updatebtn = wx.Button(self, wx.ID_ANY, 'Update')
		resetbtn = wx.Button(self, wx.ID_ANY, 'Reset')
		loadbtn = wx.Button(self, wx.ID_OPEN)
		savebtn = wx.Button(self, wx.ID_SAVE)
		cancelbtn = wx.Button(self, wx.ID_CANCEL)
		okaybtn = wx.Button(self, wx.ID_OK)
		buttonsizer.AddF(updatebtn, self.bflag)
		buttonsizer.AddF(resetbtn, self.bflag)
		buttonsizer.AddF(loadbtn, self.bflag)
		buttonsizer.AddF(savebtn, self.bflag)
		buttonsizer.AddF(cancelbtn, self.bflag)
		buttonsizer.AddF(okaybtn, self.bflag)
		
		# button bindings
		self.Bind(wx.EVT_BUTTON, self.OnOkay, okaybtn)
		self.Bind(wx.EVT_BUTTON, self.OnUpdate, updatebtn)
		self.Bind(wx.EVT_BUTTON, self.OnReset, resetbtn)


		# the outer sizer to pack everything into
		bottomflag = wx.SizerFlags().Align(wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM).Border(wx.ALL, 10).Expand()
		outersizer = wx.FlexGridSizer(3, 1)
		middleSizer = wx.BoxSizer(wx.HORIZONTAL)
		payoutSizer = wx.BoxSizer(wx.VERTICAL)

		payoutSizer.AddF(payoutlabel, hflag.Border(wx.LEFT, 15))
		payoutSizer.AddF(payoutframe, bottomflag)

		middleSizer.AddF(self.book, wx.SizerFlags(1).Expand())
		middleSizer.AddF(payoutSizer, bottomflag)
		midSize = (self.FRAME_SIZE[0] * 0.5, self.FRAME_SIZE[1] * 0.85)
		middleSizer.SetMinSize(midSize)

		outersizer.AddF(middleSizer, bottomflag)
		outersizer.AddF(buttonsizer, bottomflag)

		self.SetSizerAndFit(outersizer)
		self.SetSize(self.FRAME_SIZE)
		self.Show(True)


#	def OnEditText(self, event):
		#self.setBets()

	#******************************************
	#				Settings Tab Getters and Setters
	#******************************************

	def ActivePage(self):
		currentPage = self.book.GetSelection()
		pageName = self.book.GetPageText(currentPage)
		return pageName

	def OnUpdate(self, event):
		if self.ActivePage() == 'Bets':
			self.SetBetSettings()
		if self.ActivePage() == 'Symbols':
			self.SetSymbolSettings()

	def OnReset(self, event):
		if self.ActivePage() == 'Bets':	
			self.SetBets()
		if self.ActivePage() == 'Symbols':
			self.wingrid.Clear(True)
			self.SetSymbols(self.wingrid)
			self.wingrid.Layout()

	def SetBets(self):
		#set the values of the items in the bet tab
		self.debtallowed.SetSelection(self.settings.bets.debt)
		self.roundsentry.SetValue(str(self.settings.rounds))
		self.seedentry.SetValue(str(self.settings.seed))
		while self.wagers:
			self.RemoveWager(self.wagers[0])
			
		for w in self.settings.bets.betsizes:
			w = str(w)
			self.AddWager(w, self.betspage)

	def SetBetSettings(self):
		#sets the values of the bet object based on the gui contents
		debt = self.debtallowed.GetCurrentSelection()
		currency = self.currencytype.GetCurrentSelection()
		self.settings.seed = self.seedentry.GetValue()
		self.settings.rounds = self.roundsentry.GetValue()
		betsizes = []
		for w in self.wagers:
			wagertext = w.GetItem(1).GetWindow()
			betsizes.append(float(wagertext.GetLabel().split(' ')[0]))

		self.settings.setBets(betsizes, debt, currency)	

	def SetSymbols(self, wingrid):
		self.autocombos = wx.CheckBox(self.symbolspage, wx.ID_ANY, "Autoselect")
		wingrid.Add(self.autocombos)
		for i in range(0,3):
			wingrid.AddStretchSpacer()
		wingrid.Add(wx.StaticText(self.symbolspage, wx.ID_ANY, "Payout (x wager)"))

		i = 0
		self.comboboxes = []
		self.symbolPayouts = []
		for c in self.settings.symbols.combos: 
			self.create_winning_combo(self.symbolspage, wingrid, i+1, c, self.settings.symbols.payoffs[i])
			i = i + 1



	def SetSymbolSettings(self):
		#sets the values of the symbol object based on the gui contents

		#set the combos
		combos = []
		
		combo = []
		for c in self.comboboxes:
			symbol = c.GetValue()
			if len(combo) < 3:
				combo.append(symbol)
			else:
				combos.append(combo)
				combo = [symbol]

		self.settings.symbols.combos = combos

		#set the payoffs
		payoffs = []
		for p in self.symbolPayouts:
			payoffs.append(p.GetValue())

		self.settings.payoffs = payoffs
		

	#*******************************************
	# 				Helper Functions
	#*******************************************
	def create_page(self, name):
		page = wx.lib.scrolledpanel.ScrolledPanel(self.book)
		self.book.AddPage(page, name)
		sizer = wx.BoxSizer(wx.VERTICAL)
		page.SetSizer(sizer)
		page.SetupScrolling()
		return page, sizer

	def create_symbols_checkbox(self, parent, index):
		sizer = wx.BoxSizer(wx.VERTICAL)
		img = wx.Image(index)
		img = img.Scale(cfg.SLOT_SIZE[0], cfg.SLOT_SIZE[1], 1)
		bitmap = wx.BitmapFromImage(img)

		bmp = wx.StaticBitmap(parent, wx.ID_ANY, bitmap)
		checkbox = wx.CheckBox(parent, wx.ID_ANY, "")
		sizer.AddF(bmp, self.bflag) 
		sizer.AddF(checkbox, self.bflag)
		return sizer

	def makeBitmap(self, filename):
		img = wx.Image(filename)
		img = img.Scale(cfg.SLOT_SIZE[0], cfg.SLOT_SIZE[1], 1)
		bitmap = wx.BitmapFromImage(img)
		bitmap.SetHeight(cfg.SLOT_SIZE[0])
		bitmap.SetWidth(cfg.SLOT_SIZE[1])
		return bitmap

	def create_winning_combo(self, parent, grid, index, combos, value):
		grid.AddF(wx.StaticText(parent, wx.ID_ANY, "Payout " + str(index) + ":"), self.bflag)
		# This seems like a terrible way to get the default size, but it works...
		unused = wx.combo.BitmapComboBox(parent)
		h = unused.GetSize().y
		unused.Destroy()
		for c in combos:
			combo = wx.combo.BitmapComboBox(parent, style=wx.CB_READONLY, size=(h*2, h))
			for i in range (0, len(cfg.symbols)):
				combo.Append(cfg.symbols[i], self.makeBitmap(cfg.symbols[i]))

			
			combo.SetStringSelection(c)
			self.comboboxes.append(combo)
			grid.Add(combo)

		tc = wx.TextCtrl(parent, value=str(value))

		self.symbolPayouts.append(tc) 

		grid.AddF(tc, self.bflag)
	
	def enable_sizer_items(self, sizer, enable):
		for item in sizer.GetChildren():
			window = item.GetWindow()
			if window is not None:
				window.Enable(enable)

	def update_wagers(self):
		parent = self.amountentry.GetParent()
		parent.Fit()
	#*******************************************
	# 				Wager Callbacks
	#*******************************************
	def AddWager(self, wager, parent):
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

	def OnAddWager(self, event):
		wager = self.amountentry.GetValue()
		parent = self.amountentry.GetParent()
		self.AddWager(wager, parent)

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
				break

		self.RemoveWager(wager)
		
	
	def OnEditWager(self, event, index):
		wagertext = self.wagers[index].GetItem(1).GetWindow()
		wagertext.SetLabel(self.amountentry.GetValue() + " " + self.currencytype.GetStringSelection())
		self.update_wagers()

	def RemoveWager(self, wager):
		index = self.wagers.index(wager)
		self.wagertable.Hide(self.wagers[index])
		self.wagers[index].DeleteWindows()
		del self.wagers[index]
		#self.wagernum.Delete(index+1)

		# fix the wager numbering
		i = 1
		for wager in self.wagers:
			number = wager.GetItem(0).GetWindow()
			number.SetLabel("Wager " + str(i) + ":")

			self.wagernum.SetString(i, str(i))

			i += 1
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
	
	#*******************************************
	# 				Common Callbacks
	#*******************************************
	def OnOkay(self, event):
		message = wx.MessageDialog(self, "Do you want to accept these settings?", caption="",
			style=wx.YES_NO|wx.ICON_QUESTION)
		ans = message.ShowModal()
		if ans == wx.ID_YES:
			infodialog = subjectinfo.SubjectInfoDialog(self, "Subject Info")
			infodialog.enable_control("Name", self.collectname.IsChecked())
			infodialog.enable_control("Age", self.collectage.IsChecked())
			infodialog.enable_control("Sex", self.collectsex.IsChecked())
			infodialog.enable_control("Handedness", self.collecthandedness.IsChecked())
			
			ans2 = infodialog.ShowModal()
			if ans2 == wx.ID_SAVE:
				infodialog.save_info()

if __name__ == '__main__':
    app = wx.App(False)
    mainframe = SetupGUI(None)
    app.MainLoop()
