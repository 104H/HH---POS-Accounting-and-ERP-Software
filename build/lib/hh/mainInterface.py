
import wx
import wx.xrc

from connectToDb import connectToDB
conn = connectToDB()

from connectToDb import connectToDB
from salesPanel import cashSalePanel
from invoicePanel import invoiceSalePanel
from quotationPanel import quotationPanel
from purchasePanel import purchasePanel
from stockLevelsPanel import stockLevelsPanel
from saleInfoPanel import saleInfoPanel
from invoiceInfoPanel import invoiceInfoPanel
from purchaseInfoPanel import purchaseInfoPanel
from customerInfoPanel import customerInfoPanel
from supplierInfoPanel import supplierInfoPanel
from quoteInfoPanel import quoteInfoPanel
from journal import journalPanel
from accountsByFolio import folioAccountsPanel
from controlAccountPanel import controlAccountPanel
from incomeStatementPanel import incomeStatementPanel
from usersPanel import usersPanel

class mainInterface ( wx.Frame ):
	
	def __init__( self, parent, access, uid ):
		self.makeInventoryValEntry()
		
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"POS, ERP and Accounting", pos = wx.DefaultPosition, size = wx.Size( 676,460 ), style = wx.DEFAULT_FRAME_STYLE|wx.MAXIMIZE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_notebook1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		x = 0
		if access[x:x+1] == '1':
			self.m_salesPanel = cashSalePanel( self.m_notebook1, "Cash Sale", uid )
			self.m_notebook1.AddPage( self.m_salesPanel, u"Sales", True )
		x = x+1
		
		if access[x:x+1] == '1':
			self.m_invoicePanel = invoiceSalePanel( self.m_notebook1, "Print Invoice", uid )
			self.m_notebook1.AddPage( self.m_invoicePanel, u"Invoice", False )
		x = x+1
		
		if access[x:x+1] == '1':
			self.m_quotePanel = quotationPanel( self.m_notebook1, "Print Quotation", uid )
			self.m_notebook1.AddPage( self.m_quotePanel, u"Quotation", False )
		x = x+1
		
		if access[x:x+1] == '1':
			self.m_purchasePanel = purchasePanel( self.m_notebook1, "Purchase", uid )
			self.m_notebook1.AddPage( self.m_purchasePanel, u"GPN", False )
		x = x+1
		
		if access[x:x+1] == '1':
			self.m_stockLevelsPanel = stockLevelsPanel( self.m_notebook1 )
			self.m_notebook1.AddPage( self.m_stockLevelsPanel, u"Stock Levels", False )
		x = x+1
		
		if access[x:x+1] == '1':
			self.m_salesInfoPanel = saleInfoPanel(self.m_notebook1)
			self.m_notebook1.AddPage( self.m_salesInfoPanel, u"Sale Info", False )
		x = x+1
		
		if access[x:x+1] == '1':
			self.m_invoiceInfoPanel = invoiceInfoPanel(self.m_notebook1)
			self.m_notebook1.AddPage( self.m_invoiceInfoPanel, u"Invoice Info", False )
		x = x+1
		
		if access[x:x+1] == '1':
			self.m_purchaseInfoPanel = purchaseInfoPanel(self.m_notebook1)
			self.m_notebook1.AddPage( self.m_purchaseInfoPanel, u"GPN Info", False )
		x = x+1
		
		if access[x:x+1] == '1':
			self.m_quoteInfoPanel = quoteInfoPanel(self.m_notebook1)
			self.m_notebook1.AddPage( self.m_quoteInfoPanel, u"Quotation Info", False )
		x = x+1
		
		if access[x:x+1] == '1':
			self.m_customerInfoPanel = customerInfoPanel(self.m_notebook1)
			self.m_notebook1.AddPage( self.m_customerInfoPanel, u"Customer Info", False )
		x = x+1
		
		if access[x:x+1] == '1':
			self.m_supplierInfoPanel = supplierInfoPanel(self.m_notebook1)
			self.m_notebook1.AddPage( self.m_supplierInfoPanel, u"Supplier Info", False )
		x = x+1
		
		if access[x:x+1] == '1':
			self.m_journalPanel = journalPanel(self.m_notebook1)
			self.m_notebook1.AddPage( self.m_journalPanel, u"Journal", False )
		x = x+1
		
		if access[x:x+1] == '1':
			self.m_folioAccountsPanel = folioAccountsPanel(self.m_notebook1)
			self.m_notebook1.AddPage( self.m_folioAccountsPanel, u"Accounts", False )
		x = x+1
		
		if access[x:x+1] == '1':
			self.m_controlAccountPanel = controlAccountPanel(self.m_notebook1)
			self.m_notebook1.AddPage( self.m_controlAccountPanel, u"Control Account", False )
		x = x+1
		
		if access[x:x+1] == '1':
			self.m_incomeStatementPanel = incomeStatementPanel(self.m_notebook1)
			self.m_notebook1.AddPage( self.m_incomeStatementPanel, u"Income Statement", False )
		x = x+1
		
		if access[x:x+1] == '1':
			self.m_usersPanel = usersPanel(self.m_notebook1)
			self.m_notebook1.AddPage( self.m_usersPanel, u"Users", False )
		x = x+1
		
		bSizer1.Add( self.m_notebook1, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		self.m_notebook1.Bind( wx.EVT_NOTEBOOK_PAGE_CHANGED, self.refreshStockLevels)
	
	def __del__( self ):
		pass
	def refreshStockLevels (self, event):
		self.m_stockLevelsPanel.updateStocks()
		self.m_invoiceInfoPanel.updateInvoices()
		self.m_purchaseInfoPanel.updatePurchases()
		self.m_customerInfoPanel.updateCustomers()
		self.m_supplierInfoPanel.updateSuppliers()
		self.m_quoteInfoPanel.updateQuotes()
		self.m_journalPanel.reloadJournal()
		self.m_folioAccountsPanel.reloadJournal()
		self.m_controlAccountPanel.reloadJournal()
	def makeInventoryValEntry (self):
		qry = 'INSERT IGNORE INTO inventoryVal (inventory) VALUES ( (SELECT SUM(p.costPrice * ci.quantity) FROM products p, currentinventory ci WHERE ci.productId = p.id) )'
		con = connectToDB()
		curs = con.cursor()
		curs.execute(qry)
		con.commit()

