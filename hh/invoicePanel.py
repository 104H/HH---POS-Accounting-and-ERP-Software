
from terminalFrontEnd import terminalPanel
import newCust as nc

class invoiceSalePanel (terminalPanel):
	def __init__ (self, parent, transactionButtonName, uid):
		terminalPanel.__init__(self, parent, transactionButtonName, uid)
		self.returnButton.Hide()
	
	def CheckOutFunc( self, event ):
		amt = self.makePopUp("Enter Recieved Amount", "Amount Recieved")
		self.t.prepareInvoice(amt, float( self.billAfterDiscount.GetLabel() ))
		self.clearCartGrid()
	
	'''
	def refundFunc( self, event ):
		self.clearCartGrid()
		self.t.returnProducts()
	'''
