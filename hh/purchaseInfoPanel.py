# 26th May, 2018 5:05pm

import wx
import wx.grid
import wx.xrc
import wx.dataview

from connectToDb import connectToDB
import updatePurchaseMoney as upm

class purchaseInfoPanel ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__( self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )

		bSizer11 = wx.BoxSizer( wx.VERTICAL )

		self.search = wx.TextCtrl( self, wx.ID_ANY, u"", wx.DefaultPosition, size=(-1, 30) )
		self.search.Bind(wx.EVT_TEXT, self.searchInput)
		bSizer11.Add ( self.search, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_purchaseGrid = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,700 ), 0 )
		
		p = self.populateTable()
		lenP = len(p)
		
		# Grid
		self.m_purchaseGrid.CreateGrid( lenP, 7 )
		self.m_purchaseGrid.EnableEditing( False )
		self.m_purchaseGrid.EnableGridLines( True )
		self.m_purchaseGrid.EnableDragGridSize( False )
		self.m_purchaseGrid.SetMargins( 0, 0 )

		# Populate Table
		row = 0
		for x in p:
			col = 0
			x = list(x.values())
			if x[2] > x[3]:
				self.m_purchaseGrid.SetCellBackgroundColour(row, 3, wx.Colour(255, 128, 128))
			for y in x:
				self.m_purchaseGrid.SetCellValue(row, col, str(y))
				col = col + 1
			row = row + 1
		
		# Columns
		self.m_purchaseGrid.SetColSize( 0, 30 )
		self.m_purchaseGrid.SetColSize( 1, 140 )
		self.m_purchaseGrid.SetColSize( 2, 120 )
		self.m_purchaseGrid.SetColSize( 3, 140 )
		self.m_purchaseGrid.SetColSize( 4, 160 )
		self.m_purchaseGrid.SetColSize( 5, 210 )
		self.m_purchaseGrid.SetColSize( 6, 230 )
		#self.m_purchaseGrid.SetColSize( 7, 250 )
		#self.m_purchaseGrid.SetColSize( 8, 270 )
		#self.m_purchaseGrid.AutoSizeColumns()
		self.m_purchaseGrid.EnableDragColMove( True )
		self.m_purchaseGrid.EnableDragColSize( True )
		self.m_purchaseGrid.SetColLabelSize( 30 )
		self.m_purchaseGrid.SetColLabelValue( 0, u"ID" )
		self.m_purchaseGrid.SetColLabelValue( 1, u"Date Time" )
		self.m_purchaseGrid.SetColLabelValue( 2, u"Amount" )
		self.m_purchaseGrid.SetColLabelValue( 3, u"Amount Paid" )
		self.m_purchaseGrid.SetColLabelValue( 4, u"Supplier ID" )
		self.m_purchaseGrid.SetColLabelValue( 5, u"Supplier Name" )
		self.m_purchaseGrid.SetColLabelValue( 6, u"Supplier Contact" )
		#self.m_purchaseGrid.SetColLabelValue( 7, u"Supplier Address" )
		#self.m_purchaseGrid.SetColLabelValue( 8, u"Supplier IBAN" )
		self.m_purchaseGrid.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.m_purchaseGrid.EnableDragRowSize( False )
		self.m_purchaseGrid.SetRowLabelSize( 1 )
		self.m_purchaseGrid.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.m_purchaseGrid.SetDefaultCellAlignment( wx.ALIGN_CENTRE, wx.ALIGN_TOP )
		bSizer11.Add( self.m_purchaseGrid, 0, wx.EXPAND|wx.ALIGN_CENTRE|wx.ALL, 5 )
		
		self.SetSizer( bSizer11 )
		self.Layout()
		bSizer11.Fit( self )
		
		self.m_purchaseGrid.Bind( wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.updateCollectedMoney )
		
	def populateTable (self):
		qry = 'SELECT p.id, p.dateTime, p.totalBill, p.amountPaid, s.id, s.name, s.contact FROM purchase p, supplier s where s.id=p.supplier ORDER BY p.id DESC'
		
		con = connectToDB()
		curs = con.cursor()
		curs.execute(qry)
		
		inv = []
		
		while (1):
			r = curs.fetchone()
			if (r is not None):
				inv.append(r)
			else:
				return inv
		
	def updatePurchases (self):
		self.m_purchaseGrid.DeleteRows(numRows=self.m_purchaseGrid.GetNumberRows())
		
		p = self.populateTable()
		lenP = len(p)
		
		self.m_purchaseGrid.InsertRows(numRows=lenP)
		
		# Populate Table
		row=0
		for x in p:
			col=0
			x = list(x.values())
			if x[2] > x[3]:
				self.m_purchaseGrid.SetCellBackgroundColour(row, 3, wx.Colour(255, 128, 128))
			for y in x:
				self.m_purchaseGrid.SetCellValue(row, col, str(y))
				col = col+1
			row = row+1
	
	def updateCollectedMoney (self, event):
		iid = self.m_purchaseGrid.GetCellValue(event.GetRow(), 0)
		sid = self.m_purchaseGrid.GetCellValue(event.GetRow(), 4)
		dlg = upm.GetData(self, iid, sid)
		dlg.ShowModal()
		self.updatePurchases()
	
	def searchInput(self, event):
		v = self.search.GetValue()
		if v == "":
			self.updatePurchases()
			return
		
		if self.m_purchaseGrid.GetNumberRows() > 0:
			self.m_purchaseGrid.DeleteRows(numRows=self.m_purchaseGrid.GetNumberRows())
		
		qry = 'SELECT DISTINCT p.id, p.dateTime, p.totalBill, p.amountPaid, s.id, s.name, s.contact FROM purchase p, supplier s where s.id=p.supplier and ( p.id LIKE "%'+v+'%" OR p.dateTime LIKE "%'+v+'%" OR p.totalBill LIKE "%'+v+'%" OR p.amountPaid LIKE "%'+v+'%" OR s.id LIKE "%'+v+'%" OR s.name LIKE "%'+v+'%" OR s.contact LIKE "%'+v+'%") ORDER BY p.id DESC'
		con = connectToDB()
		curs = con.cursor()
		curs.execute(qry)
		
		p = []
		
		while (1):
			r = curs.fetchone()
			if (r is not None):
				p.append(r)
			else:
				break
		
		lenP = len(p)
		
		self.m_purchaseGrid.InsertRows(numRows=lenP)

		# Populate Table
		row = 0
		for x in p:
			col = 0
			x = list(x.values())
			if x[2] > x[3]:
				self.m_purchaseGrid.SetCellBackgroundColour(row, 3, wx.Colour(255, 128, 128))
			for y in x:
				self.m_purchaseGrid.SetCellValue(row, col, str(y))
				col = col + 1
			row = row + 1