
import wx
import wx.xrc
import time

from manage_mysql_script import Manage_Mysql

my_sql = Manage_Mysql()
my_sql.start()

time.sleep(3)

from loginScreen import loginScreen
def main():

	print("hello")
	app = wx.App()
	loginScreen(None).Show()
	
	app.MainLoop()
	print("hello")
	my_sql.stop()
	print('closed')
	
if __name__ == "__main__":
	main()
