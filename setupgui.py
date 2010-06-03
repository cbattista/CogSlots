#!/usr/bin/env python

import sys
import wx, wx.html
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
		self.bflag = wx.SizerFlags().Border(wx.ALL, 5).Expand()
		lflag = wx.SizerFlags().Border(wx.LEFT, 10).Expand()
		
		#*******************************************
		# 				The bets page
		#*******************************************
		# Number of rounds
		roundsentry = wx.TextCtrl(betspage, wx.ID_ANY, style=wx.TE_RIGHT)
		debtallowed = wx.Choice(betspage, wx.ID_ANY, choices=["Allowed", "Not Allowed"])
		
		# Currency
		seedentry = wx.TextCtrl(betspage, wx.ID_ANY, style=wx.TE_RIGHT)
		self.currencytype = wx.Choice(betspage, wx.ID_ANY, choices=["Credits", "Dollars"])
		
		# Wagers
		self.wagernum = wx.Choice(betspage, wx.ID_ANY, choices=["New"])
		self.amountentry = wx.TextCtrl(betspage, wx.ID_ANY, style=wx.TE_RIGHT)
		self.addbtn = wx.Button(betspage, wx.ID_ANY, "Add")
		self.wagertable = wx.StaticBoxSizer(wx.StaticBox(betspage), wx.VERTICAL)
		self.wagers = []

		#*******************************************
		# 				Common Elements
		#*******************************************
		# Payout table
		payoutframe = wx.StaticBoxSizer(wx.StaticBox(self), wx.VERTICAL)
		self.payouttable = commongui.create_payout_table(self, 'credits')
		payoutframe.AddF(self.payouttable, wx.SizerFlags().Expand())
		
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
		
		#*******************************************
		# 				Layout
		#*******************************************
		# number of rounds stuff
		roundslabel = wx.StaticText(betspage, wx.ID_ANY, "Number of Rounds:")
		roundslabel.SetFont(hfont)
		betssizer.AddF(roundslabel, lflag)
		numroundsbox = wx.BoxSizer(wx.HORIZONTAL)
		numroundsbox.AddF(roundsentry, self.bflag)
		numroundsbox.AddF(wx.StaticText(betspage, wx.ID_ANY, "Subject Debt:"), self.bflag)
		numroundsbox.AddF(debtallowed, self.bflag)
		betssizer.AddF(numroundsbox, self.bflag)
		betssizer.AddF(wx.StaticLine(betspage), self.bflag)
		
		# the currency stuff
		currencylabel = wx.StaticText(betspage, wx.ID_ANY, "Currency:")
		currencylabel.SetFont(hfont)
		betssizer.AddF(currencylabel, lflag)
		currencybox = wx.BoxSizer(wx.HORIZONTAL)
		currencybox.AddF(wx.StaticText(betspage, wx.ID_ANY, "Seed Amount:"), self.bflag)
		currencybox.AddF(seedentry, self.bflag)
		currencybox.AddF(self.currencytype, self.bflag)
		betssizer.AddF(currencybox, self.bflag)
		betssizer.AddF(wx.StaticLine(betspage), self.bflag)
		
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
		betssizer.AddF(self.wagertable, self.bflag)
		
		# the payout table
		payoutlabel = wx.StaticText(self, wx.ID_ANY, "Payout Table:")
		payoutlabel.SetFont(hfont)
		
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
		
	def create_page(self, name):
		page = wx.Panel(self.book)
		self.book.AddPage(page, name)
		outerbox = wx.BoxSizer(wx.VERTICAL)
		page.SetSizerAndFit(outerbox)
		return page, outerbox
	
	def update_wagers(self):
		parent = self.amountentry.GetParent()
		parent.Layout()
		self.Layout()
		self.Fit()
			
	# Wager Callbacks
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
			
if __name__ == '__main__':
	app = wx.App(False)
	mainframe = SetupGUI(None)
	app.MainLoop()
