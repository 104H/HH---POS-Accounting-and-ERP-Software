from connectToDb import connectToDB

conn = connectToDB()

import wx
import wx.xrc

import time as t

import gLedgerFunctions as af
from validators import numOnlyValidator
import invoiceMaker as im
#import functions as f

class GetData(wx.Dialog):
	def __init__(self, parent, iid, cid):
		self.iid = iid
		self.cid = cid
		
		wx.Dialog.__init__(self, parent, wx.ID_ANY, "Invoice "+iid, size= (650,500))
		self.panel = wx.Panel(self,wx.ID_ANY)

		self.m_cartDV = wx.dataview.DataViewListCtrl( self.panel, wx.ID_ANY, (20,20), wx.Size( 600, 180 ), 0 )
		self.m_cartDV.SetMinSize( wx.Size( -1,400 ) )
		
		self.m_cartDV.AppendTextColumn('Name')
		self.m_cartDV.AppendTextColumn('Quantity')
		self.m_cartDV.AppendTextColumn('Price')
		self.m_cartDV.AppendTextColumn('Total Price')
		
		qry = 'select p.name, pi.quantity, pi.price from productinvoice pi, products p where pi.product = p.id and invoiceId = %s' % (iid)
		curs = conn.cursor()
		curs.execute(qry)
		r = curs.fetchone()
		while (1):
			if r is not None:
				self.m_cartDV.AppendItem([ r['name'], str(r['quantity']), str(r['price']), str(int(r['quantity']) * int(r['price'])) ])
				r = curs.fetchone()
			else:
				break

		self.lblRecMoney = wx.StaticText(self.panel, label="Recieved Money", pos=(20,220))
		self.recMoney = wx.TextCtrl(self.panel, value="", pos=(130,220), size=(90,-1), validator=numOnlyValidator())
		
		self.lblcheque = wx.StaticText(self.panel, label="Cheque Number", pos=(20,270))
		self.chequeNum = wx.TextCtrl(self.panel, value="", pos=(130,270), size=(90,-1))
		
		self.lbltranspKey = wx.StaticText(self.panel, label="Bilty", pos=(20,320))
		self.transpKey = wx.TextCtrl(self.panel, value="", pos=(130,320), size=(90,-1))
		
		self.lbltranspAgency = wx.StaticText(self.panel, label="Agency", pos=(20,370))
		self.transpAgency = wx.TextCtrl(self.panel, value="", pos=(130,370), size=(90,-1))
		
		self.saveButton =wx.Button(self.panel, label="Save", pos=(110,420))
		self.closeButton =wx.Button(self.panel, label="Cancel", pos=(250,420))
		self.returnButton =wx.Button(self.panel, label="Return", pos=(390,420))
		self.printInvoiceButton =wx.Button(self.panel, label="Print Invoice", pos=(530,420))
		
		self.saveButton.Bind(wx.EVT_BUTTON, self.SaveConnString)
		self.closeButton.Bind(wx.EVT_BUTTON, self.OnQuit)
		self.returnButton.Bind(wx.EVT_BUTTON, self.OnReturn)
		self.printInvoiceButton.Bind(wx.EVT_BUTTON, self.makeInvoice)
		
		self.Bind(wx.EVT_CLOSE, self.OnQuit)
		
		self.Show()
	
	def returnInvoice(self, saleId):
		curs = conn.cursor()
		qry = 'UPDATE invoice SET returned=1 WHERE id = %s' % (saleId)
		curs.execute(qry)
	
		qry = 'UPDATE currentinventory ci JOIN productinvoice pi ON ci.productId = pi.product SET ci.quantity = ci.quantity+pi.quantity WHERE pi.invoiceId = %s' % (saleId)
		curs.execute(qry)
		
		conn.commit()
	
		af.invoiceReturnEntry(saleId)

	def OnReturn (self, event):
		self.returnInvoice(self.iid)
		self.Destroy()

	def OnQuit(self, event):
		self.result_name = None
		self.Destroy()
	
	def updateMoney (self, iid, amt, cust, cheque):
		### update recieved amount
		qry = 'UPDATE `invoice` SET amountRecieved = amountRecieved+%s WHERE id = %s' % (amt, iid)
		curs = conn.cursor()
		curs.execute(qry)
		
		qry = 'INSERT INTO `invoicePayment` (invoiceId, amount) VALUES (%s, %s)' % (iid, amt)
		curs = conn.cursor()
		curs.execute(qry)
		
		conn.commit()

		af.invoiceMoneyUpdateEntry (amt, cust, iid, cheque)

	def updateTranspKey(self, transpKey, transAgency, iid):
		qry = 'UPDATE `invoice` SET transportKey = "%s", transportAgency = "%s" WHERE id = %s' % (transpKey, transAgency, iid)
		curs = conn.cursor()
		curs.execute(qry)
		conn.commit()
		
	def SaveConnString(self, event):
		if not self.recMoney.Validate():
				return
		recMoney = self.recMoney.GetValue()
		cheque = self.chequeNum.GetValue()
		transpKey = self.transpKey.GetValue()
		transpAgency = self.transpAgency.GetValue()
		if (recMoney != ''):
			self.updateMoney(self.iid, recMoney, self.cid, cheque)
		if (transpKey != ''):
			self.updateTranspKey(transpKey, transpAgency, self.iid)
		self.Destroy()
	
	def makeInvoice (self, event):
		conn = connectToDB()
		
		qry = 'select p.name, pi.quantity, pi.price, pi.discount from productinvoice pi, products p where pi.product = p.id and invoiceId = %s' % (self.iid)
		
		curs = conn.cursor()
		curs.execute(qry)
		r = curs.fetchone()
		
		prods = []
		
		while r is not None:
			prods.append([ r['name'], '', int(r['quantity']), int(r['price']) + int(r['discount']), int(r['price']) ])
			r = curs.fetchone()
		
		qry = 'select i.id, i.employeeid, i.timeStamp, i.amount, i.amountRecieved, i.discount, c.id, c.name, c.contact from customer c, invoice i where i.buyerId = c.id ORDER BY i.id DESC'
		
		curs = conn.cursor()
		curs.execute(qry)
		
		r = curs.fetchone()
		
		im.imaker(str(self.iid), 
		self.iid, 
		r['employeeid'], 
		r['c.id'], 
		r['name'], 
		r['contact'], 
		prods, 
		int(r['discount']), 
		int(r['amountRecieved']), 
		r['timeStamp'])
		
		import os
		cmd = "lpr -P HP-LaserJet-M101-M106 " + str(self.iid)
		os.system(cmd)
		
		self.Destroy()
	
