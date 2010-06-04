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
		lflag = wx.SizerFlags().Border(wx.LEFT, 10)

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
		betssizer.AddF(roundslabel, lflag)
		numroundsbox = wx.BoxSizer(wx.HORIZONTAL)
		numroundsbox.AddF(self.roundsentry, self.bflag)
		numroundsbox.AddF(wx.StaticText(betspage, wx.ID_ANY, "Subject Debt:"), self.bflag)
		numroundsbox.AddF(self.debtallowed, self.bflag)
		betssizer.AddF(numroundsbox, self.bflag)
		betssizer.AddF(wx.StaticLine(betspage), self.eflag)

		# the currency stuff
		currencylabel = wx.StaticText(betspage, wx.ID_ANY, "Currency:")
		currencylabel.SetFont(hfont)
		betssizer.AddF(currencylabel, lflag)
		currencybox = wx.BoxSizer(wx.HORIZONTAL)
		currencybox.AddF(wx.StaticText(betspage, wx.ID_ANY, "Seed Amount:"), self.bflag)
		currencybox.AddF(self.seedentry, self.bflag)
		currencybox.AddF(self.currencytype, self.bflag)
		betssizer.AddF(currencybox, self.bflag)
		betssizer.AddF(wx.StaticLine(betspage), self.eflag)

		# the wager stuff
		wagerlabel = wx.StaticText(betspage, wx.ID_ANY, "Wagers:")
		wagerlabel.SetFont(hfont)
		betssizer.AddF(wagerlabel, lflag)
		wagerbox = wx.BoxSizer(wx.HORIZONTAL)
		wagerbox.AddF(self.wagernum, self.bflag)
		wagerbox.AddF(wx.StaticText(betspage, wx.ID_ANY, "Amount:"), self.bflag)
		wagerbox.AddF(self.amountentry, self.bflag)
		wagerbox.AddF(self.addbtn, self.bflag)
		betssizer.AddF(wagerbox, self.bflag)
		betssizer.AddF(self.wagertable, self.eflag)

		#*******************************************
		# 				The Symbols page
		#*******************************************
		self.autoselect = wx.CheckBox(symbolspage, wx.ID_ANY, "Autoselect")

		# Visible types of symbols
		symbolslabel = wx.StaticText(symbolspage, wx.ID_ANY, "Visible Types of Symbols")
		symbolslabel.SetFont(hfont)
		symbolssizer.AddF(symbolslabel, lflag)
		symbolsbox = wx.BoxSizer(wx.HORIZONTAL)
		for i in range (0, len(cfg.symbols)):
			symbolsbox.AddF(self.create_symbols_checkbox(symbolspage, i), self.bflag)
		symbolssizer.AddF(symbolsbox, self.bflag)
		symbolssizer.AddF(wx.StaticLine(symbolspage), self.bflag)

		# Winning Combinations
		comboslabel = wx.StaticText(symbolspage, wx.ID_ANY, "Winning Combinations")
		comboslabel.SetFont(hfont)
		symbolssizer.AddF(comboslabel, lflag)
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
		self.autopercent = wx.TextCtrl(oddspage, wx.ID_ANY, style=wx.TE_RIGHT)
		self.autopayout = wx.Choice(oddspage, wx.ID_ANY, choices=["Equal Odds", "Casino Odds", "Linear Odds"])
		
		# Manual
		self.manualodds = wx.CheckBox(oddspage, wx.ID_ANY, "Manual Odds")
		self.manualodds.SetFont(hfont)
		
		# Near Misses
		self.nearmisses = wx.TextCtrl(oddspage, wx.ID_ANY, style=wx.TE_RIGHT)
		self.chance = wx.CheckBox(oddspage, wx.ID_ANY, "Chance")
		
		# Pack together the auto stuff
		oddssizer.AddF(self.autoodds, lflag)
		autogrid = wx.FlexGridSizer(3, 3)
		autogrid.AddF(wx.StaticText(oddspage, wx.ID_ANY, "Overall Odds of Winning:"), self.bflag)
		autogrid.AddF(self.autopercent, self.bflag)
		autogrid.Add(wx.StaticText(oddspage, wx.ID_ANY, "%"))
		autogrid.AddF(wx.StaticText(oddspage, wx.ID_ANY, "Overall Odds of Losing:"), self.bflag)
		autogrid.AddF(wx.StaticText(oddspage, wx.ID_ANY, "100"), self.bflag.Align(wx.ALIGN_RIGHT))
		autogrid.Add(wx.StaticText(oddspage, wx.ID_ANY, "%"))
		oddssizer.AddF(autogrid, self.eflag)
		oddssizer.AddF(self.manualodds, lflag)
		
		
		
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
		outersizer.AddF(payoutlabel, lflag.Border(wx.LEFT, 15))
		outersizer.AddF(payoutframe, self.bflag)
		outersizer.AddF(buttonsizer, self.bflag)

		# Bindings, woot
		self.Bind(wx.EVT_BUTTON, self.OnAddWager, self.addbtn)
		self.Bind(wx.EVT_CHOICE, self.OnChooseWager, self.wagernum)

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

if __name__ == '__main__':
    app = wx.App(False)
    mainframe = SetupGUI(None)
    app.MainLoop()
