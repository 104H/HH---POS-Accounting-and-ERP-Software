# 26th May, 2018 5:05pm

import wx
import wx.grid
import wx.xrc
import wx.dataview

from connectToDb import connectToDB

class saleInfoPanel ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__( self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )

		bSizer11 = wx.BoxSizer( wx.VERTICAL )

		self.search = wx.TextCtrl( self, wx.ID_ANY, u"", wx.DefaultPosition, size=(-1, 30) )
		self.search.Bind(wx.EVT_TEXT, self.searchInput)
		bSizer11.Add ( self.search, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_saleInfoGrid = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		
		p = self.populateTable()
		lenP = len(p)
		
		# Grid
		self.m_saleInfoGrid.CreateGrid( lenP, 8 )
		self.m_saleInfoGrid.EnableEditing( False )
		self.m_saleInfoGrid.EnableGridLines( True )
		self.m_saleInfoGrid.EnableDragGridSize( False )
		self.m_saleInfoGrid.SetMargins( 0, 0 )
		
		# Populate Table
		col=0
		for x in p:
			row=0
			for y in list(x.values()):
				self.m_saleInfoGrid.SetCellValue(col, row, str(y))
				row = row+1
			col = col+1
		
		# Columns
		self.m_saleInfoGrid.SetColSize( 0, 30 )
		self.m_saleInfoGrid.SetColSize( 1, 60 )
		self.m_saleInfoGrid.SetColSize( 2, 90 )
		self.m_saleInfoGrid.SetColSize( 3, 120 )
		#self.m_saleInfoGrid.AutoSizeColumns()
		self.m_saleInfoGrid.EnableDragColMove( True )
		self.m_saleInfoGrid.EnableDragColSize( True )
		self.m_saleInfoGrid.SetColLabelSize( 30 )
		self.m_saleInfoGrid.SetColLabelValue( 0, u"ID" )
		self.m_saleInfoGrid.SetColLabelValue( 1, u"Date Time" )
		self.m_saleInfoGrid.SetColLabelValue( 2, u"Amount" )
		self.m_saleInfoGrid.SetColLabelValue( 3, u"Employee ID" )
		self.m_saleInfoGrid.SetColLabelValue( 4, u"Refund" )
		self.m_saleInfoGrid.SetColLabelValue( 5, u"Customer Name" )
		self.m_saleInfoGrid.SetColLabelValue( 6, u"Customer Contact" )
		self.m_saleInfoGrid.SetColLabelValue( 7, u"Customer Address" )
		self.m_saleInfoGrid.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.m_saleInfoGrid.EnableDragRowSize( False )
		self.m_saleInfoGrid.SetRowLabelSize( 1 )
		self.m_saleInfoGrid.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.m_saleInfoGrid.SetDefaultCellAlignment( wx.ALIGN_CENTRE, wx.ALIGN_TOP )
		bSizer11.Add( self.m_saleInfoGrid, 0, wx.EXPAND|wx.ALIGN_CENTRE|wx.ALL, 5 )
		
		self.SetSizer( bSizer11 )
		self.Layout()
		bSizer11.Fit( self )
		
		self.m_saleInfoGrid.Bind( wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.refundSale )
		
	def populateTable (self):
		qry = 'select s.id, s.dateTime, s.totalBill, s.preparedBy, s.refund, c.name, c.contact, c.address from sales s, customer c where s.customer = c.id'
		
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
		
	def updateSales (self):
		self.m_saleInfoGrid.DeleteRows(numRows=self.m_saleInfoGrid.GetNumberRows())
		
		p = self.populateTable()
		lenP = len(p)
		
		self.m_saleInfoGrid.InsertRows(numRows=lenP)
		
		# Populate Table
		col=0
		for x in p:
			row=0
			for y in list(x.values()):
				self.m_saleInfoGrid.SetCellValue(col, row, str(y))
				row = row+1
			col = col+1
	
	def refundSale (self, event):
		iid = self.m_saleInfoGrid.GetCellValue(event.GetRow(), 0)
		dlg = uim.GetData(self, iid) 
		dlg.ShowModal()
		self.updateStocks()
	
	def searchInput(self, event):
		v = self.search.GetValue()
		if v == "":
			self.updateSales()
			return
		
		if self.m_saleInfoGrid.GetNumberRows() > 0:
			self.m_saleInfoGrid.DeleteRows(numRows=self.m_saleInfoGrid.GetNumberRows())
		
		qry = 'select DISTINCT s.id, s.dateTime, s.totalBill, s.preparedBy, s.refund, c.name, c.contact, c.address from sales s, customer c where s.customer = c.id AND (s.id LIKE "%'+v+'%" OR s.dateTime LIKE "%'+v+'%" OR s.totalBill LIKE "%'+v+'%" OR s.preparedBy LIKE "%'+v+'%" OR s.refund LIKE "%'+v+'%" OR c.name LIKE "%'+v+'%" OR c.contact LIKE "%'+v+'%" OR c.address LIKE "%'+v+'%") ORDER BY s.id'
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
		
		self.m_saleInfoGrid.InsertRows(numRows=lenP)
		
		# Populate Table
		col=0
		for x in p:
			row=0
			x = list(x.values())
			#if float(x[3]) > float(x[4]):
			#	self.m_productsGrid.SetCellBackgroundColour(x[0], 4, wx.Colour(255, 128, 128))
			for y in x:
				self.m_saleInfoGrid.SetCellValue(col, row, str(y))
				row = row+1
			col = col+1
