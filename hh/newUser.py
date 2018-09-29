from connectToDb import connectToDB

conn = connectToDB()

import wx
import wx.xrc
import re

class GetData(wx.Dialog):
	def __init__(self, parent):
		
		wx.Dialog.__init__(self, parent, wx.ID_ANY, "New User Account", size= (500,280))
		self.panel = wx.Panel(self,wx.ID_ANY)
		
		self.mainSizer = wx.BoxSizer( wx.VERTICAL )
		
		self.lblName = wx.StaticText(self.panel, label="Username")
		self.name = wx.TextCtrl(self.panel, value="", size=(180,-1))
		
		self.labelSizer = wx.BoxSizer( wx.VERTICAL )

		
		self.lblPasswd = wx.StaticText(self.panel, label="Password")
		self.passwd = wx.TextCtrl(self.panel, value="", size=(180,-1))
		
		self.textSizer = wx.BoxSizer( wx.VERTICAL )

		self.labelSizer.Add(self.lblName, 1 , wx.ALL,8 )
		self.labelSizer.Add(self.lblPasswd, 1, wx.ALL,8 )

		self.textSizer.Add(self.name, 1 , wx.ALL,4)
		self.textSizer.Add(self.passwd,1 , wx.ALL,4)

		self.credentialBoxSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.credentialBoxSizer.Add(self.labelSizer, 1, wx.ALL,4)
		self.credentialBoxSizer.Add(self.textSizer, 2, wx.ALL,4)

		self.mainSizer.Add(self.credentialBoxSizer )

		
		self.cashSale = wx.CheckBox(self.panel, wx.ID_ANY, label="cashSale", style=0, name="cashSale")
		self.invoice = wx.CheckBox(self.panel, wx.ID_ANY, label="invoice", style=0, name="invoice")
		self.quote = wx.CheckBox(self.panel, wx.ID_ANY, label="quote", style=0, name="quote")
		self.purchase = wx.CheckBox(self.panel, wx.ID_ANY, label="purchase", style=0, name="purchase")
		self.stockLevels = wx.CheckBox(self.panel, wx.ID_ANY, label="stockLevels", style=0, name="stockLevels")
		self.cashSaleInfo = wx.CheckBox(self.panel, wx.ID_ANY, label="cashSaleInfo", style=0, name="cashSaleInfo")
		self.invoiceInfo = wx.CheckBox(self.panel, wx.ID_ANY, label="invoiceInfo", style=0, name="invoiceInfo")
		self.purchaseInfo = wx.CheckBox(self.panel, wx.ID_ANY, label="purchaseInfo", style=0, name="purchaseInfo")
		self.quoteInfo = wx.CheckBox(self.panel, wx.ID_ANY, label="quoteInfo", style=0, name="quoteInfo")
		self.customerInfo = wx.CheckBox(self.panel, wx.ID_ANY, label="customerInfo", style=0, name="customerInfo")
		self.supplierInfo = wx.CheckBox(self.panel, wx.ID_ANY, label="supplierInfo", style=0, name="supplierInfo")
		self.journal = wx.CheckBox(self.panel, wx.ID_ANY, label="journal", style=0, name="journal")
		self.accountsByFolio = wx.CheckBox(self.panel, wx.ID_ANY, label="accountsByFolio", style=0, name="accountsByFolio")
		self.controlAccount = wx.CheckBox(self.panel, wx.ID_ANY, label="controlAccount", style=0, name="controlAccount")
		self.incomeStatement = wx.CheckBox(self.panel, wx.ID_ANY, label="incomeStatement", style=0, name="incomeStatement")
		self.users = wx.CheckBox(self.panel, wx.ID_ANY, label="users", style=0, name="users")
		#self. = wx.CheckBox(self.panel, wx.ID_ANY, label="", style=0, name="")
		
		self.checkboxSizer1 = wx.BoxSizer( wx.VERTICAL )
		self.checkboxSizer1.Add( self.cashSale, 1, wx.ALL,4 )
		self.checkboxSizer1.Add( self.invoice, 1, wx.ALL,4 )
		self.checkboxSizer1.Add( self.quote , 1, wx.ALL,4)
		self.checkboxSizer1.Add( self.purchase , 1, wx.ALL,4)
		
		self.checkboxSizer2 = wx.BoxSizer( wx.VERTICAL )
		self.checkboxSizer2.Add( self.stockLevels , 1, wx.ALL,4)
		self.checkboxSizer2.Add( self.cashSaleInfo, 1, wx.ALL,4 )
		self.checkboxSizer2.Add( self.invoiceInfo , 1, wx.ALL,4)
		self.checkboxSizer2.Add( self.purchaseInfo , 1, wx.ALL,4)
		self.checkboxSizer2.Add( self.quoteInfo , 1, wx.ALL,4)
		
		self.checkboxSizer3 = wx.BoxSizer( wx.VERTICAL )
		self.checkboxSizer3.Add( self.customerInfo , 1, wx.ALL,4)
		self.checkboxSizer3.Add( self.supplierInfo , 1, wx.ALL,4)
		
		self.checkboxSizer4 = wx.BoxSizer( wx.VERTICAL )
		self.checkboxSizer4.Add( self.journal , 1, wx.ALL,4)
		self.checkboxSizer4.Add( self.accountsByFolio , 1, wx.ALL,4)
		self.checkboxSizer4.Add( self.controlAccount , 1, wx.ALL,4)
		self.checkboxSizer4.Add( self.incomeStatement , 1, wx.ALL,4)
		
		self.checkboxSizer5 = wx.BoxSizer( wx.VERTICAL )
		self.checkboxSizer5.Add( self.users , 1, wx.ALL,4)
		#self.checkboxSizer.Add(  )
		self.checkCollectionBoxSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.checkCollectionBoxSizer.Add( self.checkboxSizer1 ,1 ,wx.LEFT,8)
		self.checkCollectionBoxSizer.Add( self.checkboxSizer2 )
		self.checkCollectionBoxSizer.Add( self.checkboxSizer3 )
		self.checkCollectionBoxSizer.Add( self.checkboxSizer4 )
		self.checkCollectionBoxSizer.Add( self.checkboxSizer5 )

		self.mainSizer.Add(self.checkCollectionBoxSizer)
		
		self.saveButton = wx.Button(self.panel, label="Save")
		self.closeButton = wx.Button(self.panel, label="Cancel")
		
		self.buttonSizer = wx.BoxSizer( wx.HORIZONTAL )
		self.buttonSizer.Add( self.saveButton ,1 , wx.ALL, 8)
		self.buttonSizer.Add( self.closeButton,1 , wx.ALL, 8 )
		self.mainSizer.Add( self.buttonSizer, 1, wx.ALIGN_CENTER,2 )
		
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


		username = self.name.GetValue()
		passwd = self.passwd.GetValue()

		if username != '' and passwd != '':

			access = str(int(self.cashSale.GetValue())) \
					 + str(int(self.invoice.GetValue())) \
					 + str(int(self.quote.GetValue())) \
					 + str(int(self.purchase.GetValue())) \
					 + str(int(self.stockLevels.GetValue())) \
					 + str(int(self.cashSaleInfo.GetValue())) \
					 + str(int(self.invoiceInfo.GetValue())) \
					 + str(int(self.purchaseInfo.GetValue())) \
					 + str(int(self.quoteInfo.GetValue())) \
					 + str(int(self.customerInfo.GetValue())) \
					 + str(int(self.supplierInfo.GetValue())) \
					 + str(int(self.journal.GetValue())) \
					 + str(int(self.accountsByFolio.GetValue())) \
					 + str(int(self.controlAccount.GetValue())) \
					 + str(int(self.incomeStatement.GetValue())) \
					 + str(int(self.users.GetValue()))
			int_access = int(access)
			if int_access != 0:
				qry = 'INSERT INTO users (username, password, access) VALUES ("%s", "%s", "%s")' % (username, passwd, access)
				conn = connectToDB()
				curs = conn.cursor()
				curs.execute(qry)
				conn.commit()

				self.Destroy()
			else:
				y = wx.MessageDialog(self, "Please tick atleast one checkbox", "Notice", wx.OK)
				y.ShowModal()
		else:
			x = wx.MessageDialog(self, "Please enter both username and password", "Notice", wx.OK)
			x.ShowModal()

