from connectToDb import connectToDB

conn = connectToDB()

import wx
import wx.xrc
import re

import barcodeMaker as bm

class GetData(wx.Dialog):
	def __init__(self, parent):
		
		wx.Dialog.__init__(self, parent, wx.ID_ANY, "Print Barcodes", size= (650,400))
		self.panel = wx.Panel(self,wx.ID_ANY)
		
		self.mainSizer = wx.BoxSizer( wx.VERTICAL )
		
		self.lblName = wx.StaticText(self.panel, label="Barcode")
		self.name = wx.TextCtrl(self.panel, value="", size=(90,-1))
		
		self.nameSizer = wx.BoxSizer( wx.HORIZONTAL )
		self.nameSizer.Add( self.lblName )
		self.nameSizer.Add( self.name )
		self.mainSizer.Add( self.nameSizer )
		
		self.lblheight = wx.StaticText(self.panel, label="Height (in mm)")
		self.height = wx.TextCtrl(self.panel, value="", size=(90,-1))
		
		self.heightSizer = wx.BoxSizer( wx.HORIZONTAL )
		self.heightSizer.Add( self.lblheight )
		self.heightSizer.Add( self.height )
		self.mainSizer.Add( self.heightSizer )
		
		self.lblwidth = wx.StaticText(self.panel, label="Width (in mm)")
		self.width = wx.TextCtrl(self.panel, value="", size=(90,-1))
		
		self.widthSizer = wx.BoxSizer( wx.HORIZONTAL )
		self.widthSizer.Add( self.lblwidth )
		self.widthSizer.Add( self.width )
		self.mainSizer.Add( self.widthSizer )
		
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
		height = self.height.GetValue()
		width = self.width.GetValue()
		
		bm.makeBarcodeFile(name, width, height)
		
		self.Destroy()

