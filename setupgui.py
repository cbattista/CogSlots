#!/usr/bin/env python

import sys
import wx, wx.combo, wx.lib.scrolledpanel
import cfg
import copy
import commongui
from commongui import makeBitmap
import gameplay
import subjectinfo
from Settings import Settings
import pickle
from SlotReels import Slots
import Shuffler
import random

class SetupGUI(wx.Frame):
	""" The interface for the tester to set up parameters """
	def __init__(self, parent, *args, **kwargs):
		# create the parent class
		wx.Frame.__init__(self, parent, *args, **kwargs)

		#self.FRAME_SIZE = (750, 600)

		self.settings = Settings()

		# the notebook
		#nbW = self.FRAME_SIZE[0]
		#nbH = self.FRAME_SIZE[1] * 0.9
		#self.nbH = nbH
		#self.nbW = nbW
		self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
		self.book = wx.Notebook(self, wx.ID_ANY)

		betspage, betssizer = self.create_page('Bets')
		self.betspage = betspage
		self.betssizer = betssizer
		symbolpage, symbolsizer = self.create_page('Symbols')
		#self.oddpage, self.oddsizer = self.create_page('Odds')
		infopage, infosizer = self.create_page('Info')
		self.infopage = infopage

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
		self.debtallowed = wx.CheckBox(betspage, wx.ID_ANY, "Allow subject debt")

		# Wagers
		self.wagernum = wx.Choice(betspage, wx.ID_ANY, choices=["New"])
		self.amountentry = wx.TextCtrl(betspage, wx.ID_ANY, style=wx.TE_RIGHT)
		self.addbtn = wx.Button(betspage, wx.ID_ANY, "Add")
		self.wagertable = wx.StaticBoxSizer(wx.StaticBox(betspage), wx.VERTICAL)
		self.wagerrows = []

		# number of rounds stuff
		roundslabel = wx.StaticText(betspage, wx.ID_ANY, "Number of Rounds:")
		roundslabel.SetFont(self.hfont)
		betssizer.AddF(roundslabel, self.hflag)
		numroundsbox = wx.BoxSizer(wx.HORIZONTAL)
		numroundsbox.AddF(self.roundsentry, self.bflag)
		debtlabel = wx.StaticText(betspage, wx.ID_ANY, "Subject Debt:")
		debtlabel.SetFont(self.hfont)
		betssizer.AddF(numroundsbox, self.bflag)
		
		#numroundsbox.AddF(debtlabel, self.bflag)
		#numroundsbox.AddF(self.debtallowed, self.bflag)
		betssizer.AddF(debtlabel, self.bflag)
		betssizer.AddF(self.debtallowed, self.bflag)
		betssizer.AddF(wx.StaticLine(betspage), self.eflag)

		# the currency stuff
		currencylabel = wx.StaticText(betspage, wx.ID_ANY, "Currency:")
		currencylabel.SetFont(self.hfont)
		betssizer.AddF(currencylabel, self.hflag)
		self.currencytype = wx.Choice(betspage, wx.ID_ANY, choices=["Credits", "$"])
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
		choices = []
		for i in range(1,11):
			choices.append(str(i))
		
		pbox = wx.BoxSizer(wx.HORIZONTAL)
		pbox.AddF(wx.StaticText(symbolpage, wx.ID_ANY, "Number of Winning Combinations:"), self.bflag)
		self.pCtrl = wx.Choice(symbolpage, wx.ID_ANY, choices=choices)
		pbox.AddF(self.pCtrl, self.bflag)
		symbolsizer.AddF(pbox, self.bflag)
		
		rbox = wx.BoxSizer(wx.HORIZONTAL)
		rbox.AddF(wx.StaticText(symbolpage, wx.ID_ANY, "Number of Reels:"), self.bflag)
		self.rCtrl = wx.Choice(symbolpage, wx.ID_ANY, choices=choices)
		rbox.AddF(self.rCtrl, self.bflag)
		symbolsizer.AddF(rbox, self.bflag)
		symbolsizer.AddF(wx.StaticLine(symbolpage), self.eflag)
		
		symbolslabel = wx.StaticText(symbolpage, wx.ID_ANY, "Select Symbols:")
		symbolslabel.SetFont(self.hfont)
		symbolsizer.AddF(symbolslabel, self.hflag)
		
		symsizer = wx.BoxSizer(wx.HORIZONTAL)

		self.symboxes = []
		
		for s in self.settings.symbols:
			if s != cfg.IM_EMPTY:
				checkbox = wx.CheckBox(symbolpage, wx.ID_ANY, "")
				#checkbox.SetValue(True)
				checkbox.cbname = s
				self.symboxes.append(checkbox)
				checkSizer = wx.BoxSizer(wx.VERTICAL)
				checkSizer.Add(wx.StaticBitmap(symbolpage, -1, makeBitmap(s, [16, 16])), 1)
				checkSizer.Add(checkbox, 1)
				symsizer.AddF(checkSizer, self.bflag)
		
		symbolsizer.AddF(symsizer, self.bflag)
		self.SetSymbols()
		symbolpage.SetSizerAndFit(symbolsizer)
				
		#*******************************************
		# 				The Info page
		#*******************************************
		
		# Payout table
		self.payoutframe = commongui.PayoutTable(infopage, self.settings)
		self.payoutSizer = wx.BoxSizer(wx.VERTICAL)
		self.payoutSizer.Add(self.payoutframe)
		infosizer.Add(self.payoutSizer)

		# subject info		
		self.collectname = wx.CheckBox(infopage, wx.ID_ANY, "Name")
		self.collectage = wx.CheckBox(infopage, wx.ID_ANY, "Age")
		self.collectsex = wx.CheckBox(infopage, wx.ID_ANY, "Sex")
		self.collecthandedness = wx.CheckBox(infopage, wx.ID_ANY, "Handedness")
		
		self.showpayouts = wx.CheckBox(infopage, wx.ID_ANY, "Show Payouts Table During Gameplay?")
		
		# subjective probability estimate
		self.getprobestimate = wx.CheckBox(infopage, wx.ID_ANY, "Obtain Subject Probability Estimate")
		self.getprobestimate.SetFont(self.hfont)
		self.estimatetiming = wx.Choice(infopage, wx.ID_ANY, choices=["beginning", "end"])
		self.estimateinterval = wx.TextCtrl(infopage, wx.ID_ANY, style=wx.TE_RIGHT)
		
		# save as
		self.filenamebox = wx.TextCtrl(infopage, wx.ID_ANY)
		self.sessionnumbox = wx.TextCtrl(infopage, wx.ID_ANY, style=wx.TE_RIGHT)
		
		# info collection package
		infolabel = wx.StaticText(infopage, wx.ID_ANY, "Collect Subject Information")
		infolabel.SetFont(self.hfont)
		infosizer.AddF(infolabel, self.hflag)
		infosizer.AddF(self.collectname, self.bflag)
		infosizer.AddF(self.collectage, self.bflag)
		infosizer.AddF(self.collectsex, self.bflag)
		infosizer.AddF(self.collecthandedness, self.bflag)
		infosizer.AddF(wx.StaticLine(self), self.eflag)
		infosizer.AddF(self.showpayouts, self.eflag)
		infosizer.AddF(wx.StaticLine(self), self.eflag)
		
		# probability estimate stuff
		infosizer.AddF(self.getprobestimate, self.hflag)
		self.pBox = wx.BoxSizer(wx.VERTICAL)
		self.probrow = wx.BoxSizer(wx.HORIZONTAL)
		self.probrow.AddF(self.estimatetiming, self.bflag)
		self.probrow.AddF(wx.StaticText(infopage, wx.ID_ANY, "of every"), self.bflag)
		self.probrow.AddF(self.estimateinterval, self.bflag)
		self.probrow.AddF(wx.StaticText(infopage, wx.ID_ANY, "rounds"), self.bflag)
		self.pBox.AddF(self.probrow, self.bflag)
		self.mrow = wx.BoxSizer(wx.HORIZONTAL)
		self.mrow.AddF(wx.StaticText(infopage, wx.ID_ANY, "Message:"), self.bflag)
		self.probText = wx.TextCtrl(infopage, wx.ID_ANY, "")
		self.mrow.AddF(self.probText, self.bflag)
		self.pBox.AddF(self.mrow, self.bflag)
		infosizer.AddF(self.pBox, self.eflag)
		infosizer.AddF(wx.StaticLine(infopage), self.eflag)
		
		# Save as
		saveaslabel = wx.StaticText(infopage, wx.ID_ANY, "Save As:")
		saveaslabel.SetFont(self.hfont)
		infosizer.AddF(saveaslabel, self.hflag)
		savegrid = wx.FlexGridSizer(2,2)
		savegrid.AddF(wx.StaticText(infopage, wx.ID_ANY, "Filename:"), self.bflag)
		savegrid.AddF(self.filenamebox, self.eflag)
		savegrid.AddF(wx.StaticText(infopage, wx.ID_ANY, "Session Number:"), self.bflag)
		savegrid.AddF(self.sessionnumbox, self.eflag)
		infosizer.AddF(savegrid, self.eflag)
		
		infopage.SetSizerAndFit(infosizer)
		
		self.SetInfo()
		

		#*******************************************
		# 				The Odds page
		#*******************************************		
		
		self.makeOddsTab()

		#*******************************************
		# 				Common Elements
		#*******************************************
				
		# Buttons
		buttonsizer = wx.BoxSizer(wx.HORIZONTAL)
		updatebtn = wx.Button(self, wx.ID_ANY, 'Update')
		resetbtn = wx.Button(self, wx.ID_ANY, 'Reset')
		loadbtn = wx.Button(self, wx.ID_OPEN)
		savebtn = wx.Button(self, wx.ID_SAVE)
		#cancelbtn = wx.Button(self, wx.ID_CANCEL)
		okaybtn = wx.Button(self, wx.ID_OK)
		buttonsizer.AddF(updatebtn, self.bflag)
		buttonsizer.AddF(resetbtn, self.bflag)
		buttonsizer.AddF(loadbtn, self.bflag)
		buttonsizer.AddF(savebtn, self.bflag)
		#buttonsizer.AddF(cancelbtn, self.bflag)
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

		middleSizer.AddF(self.book, wx.SizerFlags(1).Expand())
		
		#midSize = (self.FRAME_SIZE[0] * 0.9, self.FRAME_SIZE[1] * 0.9)
		#middleSizer.SetMinSize(midSize)

		outersizer.AddF(middleSizer, bottomflag)
		outersizer.AddF(buttonsizer, bottomflag)

		self.SetSizerAndFit(outersizer)
		#self.SetSize(self.FRAME_SIZE)
		self.Show(True)


#	def OnEditText(self, event):
		#self.setBets()

	#******************************************
	#				Settings Tab Getters and Setters
	#******************************************
	
	def makeOddsTab(self):		
		if self.book.GetPageCount() == 4:
			self.book.DeletePage(3)
		
		oddpage, oddsizer = self.create_page('Odds')
		
		oddGrid = wx.FlexGridSizer(cols=1, vgap=5)
		
		weightLabel = wx.StaticText(oddpage, -1, "Symbol Weights")
		weightLabel.SetFont(self.hfont)
		oddsLabel = wx.StaticText(oddpage, -1, "Winning Combos")
		oddsLabel.SetFont(self.hfont)
				
		oddGrid.Add(weightLabel)
		text = wx.StaticText(oddpage, -1, cfg.WEIGHTS_TEXT)
		#text.Wrap(self.GetSize()[0] * .9)
		oddGrid.Add(text)
		
		self.nearMisses = []
		self.nearMissOdds = []
		cflag = wx.SizerFlags().Align(wx.ALIGN_CENTER_HORIZONTAL)
		
		#create top half
		self.weights = []
		weightSizer = wx.GridSizer(cols=self.settings.numReels+2, rows=len(self.settings.visibleSymbols))
		weightSizer.AddF(wx.StaticText(oddpage, -1, "Symbol"), cflag)
		for r in range(self.settings.numReels):
			text = "Reel %s" % (r + 1)
			weightSizer.AddF(wx.StaticText(oddpage, -1, text), cflag)
		weightSizer.AddF(wx.StaticText(oddpage, -1, "Blank Pad"), cflag)

		for s in self.settings.visibleSymbols:
			w = []
			
			weightSizer.AddF(wx.StaticBitmap(oddpage, -1, makeBitmap(s, cfg.SLOT_SIZE)), cflag)
			for r in range(self.settings.numReels):
				ctrl = wx.SpinCtrl(oddpage, -1, min=0, initial=1, size=cfg.CTRL_SIZE)
				w.append(ctrl)
				weightSizer.AddF(ctrl, cflag)
				
			nmctrl = wx.SpinCtrl(oddpage, -1, min=0, initial=0, size=cfg.CTRL_SIZE)
			weightSizer.AddF(nmctrl, cflag)
			self.nearMisses.append(nmctrl)
				
			self.weights.append(w)

		oddGrid.Add(weightSizer)
			
		#oddsizer.Add(wx.Button(oddpage, -1, "Update Reels"))
		
		oddGrid.Add(oddsLabel)
		text = wx.StaticText(oddpage, -1, cfg.COMBOS_TEXT)
		#text.Wrap(self.nbW * .95)
		oddGrid.Add(text)
		#create bottom half
		self.odds = []
		self.allCombos = []
		self.payoffs = []
		
		self.gfBox = wx.CheckBox(oddpage, -1, "Employ Gambler's Fallacy")
		oddGrid.Add(self.gfBox)
		self.overBox = wx.CheckBox(oddpage, -1, "Override True Reel Odds")
		oddGrid.Add(self.overBox)
		
		
		comboSizer = wx.GridSizer(rows=len(self.settings.payouts) + 1, cols=self.settings.numReels+4)
		
		comboSizer.Add(wx.StaticText(oddpage, -1, "Payout"))
		for r in range(self.settings.numReels):
			text = "Reel %s" % (r+1)
			comboSizer.Add(wx.StaticText(oddpage, -1, text))
		comboSizer.AddF(wx.StaticText(oddpage, -1, "Odds (%)"), cflag)
		comboSizer.AddF(wx.StaticText(oddpage, -1, "Odds\n Override"), cflag)
		comboSizer.AddF(wx.StaticText(oddpage, -1, "Miss Override %"), cflag)
		
		self.overrides = []
		
		for p in range(self.settings.numPayouts):
			o = []
			pctrl = wx.SpinCtrl(oddpage, -1, min=0, initial=0, size=cfg.CTRL_SIZE)
			self.payoffs.append(pctrl)
			comboSizer.Add(pctrl)
			#make symbol combo boxes
			combos = []
			for c in range(self.settings.numReels):
				combo = wx.combo.BitmapComboBox(oddpage, size=(45, -1))
				symbols = self.settings.visibleSymbols
				for i in range (0, len(symbols)):
					combo.Append(symbols[i], makeBitmap(symbols[i], scale=cfg.SLOT_SIZE))
				combo.Append(cfg.IM_EMPTY, makeBitmap(cfg.IM_EMPTY, scale=cfg.SLOT_SIZE))
				combo.SetSelection(i)
				combos.append(combo)
				comboSizer.Add(combo)
				
			self.allCombos.append(combos)
			oddsText = wx.TextCtrl(oddpage, -1, "100", style=wx.TE_READONLY, size=cfg.CTRL_SIZE)
			override = wx.SpinCtrl(oddpage, -1, min=0, initial=0, size=cfg.CTRL_SIZE)
			comboSizer.Add(oddsText)
			comboSizer.Add(override)
			nmoctrl = wx.SpinCtrl(oddpage, -1, min=0, initial=0, size=cfg.CTRL_SIZE)
			comboSizer.Add(nmoctrl)
			self.nearMissOdds.append(nmoctrl)

			self.odds.append(oddsText)
			self.overrides.append(override)
		
		#SUMMARY INFORMATION
		summaryGrid = wx.BoxSizer(wx.HORIZONTAL)
		
		#odds
		totalOddsText = wx.StaticText(oddpage, -1, "Total Odds of a Win (%):")
		self.totalOdds = wx.TextCtrl(oddpage, -1, "100", style=wx.TE_READONLY, size=cfg.CTRL_SIZE)
		oddGrid.Add(comboSizer)
		summaryGrid.Add(totalOddsText)
		summaryGrid.Add(self.totalOdds)
		summaryGrid.Add(wx.StaticText(oddpage, -1, "Near Miss Odds:"))
		self.nmOdds = wx.TextCtrl(oddpage, -1, "0", style=wx.TE_READONLY, size=cfg.CTRL_SIZE)
		summaryGrid.Add(self.nmOdds)
		
		#max and min payouts
		summaryGrid.Add(wx.StaticText(oddpage, -1, "Max Payout:"))
		self.maxPay = wx.TextCtrl(oddpage, -1, "0", style=wx.TE_READONLY, size=cfg.CTRL_SIZE)
		summaryGrid.Add(self.maxPay)
		summaryGrid.Add(wx.StaticText(oddpage, -1, "Min Payout:"))
		self.minPay = wx.TextCtrl(oddpage, -1, "0", style=wx.TE_READONLY, size=cfg.CTRL_SIZE)
		summaryGrid.Add(self.minPay)
		
		
		oddGrid.AddF(wx.StaticLine(oddpage), self.eflag)
		oddGrid.Add(summaryGrid)
		
		oddsizer.Add(oddGrid)
		self.Bind(wx.EVT_COMBOBOX, self.onComboSelect)

		self.Bind(wx.EVT_CHECKBOX, self.onSpin)
		self.Bind(wx.EVT_SPINCTRL, self.onSpin)

		
		oddpage.SetSizerAndFit(oddsizer)
		self.SetOdds()
		self.makeReels()
		self.updateOdds()
		oddpage.SetupScrolling()
		oddpage.Refresh()
		oddpage.Update()
	
	def UpdateFromSettings(self):
		self.SetInfo()
		self.SetBets()
		self.SetSymbols()
		self.makeOddsTab()
		self.SetOdds()

	def ActivePage(self):
		currentPage = self.book.GetSelection()
		pageName = self.book.GetPageText(currentPage)
		return pageName

	def OnUpdate(self, event):
		self.SetCursor(wx.StockCursor(wx.CURSOR_WAIT))

		self.SetInfoSettings()
		self.SetBetSettings()
		self.SetSymbolSettings()
						
		if self.ActivePage() == 'Symbols':
			self.makeOddsTab()

		self.updateOdds()
		
		self.payoutSizer.Hide(self.payoutframe)
		self.payoutSizer.Remove(self.payoutframe)
		self.payoutSizer.Layout()
		self.payoutframe = commongui.PayoutTable(self.infopage, self.settings)
		self.payoutSizer.InsertF(0, self.payoutframe, wx.SizerFlags().Align(wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM).Border(wx.ALL, 10).Expand())
		self.payoutSizer.Layout()
		
		self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))

		#determine 
		if self.settings.gamblersFallacy:
			ratio = []

			if not self.settings.override['engage']:
				for o in self.odds:
					amount = float(o.GetValue()) * self.settings.rounds / 100.
					ratio.append(int(amount))
			else:
				for o in self.settings.override['odds']:
					amount = o * self.settings.rounds / 100.
					ratio.append(int(amount))				
				
			nearMisses = []
			items = self.settings.combos

			for nmo, c in zip(self.nearMissOdds, self.settings.combos):
				if nmo.GetValue():
					newC = copy.deepcopy(c)
					blankIndex = random.choice([0,1,2])
					newC[blankIndex] = cfg.IM_BLANK
					amount = float(nmo.GetValue()) * self.settings.rounds / 100.
					ratio.append(int(amount))
					items.append(newC)
			
			losses = self.settings.rounds - sum(ratio)
			items = items + ["LOSS"]
			ratios = ratio + [losses]			
			
			print items
			print ratios
						
			shuffler = Shuffler.Shuffler(items, self.settings.rounds, self.settings.rounds, ratios)
			self.settings.stimList = shuffler.shuffleIt()
		
			

		
	def OnReset(self, event):
		if self.ActivePage() == 'Bets':	
			self.SetBets()

		elif self.ActivePage() == 'Symbols':
			self.SetSymbols()

		elif self.ActivePage() == 'Odds':
			self.updateOdds()
	
		elif self.ActivePage() == 'Info':
			self.SetInfo()

	
	def SetInfo(self):
		#set the values of the info items (prob est, sub info, etc...)
		probDict = self.settings.probDict
		
		self.getprobestimate.SetValue(probDict['obtain'])
		self.probText.SetValue(probDict['msg'])
		self.estimateinterval.SetValue(str(probDict['interval']))
		
		if probDict['when']:
			self.estimatetiming.SetStringSelection(probDict['when'])

		self.showpayouts.SetValue(self.settings.showPayouts)
		self.filenamebox.SetValue(self.settings.saveAs)
		self.sessionnumbox.SetValue(str(self.settings.session))
		
		d = self.settings.subInfo
		
		self.collectname.SetValue(d["Name"])
		self.collectage.SetValue(d["Age"])
		self.collecthandedness.SetValue(d["Handedness"])
		self.collectsex.SetValue(d["Sex"])
		
	def SetInfoSettings(self):
		self.settings.probDict['obtain'] = self.getprobestimate.GetValue()
		self.settings.probDict['when'] = self.estimatetiming.GetStringSelection()
		self.settings.probDict['msg'] = self.probText.GetValue()
		if self.estimateinterval.GetValue():
			self.settings.probDict['interval'] = int(self.estimateinterval.GetValue())
			
		self.settings.showPayouts = self.showpayouts.GetValue()
		self.settings.session = self.sessionnumbox.GetValue()
		self.settings.saveAs = self.filenamebox.GetValue()
		
		d = {}
		d["Name"] = self.collectname.GetValue()
		d["Age"] = self.collectage.GetValue()
		d["Sex"] = self.collectsex.GetValue()
		d["Handedness"] = self.collecthandedness.GetValue()
		self.settings.subInfo = d
		
			
	def SetBets(self):
		#set the values of the items in the bet tab
		self.debtallowed.SetValue(self.settings.debt)
		self.roundsentry.SetValue(str(self.settings.rounds))
		self.seedentry.SetValue(str(self.settings.seed))
		self.currencytype.SetStringSelection(self.settings.currency)
		while self.wagerrows:
			self.RemoveWager(self.wagerrows[0])
			
		for w in self.settings.betsizes:
			w = str(w)
			self.AddWager(w, self.betspage)

	def SetBetSettings(self):
		#sets the values of the bet object based on the gui contents
		debt = self.debtallowed.GetValue()
		currency = self.currencytype.GetStringSelection()
		#if cindex is 0:
		#	currency = "c"
		#elif cindex is 1:
		#	currency = "$"
			
		
		self.settings.seed = commongui.StringToType(self.seedentry.GetValue())
		self.settings.rounds = int(self.roundsentry.GetValue())
		betsizes = []
		for w in self.wagerrows:
			wagertext = w.GetItem(1).GetWindow()
			betsizes.append(commongui.StringToType(wagertext.GetLabel().split(' ')[0]))

		self.settings.setBets(betsizes, debt, currency)	

	def SetSymbols(self):
		for scb in self.symboxes:
			if scb.cbname in self.settings.visibleSymbols:
				scb.SetValue(1)
			else:
				scb.SetValue(0)

		self.pCtrl.SetSelection(self.settings.numPayouts-1)
		self.rCtrl.SetSelection(self.settings.numReels-1)
		

	def SetSymbolSettings(self):
		#now get the symbols to be used from the checkboxy thang
		self.settings.visibleSymbols = []		
		
		for scb in self.symboxes:
			if scb.GetValue():
				self.settings.visibleSymbols.append(scb.cbname)
				
		self.settings.numPayouts = self.pCtrl.GetSelection() + 1
		self.settings.numReels = self.rCtrl.GetSelection() + 1

		
	def SetOdds(self):

		#if the reels exist, get their weights...
		if "slots" in dir(self.settings):	
			slotweights = self.settings.slots.getWeights()
			for w, sw in zip(self.weights, slotweights):
				for ww, sww in zip(w, sw):
					ww.SetValue(sww)
		
		for p, sp in zip(self.payoffs, self.settings.payouts):
			p.SetValue(sp)
		
		for c, sc, pad, spad in zip(self.allCombos, self.settings.combos, self.nearMisses, self.settings.pads):
			for cc, ssc in zip(c, sc):
				cc.SetStringSelection(ssc)
			pad.SetValue(spad)	
			
		for o, oo in zip(self.overrides, self.settings.override['odds']):
			o.SetValue(oo)

		for nm, nmo in zip(self.nearMissOdds, self.settings.override['nearMiss']):
			nm.SetValue(nmo)
			
		self.gfBox.SetValue(self.settings.gamblersFallacy)
		self.overBox.SetValue(self.settings.override['engage'])
		
		self.makeReels()

		self.minPay.SetValue(str(self.settings.getMinPay()))
		self.maxPay.SetValue(str(self.settings.getMaxPay()))
	
				

	def makeReels(self):
		reels = {}
		for s in self.settings.visibleSymbols:
			weights = self.weights[self.settings.visibleSymbols.index(s)]
			for w in weights:
				k = str(weights.index(w))
				if reels.has_key(k):
					reels[k][s] = w.GetValue()
				else:
					reels[k] = {s : w.GetValue()}
		
		nms = {}
		for s, nm in zip(self.settings.visibleSymbols, self.nearMisses):
			nms[s] = nm.GetValue()
		
		
		self.settings.slots = Slots(reels, self.settings.visibleSymbols, nms)				
		self.updateOdds()		

	def updateOdds(self):

		self.settings.gamblersFallacy = self.gfBox.GetValue()
		self.settings.override['engage'] = self.overBox.GetValue()
				
		overrides = []
		nearMisses = []
		
		for o, nmo in zip(self.overrides, self.nearMissOdds):
			overrides.append(o.GetValue())
			nearMisses.append(nmo.GetValue())
			
		self.settings.override['odds'] = overrides
		self.settings.override['nearMiss'] = nearMisses
		
		payoffs = []
		for p in self.payoffs:
			payoffs.append(p.GetValue())
			
		self.settings.payouts = payoffs
		
		total=0
		setOdds = []
		self.settings.combos = []
		self.settings.pads = []
		
		for combo, nm in zip(self.allCombos, self.nearMissOdds):
			self.settings.pads.append(nm.GetValue())
			c = []
			for com in combo:
				c.append(com.GetStringSelection())
			odds = self.settings.slots.getComboOdds(c)
			self.settings.combos.append(c)
			setOdds.append(odds)
			i = self.allCombos.index(combo)
			odds = odds * 100.0
			total+=odds
			
			odds = str(round(odds, 2))
			self.odds[i].SetValue(odds)		
						
		self.settings.odds = setOdds	
		
		if self.settings.override['engage']:
			total = sum(self.settings.override['odds'])
	
		if total > 100:
			total = 100.
		total = str(round(total, 2))
	
		self.totalOdds.SetValue(total)
		if self.settings.override['engage']:
			nm = sum(self.settings.override['nearMiss'])
		else:
			nm = round(self.settings.slots.getNearMissOdds() * 100., 2)
		self.nmOdds.SetValue(str(nm))

		self.minPay.SetValue(str(self.settings.getMinPay()))
		self.maxPay.SetValue(str(self.settings.getMaxPay()))
	
	def onSpin(self, event):
		self.makeReels()
		
	def onComboSelect(self, event):
		self.updateOdds()
			
	#*******************************************
	# 				Helper Functions
	#*******************************************
	def create_page(self, name):
		page = wx.lib.scrolledpanel.ScrolledPanel(self.book)
		self.book.AddPage(page, name)
		sizer = wx.BoxSizer(wx.VERTICAL)
		page.SetSizer(sizer)
		#page.SetClientSizeWH(self.nbW, self.nbH)
		if name !="Odds":
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
			grid.Add(combo, 0)
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
		parent.FitInside()
	#*******************************************
	# 				Wager Callbacks
	#*******************************************
	def AddWager(self, wager, parent):
		index = len(self.wagerrows)
		deletebtn = wx.Button(parent, wx.ID_ANY, "Delete")
		self.Bind(wx.EVT_BUTTON, self.OnDeleteWager, deletebtn)
		self.wagernum.Append(str(index+1))
		# create the new sizer
		row = wx.BoxSizer(wx.HORIZONTAL)
		row.AddF(wx.StaticText(parent, wx.ID_ANY, "Wager " + str(index+1) + ":"), self.bflag)
		row.AddF(wx.StaticText(parent, wx.ID_ANY, wager + " " + self.currencytype.GetStringSelection()), self.bflag)
		row.AddF(deletebtn, self.bflag)
		self.wagerrows.append(row)
		self.wagertable.AddF(row, self.bflag)
		parent.Refresh()
		parent.Update()
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
		for wager in self.wagerrows:
			if wager.GetItem(2).GetWindow() is event.GetEventObject():
				break

		self.RemoveWager(wager)
		
	
	def OnEditWager(self, event, index):
		wagertext = self.wagerrows[index].GetItem(1).GetWindow()
		wagertext.SetLabel(self.amountentry.GetValue() + " " + self.currencytype.GetStringSelection())
		self.update_wagers()

	def RemoveWager(self, wager):
		index = self.wagerrows.index(wager)
		self.wagertable.Hide(self.wagerrows[index])
		self.wagerrows[index].DeleteWindows()
		del self.wagerrows[index]
		self.wagernum.Delete(index+1)

		# fix the wager numbering
		i = 1
		for wager in self.wagerrows:
			number = wager.GetItem(0).GetWindow()
			number.SetLabel("Wager " + str(i) + ":")

			self.wagernum.SetString(i, str(i))

			i += 1
		self.update_wagers()

	def OnSave(self, event):
		saveDia = wx.FileDialog(self, 'Save your settings', 'settings', self.settings.name, "*.set", wx.FD_SAVE)
		outcome = saveDia.ShowModal()
		if outcome == wx.ID_OK:
			name = saveDia.GetPath()
			#HACKY TIME
			count = name.count(".set") 
			if count > 1:
				name = name.replace(".set", "", count - 1)
				
			self.settings.name = name
			
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
			self.Hide()
			if self.collectname.IsChecked() or self.collectage.IsChecked() or self.collectsex.IsChecked() or self.collecthandedness.IsChecked():
				infodialog = subjectinfo.SubjectInfoDialog(self, "Subject Info")
				infodialog.enable_control("Name", self.collectname.IsChecked())
				infodialog.enable_control("Age", self.collectage.IsChecked())
				infodialog.enable_control("Sex", self.collectsex.IsChecked())
				infodialog.enable_control("Handedness", self.collecthandedness.IsChecked())
				ans2 = infodialog.ShowModal()
				if ans2 == wx.ID_SAVE:
					#infodialog.save_info()
					infodialog.save_info()
					infodialog.cogsub.expname = self.settings.saveAs
					infodialog.cogsub.session = self.settings.session
					game = gameplay.GamePlayGUI(None, self.settings, infodialog.cogsub)
				else:
					self.Show()
					return
			else:
				game = gameplay.GamePlayGUI(None, self.settings, None)
			
			game.Show()
			self.Destroy()


if __name__ == '__main__':
	app = wx.App(False)
	mainframe = SetupGUI(None, title="CogSlots", pos =wx.Point(0,0))
	#gameplay = gameplay.GamePlayGUI(None)
	app.MainLoop()
