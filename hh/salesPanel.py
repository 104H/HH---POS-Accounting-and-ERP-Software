
from terminalFrontEnd import terminalPanel
import newCust as nc

class cashSalePanel (terminalPanel):
	def __init__ (self, parent, transactionButtonName, uid):
		terminalPanel.__init__(self, parent, transactionButtonName, uid)

	def CheckOutFunc( self, event ):
		if len(self.t.cart.products) == 0:
			return
		
		self.t.checkout(float( self.billAfterDiscount.GetLabel() ))
		self.clearCartGrid()
	
	def refundFunc( self, event ):
		self.t.returnProducts(float( self.billAfterDiscount.GetLabel() ))
		self.clearCartGrid()
		#self.m_balanceST.SetFocus()
