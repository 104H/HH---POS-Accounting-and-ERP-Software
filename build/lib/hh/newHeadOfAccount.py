from connectToDb import connectToDB

conn = connectToDB()

import wx
import wx.xrc
import re

import gLedgerFunctions as af
from validators import numOnlyValidator
from connectToDb import connectToDB

class GetData(wx.Dialog):
	def __init__(self, parent):
		
		wx.Dialog.__init__(self, parent, wx.ID_ANY, "New Head of Account", size= (650,400))
		self.panel = wx.Panel(self,wx.ID_ANY)
		
		self.mainSizer = wx.BoxSizer( wx.VERTICAL )
		
		self.lblName = wx.StaticText(self.panel, label="Name")
		self.name = wx.TextCtrl(self.panel, value="", size=(90,-1))
		
		self.nameSizer = wx.BoxSizer( wx.HORIZONTAL )
		self.nameSizer.Add( self.lblName )
		self.nameSizer.Add( self.name )
		self.mainSizer.Add( self.nameSizer )
		
		self.assetRadio = wx.RadioButton(self.panel, wx.ID_ANY, label="Asset", style=0, name="asset")
		self.liabilityRadio = wx.RadioButton(self.panel, wx.ID_ANY, label="Liability", style=0, name="liability")
		
		self.radioSizer = wx.BoxSizer( wx.HORIZONTAL )
		self.radioSizer.Add( self.assetRadio )
		self.radioSizer.Add( self.liabilityRadio )
		self.mainSizer.Add( self.radioSizer )
		
		self.saveButton = wx.Button(self.panel, label="Save")
		self.closeButton = wx.Button(self.panel, label="Cancel")
		
		self.buttonSizer = wx.BoxSizer( wx.HORIZONTAL )
		self.buttonSizer.Add( self.saveButton )
		self.buttonSizer.Add( self.closeButton )
		self.mainSizer.Add( self.buttonSizer )
		
		self.SetSizer( self.mainSizer )
		self.Layout()
		self.mainSizer.Fit(self.panel)
		self.Centre( wx.BOTH )
		
		self.saveButton.Bind(wx.EVT_BUTTON, self.SaveConnString)
		self.closeButton.Bind(wx.EVT_BUTTON, self.OnQuit)
		
		self.Bind(wx.EVT_CLOSE, self.OnQuit)
		
		self.Show()	
		
	def OnQuit(self, event):
		self.result_name = None
		self.Destroy()
	
	def SaveConnString(self, event):
		name = self.name.GetValue()
		
		if self.assetRadio.GetValue():
			val = 1
		elif self.liabilityRadio.GetValue():
			val = 0
		
		qry = 'INSERT INTO headOfAccounts (description, computation) VALUES ("%s", "%s")' % (name, val)
		conn = connectToDB()
		curs = conn.cursor()
		curs.execute(qry)
		conn.commit()
		
		self.Destroy()

