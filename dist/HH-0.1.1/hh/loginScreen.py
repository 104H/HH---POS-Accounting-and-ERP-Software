
import wx
import wx.xrc

from connectToDb import connectToDB
conn = connectToDB()

from mainInterface import mainInterface

class loginScreen ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"POS and Accounting", pos = wx.DefaultPosition, size = wx.Size( 676,460 ), style = wx.DEFAULT_FRAME_STYLE|wx.MAXIMIZE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		
		self.mainSizer = wx.BoxSizer( wx.VERTICAL )
		
		self.userName = wx.TextCtrl (self.panel, value="admin")
		self.mainSizer.Add( self.userName, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		
		self.passwd = wx.TextCtrl (self.panel, value="admin")
		self.mainSizer.Add( self.passwd, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		
		self.lgnButton = wx.Button(self.panel, label="Login")
		self.mainSizer.Add( self.lgnButton, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		
		self.panel.SetSizer( self.mainSizer )
		
		bSizer1.Add( self.panel, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		self.lgnButton.Bind(wx.EVT_BUTTON, self.attemptLogin)
	
	def __del__( self ):
		pass
	def attemptLogin (self, event):
		usr = self.userName.GetValue()
		passwd = self.passwd.GetValue()
		c = conn.cursor()
		c.execute("select id, access FROM users WHERE username = '%s' AND password = '%s'" % (usr, passwd))
		r = c.fetchone()
		if r is None:
			#print("Invalid Username and Password")
			self.userName.SetValue("")
			self.passwd.SetValue("")
		else:
			self.Destroy()
			
			app = wx.App()
			mainInterface(None, r['access'], r['id']).Show()
			app.MainLoop()
