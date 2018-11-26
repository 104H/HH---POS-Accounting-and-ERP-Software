# 26th May, 2018 5:05pm

import wx
import wx.grid
import wx.xrc
import wx.dataview

from connectToDb import connectToDB
import convertQuotation as cq

class quoteInfoPanel ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__( self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )

		bSizer11 = wx.BoxSizer( wx.VERTICAL )
		
		self.search = wx.TextCtrl( self, wx.ID_ANY, u"", wx.DefaultPosition, size=(-1, 30) )
		self.search.Bind(wx.EVT_TEXT, self.searchInput)
		bSizer11.Add ( self.search, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_quoteInfoGrid = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,700 ), 0 )
		
		p = self.populateTable()
		lenP = len(p)
		
		# Grid
		self.m_quoteInfoGrid.CreateGrid( lenP, 9 )
		self.m_quoteInfoGrid.EnableEditing( False )
		self.m_quoteInfoGrid.EnableGridLines( True )
		self.m_quoteInfoGrid.EnableDragGridSize( False )
		self.m_quoteInfoGrid.SetMargins( 0, 0 )
		
		# Populate Table
		col=0
		for x in p:
			row=0
			# if amount of invoice is smaller than the amount recieved yet, colour the cell red
			#if float(x['amount']) > float(x['amountRecieved']):
			#	self.m_quoteInfoGrid.SetCellTextColour(row, 4, wx.Colour(255, 128, 128))
			for y in list(x.values()):
				self.m_quoteInfoGrid.SetCellValue(col, row, str(y))
				row = row+1
			col = col+1
		
		# Columns
		self.m_quoteInfoGrid.SetColSize( 0, 30 )
		self.m_quoteInfoGrid.SetColSize( 1, 100 )
		self.m_quoteInfoGrid.SetColSize( 2, 120 )
		self.m_quoteInfoGrid.SetColSize( 3, 140 )
		self.m_quoteInfoGrid.SetColSize( 4, 160 )
		self.m_quoteInfoGrid.SetColSize( 5, 80 )
		self.m_quoteInfoGrid.SetColSize( 6, 200 )
		self.m_quoteInfoGrid.SetColSize( 7, 220 )
		self.m_quoteInfoGrid.SetColSize( 8, 240 )
		#self.m_quoteInfoGrid.SetColSize( 9, 300 )
		#self.m_quoteInfoGrid.AutoSizeColumns()
		self.m_quoteInfoGrid.EnableDragColMove( True )
		self.m_quoteInfoGrid.EnableDragColSize( True )
		self.m_quoteInfoGrid.SetColLabelSize( 30 )
		self.m_quoteInfoGrid.SetColLabelValue( 0, u"ID" )
		self.m_quoteInfoGrid.SetColLabelValue( 1, u"Date" )
		self.m_quoteInfoGrid.SetColLabelValue( 2, u"Time" )
		self.m_quoteInfoGrid.SetColLabelValue( 3, u"Amount" )
		self.m_quoteInfoGrid.SetColLabelValue( 4, u"Expiry Date" )
		self.m_quoteInfoGrid.SetColLabelValue( 5, u"Converted" )
		self.m_quoteInfoGrid.SetColLabelValue( 6, u"Customer Name" )
		self.m_quoteInfoGrid.SetColLabelValue( 7, u"Customer Contact" )
		self.m_quoteInfoGrid.SetColLabelValue( 8, u"Customer Address" )
		#self.m_quoteInfoGrid.SetColLabelValue( 9, u"Customer Balance" )
		self.m_quoteInfoGrid.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.m_quoteInfoGrid.EnableDragRowSize( False )
		self.m_quoteInfoGrid.SetRowLabelSize( 1 )
		self.m_quoteInfoGrid.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.m_quoteInfoGrid.SetDefaultCellAlignment( wx.ALIGN_CENTRE, wx.ALIGN_TOP )
		bSizer11.Add( self.m_quoteInfoGrid, 0, wx.EXPAND|wx.ALIGN_CENTRE|wx.ALL, 5 )
		
		self.SetSizer( bSizer11 )
		self.Layout()
		bSizer11.Fit( self )
		
		self.m_quoteInfoGrid.Bind( wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.updateCollectedMoney )
		
	def populateTable (self):
		qry = 'SELECT q.id, SUBSTRING(q.dateTime, 1, 11), SUBSTRING(q.dateTime, 12), q.totalBill, q.expiryDate, q.converted, c.name, c.contact, c.address from quotations q, customer c WHERE q.customer=c.id ORDER BY q.id DESC'
		
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
		
	def updateQuotes (self):
		self.m_quoteInfoGrid.DeleteRows(numRows=self.m_quoteInfoGrid.GetNumberRows())
		
		p = self.populateTable()
		lenP = len(p)
		
		self.m_quoteInfoGrid.InsertRows(numRows=lenP)
		
		# Populate Table
		col=0
		for x in p:
			row=0
			x = list(x.values())
			#if float(x[3]) > float(x[4]):
				#print((x, row))
				#self.m_quoteInfoGrid.SetCellBackgroundColour(x[0], 4, wx.Colour(255, 128, 128))
			for y in x:
				self.m_quoteInfoGrid.SetCellValue(col, row, str(y))
				row = row+1
			col = col+1
	
	def updateCollectedMoney (self, event):
		qid = self.m_quoteInfoGrid.GetCellValue(event.GetRow(), 0)
		dlg = cq.GetData(self, qid) 
		dlg.ShowModal()
		self.updateQuotes()
	
	def searchInput(self, event):
		v = self.search.GetValue()
		if v == "":
			self.updateQuotes()
			return
		
		if self.m_quoteInfoGrid.GetNumberRows() > 0:
			self.m_quoteInfoGrid.DeleteRows(numRows=self.m_quoteInfoGrid.GetNumberRows())
		
		qry = 'SELECT DISTINCT q.id, SUBSTRING(q.dateTime, 1, 11), SUBSTRING(q.dateTime, 12), q.totalBill, q.expiryDate, q.converted, c.name, c.contact, c.address from quotations q, customer c WHERE q.customer=c.id AND (q.id LIKE "%'+v+'%" OR q.dateTime LIKE "%'+v+'%" OR q.totalBill LIKE "%'+v+'%" OR q.expiryDate LIKE "%'+v+'%" OR q.converted LIKE "%'+v+'%" OR c.name LIKE "%'+v+'%" OR c.contact LIKE "%'+v+'%" OR c.address LIKE "%'+v+'%") ORDER BY q.id DESC'
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
		
		self.m_quoteInfoGrid.InsertRows(numRows=lenP)
		
		# Populate Table
		col=0
		for x in p:
			row=0
			x = list(x.values())
			#if float(x[3]) > float(x[4]):
			#	self.m_quoteInfoGrid.SetCellBackgroundColour(x[0], 4, wx.Colour(255, 128, 128))
			for y in x:
				self.m_quoteInfoGrid.SetCellValue(col, row, str(y))
				row = row+1
			col = col+1
