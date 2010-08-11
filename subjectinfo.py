#!/usr/bin/env python

import wx
import CogSub

class SubjectInfoDialog(wx.Dialog):
	""" A dialogue to collect subject information prior to gameplay """
	def __init__(self, parent, title):
		wx.Dialog.__init__(self, parent, wx.ID_ANY, title)
		
		# create the sizers
		sizer = wx.BoxSizer(wx.VERTICAL)
		buttonsizer = wx.BoxSizer(wx.HORIZONTAL)
		grid = wx.FlexGridSizer(4,2)
		
		# the fields
		blank = lambda : wx.StaticText(self, wx.ID_ANY, "")
		nameentry = wx.TextCtrl(self, wx.ID_ANY)
		ageentry = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_RIGHT)
		sexentry = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_RIGHT)
		handedentry = wx.Choice(self, wx.ID_ANY, choices=["Right", "Left"])
		self.infodict = {"Name":(nameentry, blank()), "Age":(ageentry, blank()), "Sex":(sexentry, blank()),
			"Handedness":(handedentry, blank())}
		flag = wx.SizerFlags().Border(wx.ALL, 5)
		
		# add them to the grid
		for key, control in self.infodict.iteritems():
			control[1].SetLabel(key + ":")
			grid.AddF(control[1], flag)
			grid.AddF(control[0], flag)
		
		# create the buttons
		buttonflag = wx.SizerFlags().Align(wx.ALIGN_RIGHT).Border(wx.ALL, 10)
		buttonsizer.AddF(wx.Button(self, wx.ID_CANCEL), buttonflag)
		buttonsizer.AddF(wx.Button(self, wx.ID_SAVE), buttonflag)
		self.SetAffirmativeId(wx.ID_SAVE)

		# put it all together		
		sizer.AddF(grid, wx.SizerFlags(0).Expand().Border(wx.ALL, 10) )
		sizer.AddF(buttonsizer, buttonflag)
		
		self.SetSizerAndFit(sizer)
		
	def enable_control(self, key, enable):
		control = self.infodict[key]
		control[0].Enable(enable)
		control[1].Enable(enable)
	
	def save_info(self):
		self.cogsub = CogSub.Subject()
		for key in self.infodict.keys():
			control = self.infodict[key]
			if control[0].IsEnabled():
				if key == "Name":
					self.cogsub.s_id = control[0].GetValue()
				elif key == "Handedness":
					self.cogsub.hand = control[0].GetStringSelection()
				elif key == "Age":
					self.cogsub.age = control[0].GetValue()
				elif key == "Sex":
					self.cogsub.sex = control[0].GetValue()
