# 26th May, 2018 5:05pm

import wx
import wx.grid
import wx.xrc
import wx.dataview

from connectToDb import connectToDB

import newUser as nu

class usersPanel ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__( self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )

		bSizer11 = wx.BoxSizer( wx.VERTICAL )
		
		self.newUser = wx.Button (self, label="New User")
		bSizer11.Add(self.newUser, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

		self.usersGrid = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,700 ), 0 )
		
		p = self.populateTable()
		lenP = len(p)
		
		# Grid
		self.usersGrid.CreateGrid( lenP, 3 )
		self.usersGrid.EnableEditing( False )
		self.usersGrid.EnableGridLines( True )
		self.usersGrid.EnableDragGridSize( False )
		self.usersGrid.SetMargins( 0, 0 )
		
		# Populate Table
		col=0
		for x in p:
			row=0
			# if amount of invoice is smaller than the amount recieved yet, colour the cell red
			for y in list(x.values()):
				self.usersGrid.SetCellValue(col, row, str(y))
				row = row+1
			col = col+1
		
		# Columns
		self.usersGrid.SetColSize( 0, 30 )
		self.usersGrid.SetColSize( 1, 100 )
		#self.usersGrid.SetColSize( 2, 120 )
		#self.usersGrid.AutoSizeColumns()
		self.usersGrid.EnableDragColMove( True )
		self.usersGrid.EnableDragColSize( True )
		self.usersGrid.SetColLabelSize( 30 )
		self.usersGrid.SetColLabelValue( 0, u"ID" )
		self.usersGrid.SetColLabelValue( 1, u"Username" )
		#self.usersGrid.SetColLabelValue( 2, u" " )
		self.usersGrid.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.usersGrid.EnableDragRowSize( False )
		self.usersGrid.SetRowLabelSize( 1 )
		self.usersGrid.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.usersGrid.SetDefaultCellAlignment( wx.ALIGN_CENTRE, wx.ALIGN_TOP )
		bSizer11.Add( self.usersGrid, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		
		self.SetSizer( bSizer11 )
		self.Layout()
		bSizer11.Fit( self )
		
		self.usersGrid.Bind( wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.deleteUser )
		self.newUser.Bind( wx.EVT_BUTTON, self.createNewUser )
		
	def populateTable (self):
		qry = 'select id, username from users ORDER BY id'
		
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
		
	def updateUsers (self):
		self.usersGrid.DeleteRows(numRows=self.usersGrid.GetNumberRows())
		
		p = self.populateTable()
		lenP = len(p)
		
		self.usersGrid.InsertRows(numRows=lenP)
		
		# Populate Table
		col=0
		for x in p:
			row=0
			x = list(x.values())
			for y in x:
				self.usersGrid.SetCellValue(col, row, str(y))
				row = row+1
			col = col+1
	def deleteUser (self, event):
		x = wx.MessageDialog(self, "Are you sure you want to delete this user?", "Delete User", wx.OK|wx.CANCEL)
		if x.ShowModal() == wx.ID_OK:
			qry = 'DELETE FROM users WHERE id = %s' % (self.usersGrid.GetCellValue(event.GetRow(), 0))
			con = connectToDB()
			curs = con.cursor()
			curs.execute(qry)
			con.commit()
			
			self.updateUsers()
			
	def createNewUser (self, event):
		nuser = nu.GetData(self)
		nuser.ShowModal()
		
		self.updateUsers()
		
		
