
from terminalFrontEnd import terminalPanel
import newCust as nc

class quotationPanel (terminalPanel):
	def __init__ (self, parent, transactionButtonName, uid):
		terminalPanel.__init__(self, parent, transactionButtonName, uid)
		self.returnButton.Hide()
	
	def CheckOutFunc( self, event ):
		expDate = self.makePopUpDate("Enter Expiry Date", "Expiry Date")
		self.t.saveQuote(expDate, float( self.billAfterDiscount.GetLabel() ))
		self.clearCartGrid()
	
	def refundFunc( self, event ):
		self.clearCartGrid()
		self.t.returnProducts()
