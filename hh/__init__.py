
import wx
import wx.xrc

from loginScreen import loginScreen

if __name__ == "__main__":
	app = wx.App()
	loginScreen(None).Show()
	
	app.MainLoop()
	
