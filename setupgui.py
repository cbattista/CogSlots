#!/usr/bin/env python

import sys
import wx, wx.combo, wx.lib.scrolledpanel
import cfg
import commongui
import gameplay
import subjectinfo
from Settings import Settings
import pickle

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

		# same font for all the headers
		self.hfont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
		self.hfont.SetWeight(wx.FONTWEIGHT_BOLD)
		self.hfont.SetPointSize(self.hfont.GetPointSize()*1.3)

		# and the same border flag/label flag
		self.bflag = wx.SizerFlags().Border(wx.ALL, 5)
		self.eflag = self.bflag.Expand()
		self.hflag = wx.SizerFlags().Border(wx.LEFT, 10)

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
		roundslabel.SetFont(self.hfont)
		betssizer.AddF(roundslabel, self.hflag)
		numroundsbox = wx.BoxSizer(wx.HORIZONTAL)
		numroundsbox.AddF(self.roundsentry, self.bflag)
		numroundsbox.AddF(wx.StaticText(betspage, wx.ID_ANY, "Subject Debt:"), self.bflag)
		numroundsbox.AddF(self.debtallowed, self.bflag)
		betssizer.AddF(numroundsbox, self.bflag)
		betssizer.AddF(wx.StaticLine(betspage), self.eflag)

		# the currency stuff
		currencylabel = wx.StaticText(betspage, wx.ID_ANY, "Currency:")
		currencylabel.SetFont(self.hfont)
		betssizer.AddF(currencylabel, self.hflag)
		self.currencytype = wx.Choice(betspage, wx.ID_ANY, choices=["Credits", "Dollars"])
		currencybox = wx.BoxSizer(wx.HORIZONTAL)
		currencybox.AddF(wx.StaticText(betspage, wx.ID_ANY, "Seed Amount:"), self.bflag)
		currencybox.AddF(self.seedentry, self.bflag)
		currencybox.AddF(self.currencytype, self.bflag)
		betssizer.AddF(currencybox, self.bflag)
		betssizer.AddF(wx.StaticLine(betspage), self.eflag)

		# the wager stuff
		wagerlabel = wx.StaticText(betspage, wx.ID_ANY, "Wagers:")
		wagerlabel.SetFont(self.hfont)
		betssizer.AddF(wagerlabel, self.hflag)
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
		# Visible types of symbols
		symbolslabel = wx.StaticText(symbolspage, wx.ID_ANY, "Visible Types of Symbols")
		symbolslabel.SetFont(self.hfont)
		symbolssizer.AddF(symbolslabel, self.hflag)
		symbolsbox = wx.BoxSizer(wx.HORIZONTAL)

		self.symbolCheckBoxes = []

		for i in cfg.symbols:
			mySym = self.create_symbols_checkbox(symbolspage, i)
			symbolsbox.AddF(mySym, self.bflag)
		symbolssizer.AddF(symbolsbox, self.bflag)
		symbolssizer.AddF(wx.StaticLine(symbolspage), self.bflag)

		comboslabel = wx.StaticText(self.symbolspage, wx.ID_ANY, "Winning Combinations")
		comboslabel.SetFont(self.hfont)

		symbolssizer.AddF(comboslabel, self.hflag)		# Winning Combinations
		wingrid = wx.FlexGridSizer(8,5,2,2)
		self.wingrid = wingrid

		self.autocombos = wx.CheckBox(self.symbolspage, wx.ID_ANY, "Autoselect")
		wingrid.Add(self.autocombos)
		self.wcount = 0
		self.comboIndexes = []
		self.payoutIndexes = []
	
		for i in range(0,3):
			wingrid.AddStretchSpacer()
			self.wcount += 1

		wingrid.Add(wx.StaticText(self.symbolspage, wx.ID_ANY, "Payout (x wager)"))
		self.wcount += 1

		i = 0
		self.comboboxes = []
		self.symbolPayouts = []
		for c in self.settings.combos: 
			self.create_winning_combo(self.symbolspage, wingrid, i+1, c, self.settings.payouts[i])
			i = i + 1
	
		self.SetSymbols(wingrid)

		symbolssizer.AddF(wingrid, self.eflag)
		symbolssizer.AddF(wx.StaticLine(symbolspage), self.eflag)

		
		
		#*******************************************
		# 				The Odds page
		#*******************************************
		# Auto
		self.autoodds = wx.CheckBox(oddspage, wx.ID_ANY, "Auto Odds")
		self.autoodds.SetFont(self.hfont)
		self.autowinningodds = wx.TextCtrl(oddspage, wx.ID_ANY, style=wx.TE_RIGHT)
		self.autolosingodds = wx.TextCtrl(oddspage, wx.ID_ANY, style=wx.TE_RIGHT|wx.TE_READONLY)
		self.autopayout = wx.Choice(oddspage, wx.ID_ANY, choices=["equal", "casino", "linear"])

		# Manual
		self.manualodds = wx.CheckBox(oddspage, wx.ID_ANY, "Manual Odds")
		self.manualodds.SetFont(self.hfont)
		self.payoutodds = []
		
		for o in self.settings.payoutOdds:
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
		oddssizer.AddF(self.autoodds, self.hflag)
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
		self.manwinningodds.SetValue(str(self.settings.odds))
		self.manlosingodds.SetValue(str(100 - self.settings.odds))		
		
		oddssizer.AddF(self.manualodds, self.hflag)
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
		
		#need to keep a list of the the IDs of the payouts so we can change them
		gcount = 12
		self.mgIndeces = []
		# the rest don't have anything in the last three columns
		for i in range(2,len(self.payoutodds)):
			self.manualgrid.AddF(wx.StaticText(oddspage, wx.ID_ANY, "Payout " + str(i+1) + ":"), self.bflag)
			gcount += 1
			self.mgIndeces.append(gcount)
			self.manualgrid.AddF(self.payoutodds[i], self.bflag)
			gcount += 1
			self.manualgrid.AddF(percentsign(), self.bflag)
			gcount += 1
			for x in range(0,3):
				self.manualgrid.AddStretchSpacer()
				gcount += 1

		
		oddssizer.AddF(self.manualgrid, self.eflag)
		oddssizer.AddF(wx.StaticLine(oddspage), self.eflag)
		
		# Near misses... made more sense to have its own section, as it's used in both manual and auto
		nearmissrow = wx.BoxSizer(wx.HORIZONTAL)
		nearmissrow.AddF(wx.StaticText(oddspage, wx.ID_ANY, "Near Misses:"), self.bflag)
		nearmissrow.AddF(self.nearmisses, self.bflag)
		nearmissrow.AddF(percentsign(), self.bflag)
		nearmissrow.AddF(self.chance, self.bflag)
		oddssizer.AddF(nearmissrow, self.eflag)
		
		self.SetOdds()

		# Odds page bindings
		self.Bind(wx.EVT_CHECKBOX, self.OnOddsTypeChecked, self.autoodds)
		self.Bind(wx.EVT_CHECKBOX, self.OnOddsTypeChecked, self.manualodds)
		self.Bind(wx.EVT_CHECKBOX, self.OnChanceChecked, self.chance)
		
		#*******************************************
		# 				The Info page
		#*******************************************
		# subject info
		infosizer = wx.BoxSizer(wx.VERTICAL)

		self.collectname = wx.CheckBox(self, wx.ID_ANY, "Name")
		self.collectage = wx.CheckBox(self, wx.ID_ANY, "Age")
		self.collectsex = wx.CheckBox(self, wx.ID_ANY, "Sex")
		self.collecthandedness = wx.CheckBox(self, wx.ID_ANY, "Handedness")
		
		# subjective probability estimate
		self.getprobestimate = wx.CheckBox(self, wx.ID_ANY, "Obtain Subject Probability Estimate")
		self.getprobestimate.SetFont(self.hfont)
		self.estimatetiming = wx.Choice(self, wx.ID_ANY, choices=["At Beginning", "At End"])
		self.estimateinterval = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_RIGHT)
		
		# save as
		self.filenamebox = wx.TextCtrl(self, wx.ID_ANY)
		self.sessionnumbox = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_RIGHT)
		
		# info collection package
		infolabel = wx.StaticText(self, wx.ID_ANY, "Collect Subject Information")
		infolabel.SetFont(self.hfont)
		infosizer.AddF(infolabel, self.hflag)
		infosizer.AddF(self.collectname, self.bflag)
		infosizer.AddF(self.collectage, self.bflag)
		infosizer.AddF(self.collectsex, self.bflag)
		infosizer.AddF(self.collecthandedness, self.bflag)
		infosizer.AddF(wx.StaticLine(self), self.eflag)
		
		# probability estimate stuff
		infosizer.AddF(self.getprobestimate, self.hflag)
		self.probrow = wx.BoxSizer(wx.HORIZONTAL)
		self.probrow.AddF(self.estimatetiming, self.bflag)
		self.probrow.AddF(wx.StaticText(self, wx.ID_ANY, "of every"), self.bflag)
		self.probrow.AddF(self.estimateinterval, self.bflag)
		self.probrow.AddF(wx.StaticText(self, wx.ID_ANY, "rounds"), self.bflag)
		infosizer.AddF(self.probrow, self.eflag)
		infosizer.AddF(wx.StaticLine(self), self.eflag)
		
		# Save as
		saveaslabel = wx.StaticText(self, wx.ID_ANY, "Save As:")
		saveaslabel.SetFont(self.hfont)
		infosizer.AddF(saveaslabel, self.hflag)
		savegrid = wx.FlexGridSizer(2,2)
		savegrid.AddF(wx.StaticText(self, wx.ID_ANY, "Filename:"), self.bflag)
		savegrid.AddF(self.filenamebox, self.eflag)
		savegrid.AddF(wx.StaticText(self, wx.ID_ANY, "Session Number:"), self.bflag)
		savegrid.AddF(self.sessionnumbox, self.eflag)
		infosizer.AddF(savegrid, self.eflag)
		
		# Bind some stuff
		self.Bind(wx.EVT_CHECKBOX, self.OnGetProbEstimate, self.getprobestimate)
		#*******************************************
		# 				Common Elements
		#*******************************************
		
		# Payout table
		self.payoutframe = commongui.PayoutTable(self, self.settings)
		
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
		self.Bind(wx.EVT_BUTTON, self.OnLoad, loadbtn)
		self.Bind(wx.EVT_BUTTON, self.OnSave, savebtn)
		self.Bind(wx.EVT_BUTTON, self.OnOkay, okaybtn)
		self.Bind(wx.EVT_BUTTON, self.OnUpdate, updatebtn)
		self.Bind(wx.EVT_BUTTON, self.OnReset, resetbtn)


		# the outer sizer to pack everything into
		bottomflag = wx.SizerFlags().Align(wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM).Border(wx.ALL, 10).Expand()
		outersizer = wx.FlexGridSizer(3, 1)
		middleSizer = wx.BoxSizer(wx.HORIZONTAL)
		payoutSizer = wx.BoxSizer(wx.VERTICAL)
		payoutSizer.AddF(self.payoutframe, bottomflag)
		payoutSizer.AddF(infosizer, bottomflag)

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

	def UpdateFromSettings(self):
		self.SetBets()
		self.SetSymbols(self.wingrid)
		self.SetOdds()

	def ActivePage(self):
		currentPage = self.book.GetSelection()
		pageName = self.book.GetPageText(currentPage)
		return pageName

	def OnUpdate(self, event):
		if self.ActivePage() == 'Bets':
			self.SetBetSettings()

		elif self.ActivePage() == 'Symbols':
			self.SetSymbolSettings()

		elif self.ActivePage() == 'Odds':
			self.SetOddsSettings()
		
		self.payoutframe.update(self.settings)

	def OnReset(self, event):
		if self.ActivePage() == 'Bets':	
			self.SetBets()

		elif self.ActivePage() == 'Symbols':
			self.SetSymbols(self.wingrid)

		elif self.ActivePage() == 'Odds':
			self.SetOdds()

	def SetBets(self):
		#set the values of the items in the bet tab
		self.debtallowed.SetSelection(self.settings.debt)
		self.roundsentry.SetValue(str(self.settings.rounds))
		self.seedentry.SetValue(str(self.settings.seed))
		while self.wagers:
			self.RemoveWager(self.wagers[0])
			
		for w in self.settings.betsizes:
			w = str(w)
			self.AddWager(w, self.betspage)

	def SetBetSettings(self):
		#sets the values of the bet object based on the gui contents
		debt = self.debtallowed.GetCurrentSelection()
		cindex = self.currencytype.GetCurrentSelection()
		if cindex is 0:
			currency = "c"
		elif cindex is 1:
			currency = "$"
		
		self.settings.seed = int(self.seedentry.GetValue())
		self.settings.rounds = int(self.roundsentry.GetValue())
		betsizes = []
		for w in self.wagers:
			wagertext = w.GetItem(1).GetWindow()
			betsizes.append(float(wagertext.GetLabel().split(' ')[0]))

		self.settings.setBets(betsizes, debt, currency)	

	def SetSymbols(self, wingrid):
		for scb in self.symbolCheckBoxes:
			if scb.cbname in self.settings.symbols:
				scb.SetValue(1)
			else:
				scb.SetValue(0)

		count = 0
		for combo in self.settings.combos:
			for sym in combo:
				wingrid.GetItem(self.comboIndexes[count]).GetWindow().SetStringSelection(sym)
				count+=1
		
		count = 0		

		for p in self.settings.payouts:
			wingrid.GetItem(self.payoutIndexes[count]).GetWindow().SetValue(str(p))
			count+=1

	def SetSymbolSettings(self):
		#sets the values of the symbol object based on the gui contents
		combos = []
		combo = []

		#now get the symbols to be used from the checkboxy thang
		self.settings.symbols = []		
		
		for scb in self.symbolCheckBoxes:
			if scb.GetValue():
				self.settings.symbols.append(scb.cbname)

		for c in self.comboboxes:
			symbol = c.GetValue()
			if len(combo) < 3:
				combo.append(symbol)
			else:
				combos.append(combo)
				combo = [symbol]

		self.settings.combos = combos
		#set the payoffs
		payoffs = []
		for p in self.symbolPayouts:
			payoffs.append(p.GetValue())

		self.settings.payouts = payoffs

	def SetOddsSettings(self):
		#sets value of odds object from gui
		self.settings.odds = int(self.autowinningodds.GetValue())
		self.settings.oddskind = self.autopayout.GetStringSelection()

		manualOdds = []

		for i in self.mgIndeces:
			item = self.manualgrid.GetItem(i)
			manualOdds.append(item.GetWindow().GetValue())

		self.settings.payoutOdds = manualOdds

	def SetOdds(self):
		#sets value of odds gui from odds object
		self.autowinningodds.SetValue(str(self.settings.odds))
		self.autolosingodds.SetValue(str(100 - self.settings.odds))
		self.autopayout.SetStringSelection(self.settings.oddskind)

		#check and see if we have the same number of payouts still
		payoutOdds = self.settings.payoutOdds

		if len(self.mgIndeces) != len(payoutOdds):
			pass

		for i, j in zip(self.mgIndeces, payoutOdds):
			tc = self.manualgrid.GetItem(i).GetWindow()
			tc.SetValue(str(j))
		
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
		try:
			img = img.Scale(cfg.SLOT_SIZE[0], cfg.SLOT_SIZE[1], 1)
		except:
			pass
		bitmap = wx.BitmapFromImage(img)

		bmp = wx.StaticBitmap(parent, wx.ID_ANY, bitmap)
		checkbox = wx.CheckBox(parent, wx.ID_ANY, "")
		checkbox.SetValue(True)
		checkbox.cbname = index
		sizer.AddF(bmp, self.bflag) 
		sizer.AddF(checkbox, self.bflag)
		self.symbolCheckBoxes.append(checkbox)
		return sizer

	def makeBitmap(self, filename):
		img = wx.Image(filename)
		try:
			img = img.Scale(cfg.SLOT_SIZE[0], cfg.SLOT_SIZE[1], 1)
		except:
			pass
		bitmap = wx.BitmapFromImage(img)
		bitmap.SetHeight(cfg.SLOT_SIZE[0])
		bitmap.SetWidth(cfg.SLOT_SIZE[1])
		return bitmap

	def create_winning_combo(self, parent, grid, index, combos, value):
		grid.AddF(wx.StaticText(parent, wx.ID_ANY, "Payout " + str(index) + ":"), self.bflag)
		self.wcount += 1
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
			self.wcount += 1
			self.comboIndexes.append(self.wcount)
		

		tc = wx.TextCtrl(parent, value=str(value))

		self.symbolPayouts.append(tc) 

		grid.AddF(tc, self.bflag)
		self.wcount += 1
		self.payoutIndexes.append(self.wcount)

	
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

	def OnSave(self, event):
		saveDia = wx.FileDialog(self, 'Save your settings', 'settings', self.settings.name, "*.set", wx.FD_SAVE)
		outcome = saveDia.ShowModal()
		if outcome == wx.ID_OK:
			self.settings.name = saveDia.GetPath()
			self.settings.preserve()

	def OnLoad(self, event):
		openDia = wx.FileDialog(self, 'Choose your settings', 'settings', self.settings.name, "*.set", wx.FD_OPEN)
		outcome = openDia.ShowModal()
		if outcome == wx.ID_OK:
			f = open(openDia.GetPath())
			settings = pickle.load(f)
			f.close()
			self.settings = settings
			self.UpdateFromSettings()

		
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
				#infodialog.save_info()
				self.Hide()
				game = gameplay.GamePlayGUI(None, self.settings)
				game.Show()
				self.Destroy()


if __name__ == '__main__':
	app = wx.App(False)
	mainframe = SetupGUI(None)
	#gameplay = gameplay.GamePlayGUI(None)
	app.MainLoop()
