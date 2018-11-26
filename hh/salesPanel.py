from terminalFrontEnd import terminalPanel
import newCust as nc
import wx


class cashSalePanel(terminalPanel):
    def __init__(self, parent, transactionButtonName, uid):
        terminalPanel.__init__(self, parent, transactionButtonName, uid)

    def CheckOutFunc(self, event):
        if len(self.t.cart.products) == 0:
            return

        amt = self.makePopUp("Enter Recieved Amount", "Amount Recieved")
        if amt == "":
            return
        while amt.isdigit() is False:
            amt = self.makePopUp("Enter Recieved Amount (only digits)", "Amount Recieved")
            print(amt)

        isprinter = self.t.checkout(int(amt))
        if isprinter is None:
            x = wx.MessageDialog(self, "Printer not connected", "No Printer", wx.OK)
            x.ShowModal()
        else:
            self.clearCartGrid()


def refundFunc(self, event):
    self.clearCartGrid()
    self.t.returnProducts()  # self.m_balanceST.SetFocus()
