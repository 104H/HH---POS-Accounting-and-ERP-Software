from connectToDb import connectToDB



import wx
import wx.xrc
import wx.grid
import wx.adv
import re

import gLedgerFunctions as af
from validators import numOnlyValidator

conn = connectToDB()


class GetData(wx.Dialog):
	def __init__(self, parent):
		
		wx.Dialog.__init__(self, parent, wx.ID_ANY, "Manual Entry", size= (650,600))
		self.panel = wx.Panel(self,wx.ID_ANY)
		
		self.mainSizer = wx.BoxSizer( wx.VERTICAL )
		
		self.folios = self.fetchFolios()

		self.lblFolioD = wx.StaticText(self.panel, label="Folio (Debit)")
		self.folioComboD = wx.ComboBox(self.panel, id=wx.ID_ANY ,size=wx.DefaultSize, choices= list(self.folios.keys()) )
		print(self.folioComboD.GetCount())

		self.debitSizer = wx.BoxSizer( wx.HORIZONTAL )
		self.debitSizer.Add( self.lblFolioD )
		self.debitSizer.Add(self.folioComboD)

		self.mainSizer.Add(self.debitSizer )
		#self.folioC = wx.TextCtrl(self.panel, value="", pos=(130,70), size=(90,-1))
		
		self.lblFolioC = wx.StaticText(self.panel, label="Folio (Credit)")
		self.folioComboC = wx.ComboBox(self.panel, size=wx.DefaultSize, choices= list(self.folios.keys()))

		self.creditSizer = wx.BoxSizer( wx.HORIZONTAL )
		self.creditSizer.Add( self.lblFolioC )
		self.creditSizer.Add( self.folioComboC )
		self.mainSizer.Add( self.creditSizer )
		
		self.lblTransaction = wx.StaticText(self.panel, label="Transaction Type", pos=(20,170))
		self.transaction = wx.TextCtrl(self.panel, value="", size=(90,-1))
		
		self.transSizer = wx.BoxSizer( wx.HORIZONTAL )
		self.transSizer.Add( self.lblTransaction )
		self.transSizer.Add( self.transaction )
		self.mainSizer.Add( self.transSizer )
		
		self.lblChequeNo = wx.StaticText(self.panel, label="Cheque Number")
		self.chequeNo = wx.TextCtrl(self.panel, value="", size=(90,-1))
		
		self.chequeSizer = wx.BoxSizer( wx.HORIZONTAL )
		self.chequeSizer.Add( self.lblChequeNo )
		self.chequeSizer.Add( self.chequeNo )
		self.mainSizer.Add( self.chequeSizer )
		
		self.lblAmount = wx.StaticText(self.panel, label="Amount")
		self.amount = wx.TextCtrl(self.panel, value="", size=(90,-1), validator=numOnlyValidator())

		self.amountSizer = wx.BoxSizer( wx.HORIZONTAL )
		self.amountSizer.Add( self.lblAmount )
		self.amountSizer.Add( self.amount )
		self.mainSizer.Add( self.amountSizer )
		
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
		
	def transformHOAtoName (self, desc):
		x = re.search ("(?<=Customer)[0-9]*", desc)
		if x is not None:
			q = 'SELECT name FROM customer WHERE id = %s' % (x.group(0))
			c = conn.cursor()
			c.execute(q)
			cust = c.fetchone()
			return cust['name'] + " A/C Recievable"

		x = re.search ("(?<=Supplier)[0-9]*", desc)
		if x is not None:
			q = 'SELECT name FROM supplier WHERE id = %s' % (x.group(0))
			c = conn.cursor()
			c.execute(q)
			cust = c.fetchone()
			return cust['name'] + " A/C Payable"
		return None

	def fetchFolios (self):
		qry = 'SELECT id, description FROM headOfAccounts'
		curs = conn.cursor()
		curs.execute(qry)
		r = curs.fetchall()

		folios = {}
		for x in r:
			z = self.transformHOAtoName(x['description'])
			if z is not None:
				folios.update({z : x['id']})
			else:
				folios.update({x['description'] : x['id']})
		return folios

	def OnQuit(self, event):
		self.result_name = None
		self.Destroy()
	
	def SaveConnString(self, event):
		#hoa = self.m_folioCombo.GetValue()
		hoaCredit = self.folios[self.folioComboD.GetValue()]
		hoaDebit = self.folios[self.folioComboC.GetValue()]
		tran = self.transaction.GetValue()
		cheque = self.chequeNo.GetValue()
		amount = self.amount.GetValue()
		
		if ( hoaCredit != "" and hoaDebit != "" and amount != "" ):
			af.manualEntry (hoaCredit, hoaDebit, tran, cheque, amount)
		
		self.Destroy()

