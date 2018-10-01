import time as t
import os

from connectToDb import connectToDB
import gLedgerFunctions as af
import invoiceMaker as im
import purchaseInvoiceMaker as pim
import printer as pr

class product:
	def __init__ (self, pid, name, qty, price):
		self.pid = pid
		self.name = name
		self.qty = qty
		self.price = price
		self.origPrice = price

class cart:
	def __init__ (self):
		self.products = []
		
	def __repr__ (self):
		return self.products
	
	def addProduct (self, pid, name, qty, sellingPrice):
		prod = product(pid, name, qty, sellingPrice)
		self.products.append(prod)
	
	def removeProduct (self, prod):


		for index, x in enumerate(self.products):

			if str(x.pid) == str(prod):

				del self.products[index]


	
	def makeEmpty(self):
		self.products = []
			
	def computeTotalBill (self):
		bill = 0
		for p in self.products:
			bill = bill + ( p.price * p.qty )
		return bill

	def computeTotalDiscount (self):
		discount = 0
		for p in self.products:
			discount = discount + ( p.qty * ( p.origPrice - p.price ) )
		return discount
	
class terminal:
	def __init__ (self):
		self.cart = cart()
		
		self.customerId = 0
		self.customerName = ''
		self.customerContact = ''
		
		self.supplierId = 0
		self.supplierName = ''
		
		self.operatorId = 0
	
	def getCart (self):
		return self.cart
	
	def getCartProducts (self):
		return self.cart.products
	
	def numberOfItems (self):
		return len(self.cart.products)
		
	def refresh (self):
		self.customerId = 0
		self.supplierId = 0
		self.cart.makeEmpty()
		
	def commitInsertQuery (self, qry):
		conn = connectToDB()
		
		curs = conn.cursor()
		curs.execute(qry)
		insertId = conn.insert_id()
		conn.commit()
		return insertId
	
	def findProduct(self, productIdentifier, qty):
		conn = connectToDB()
		
		qry = 'SELECT p.id FROM products p where p.codeName LIKE "%s"' % (productIdentifier)
		curs = conn.cursor()
		curs.execute(qry)
		r = curs.fetchone()
		print(qry)
		if (r is None):
			qry = 'SELECT p.id FROM products p where p.barcode LIKE "%s"' % (productIdentifier)
			print('inside cart.py class terminal findProduct: ' + str(qry))
			curs.execute(qry)
			r = curs.fetchone()
			print('inside cart.py class terminal print r when none: ' + str(r))
		if r is not None:
			print('inside cart.py class terminal print r when not none : ' + str(r))
			for p in self.cart.products:
				if r['id'] == p.pid:
					return False
		
			x = self.scanProduct(r['id'], qty)
			return x
	
	def scanProduct (self, pid, qty):
		conn = connectToDB()
		
		qry = 'SELECT ci.productId, ci.quantity, p.name, p.sellingPrice from currentinventory ci, products p where ci.productId = %d and ci.productId = p.id' % pid
		curs = conn.cursor()
		curs.execute(qry)
		r = curs.fetchone()
		print(r)
	
		'''
		To allow negative stock levels this part was commented
		if (r['quantity'] < qty):
			return r['quantity']
		else:
			qry = 'UPDATE `currentinventory` SET `quantity`=%d WHERE `productId` = %s' % (int(r['quantity'])-int(qty), r['productId'])
			curs.execute(qry)
			conn.commit()
			
			self.addToCart(pid, r['name'], qty, r['sellingPrice'])
		return True
		'''
		
		self.addToCart(pid, r['name'], qty, r['sellingPrice'])
		return True
	
	def addToCart (self, pid, name, qty, sellingPrice):
		self.cart.addProduct(pid, name, qty, sellingPrice)
		
	def removeFromCart (self, pid):

		self.cart.removeProduct(pid)
	
	def computeTotalBill(self):
		return self.cart.computeTotalBill()
	
	def computeTotalDiscount(self):
		return self.cart.computeTotalDiscount()
	
	'''
	# this version of the function changed stock levels as products were punched into the cart
	# but this was removed and simpler version was deployed after the client asked for negative stock levels
	def increaseQty (self, pid, qty):
		qry = 'SELECT quantity from currentinventory where productId = %d' % pid
		curs = conn.cursor()
		curs.execute(qry)
		r = curs.fetchone()
	
		if (r['quantity'] < qty):
			return r['quantity']
		else:
			qry = 'UPDATE `currentinventory` SET `quantity`=`quantity`-%d WHERE `productId` = %s' % (int(qty), str(pid))
			self.commitInsertQuery(qry)
			
			c = 0
			for p in self.cart.products:
				if (pid == p.pid):
					self.cart.products[c].qty = self.cart.products[c].qty + qty
				c = c + 1
			return True
	'''
	
	def increaseQty (self, pid, qty):
		c = 0
		for p in self.cart.products:
			if (pid == p.pid):
				self.cart.products[c].qty = self.cart.products[c].qty + qty
			c = c + 1
		return True
	
	def fetchCustomerId (self, contact):
		conn = connectToDB()
		
		qry = "SELECT id, name from customer WHERE contact = '%s'" % str( contact )
		curs = conn.cursor()
		curs.execute(qry)
		r = curs.fetchone()
		
		if r is not None:
			self.customerId = r['id']
			self.customerName = r['name']
			self.customerContact = str(contact)
			return True
		return False
	
	def registerNewCustomer (self, name, contact):
		qry = "INSERT INTO customer (name, contact) VALUES ('%s', '%s')" % (name, contact)
		self.customerId = self.commitInsertQuery(qry)
	
	def fetchSupplierId (self, contact):
		conn = connectToDB()
		
		qry = "SELECT id, name from supplier WHERE contact = '%s'" % str( contact )
		curs = conn.cursor()
		curs.execute(qry)
		r = curs.fetchone()
		
		if r is not None:
			self.supplierId = r['id']
			self.supplierName = r['name']
			return True
		return False
	
	def registerNewSupplier (self, name, contact):
		qry = "INSERT INTO supplier (name, contact) VALUES ('%s', '%s')" % (name, contact)
		self.supplierId = self.commitInsertQuery(qry)
	
	# ========== Cash Sale =================================
	def checkout (self, amt):
		if (len(self.cart.products) == 0):
			return
		
		bill = self.computeTotalBill()
		discount = self.computeTotalDiscount()
		
		# if a discount was imposed at the time of payment
		# store that discount as well
		discount = discount + (bill - amt)
		
		saleId = self.recordSale(amt, discount)
		self.recordProductsInSale(saleId)
		self.cashSaleJournalEntry(saleId, amt, discount)
		#printInvoice(t.strftime("%d-%m-%y", t.localtime()), i)
		pr.printReciept(self.cart.products, t.strftime("%d-%m-%y", t.localtime()), saleId, amt, bill-amt)
		self.refresh()
	
	def recordSale (self, bill, discount):
		qry = 'INSERT INTO `sales` (customer, totalBill, discount, preparedBy) VALUES (%d, %d, %d, %s)' % (self.customerId, bill, discount, self.operatorId)
		return self.commitInsertQuery(qry)
		
	
	def recordProductsInSale (self, saleId):
		for p in self.cart.products:
			qry = 'INSERT INTO productsale (saleId, product, quantity, price, discount) VALUES (%s, %s, %s, %s, %s)' % (saleId, p.pid, p.qty, p.price, p.origPrice - p.price )
			self.commitInsertQuery(qry)
			
			qry = 'UPDATE `currentinventory` SET `quantity`=`quantity`-%s WHERE `productId` = %s' % (p.qty, p.pid)
			return self.commitInsertQuery(qry)
		
	
	def cashSaleJournalEntry (self, saleId, bill, discount):
		af.cashSaleEntry(bill, discount, saleId)
	
	def returnProducts (self):
		if (len(self.cart.products) == 0):
			return
		
		bill = self.computeTotalBill()
		discount = self.computeTotalDiscount()
		
		returnId = self.recordReturn(bill, discount)
		self.recordProductsInReturn(returnId)
		self.returnJournalEntry(returnId, bill, discount)
		self.refresh()
	
	def recordReturn (self, bill, discount):
		qry = 'INSERT INTO `refunds` (customer, totalBill, discount, preparedBy) VALUES (%d, %d, %d, %s)' % (self.customerId, bill, discount, self.operatorId)
		return self.commitInsertQuery(qry)
	
	def recordProductsInReturn (self, saleId):
		for p in self.cart.products:
			qry = 'INSERT INTO productrefund (refundId, product, quantity, price, discount) VALUES (%s, %s, %s, %s, %s)' % (saleId, p.pid, p.qty, p.price, p.origPrice - p.price )
			self.commitInsertQuery(qry)
			
			qry = 'UPDATE `currentinventory` SET `quantity`=`quantity`+%s WHERE `productId` = %s' % (p.qty, p.pid)
			return self.commitInsertQuery(qry)
	
	def returnJournalEntry (self, returnId, bill, discount):
		af.returnEntry(bill, discount, returnId)
	# ========== Cash Sale =================================
	
	# ========== Invoice =================================
	def prepareInvoice (self, amtRecieved):
		if (len(self.cart.products) == 0):
			return
		
		bill = self.computeTotalBill()
		discount = self.computeTotalDiscount()
		
		invoiceId = self.recordInvoice(amtRecieved, bill, discount)
		self.recordProductsInInvoice(invoiceId)
		self.makeInvoice(invoiceId)
		self.makePrintout(invoiceId)
		self.invoiceSaleJournalEntry(invoiceId, bill, discount, amtRecieved)
		self.refresh()
	
	def recordInvoice (self, amtRecieved, bill, discount):
		qry = 'INSERT INTO invoice (employeeId, amount, amountRecieved, discount, buyerId) VALUES (%d, %d, "%s", %d, %d)' % (self.operatorId, bill, amtRecieved, discount, self.customerId)
		return self.commitInsertQuery(qry)
	
	def recordProductsInInvoice (self, invoiceId):
		for p in self.cart.products:
			qry = 'INSERT INTO productinvoice (invoiceId, product, quantity, price, discount) VALUES (%s, %s, %s, %s, %s)' % (invoiceId, p.pid, p.qty, p.price, p.origPrice - p.price )
			self.commitInsertQuery(qry)
			
			qry = 'UPDATE `currentinventory` SET `quantity`=`quantity`-%s WHERE `productId` = %s' % (p.qty, p.pid)
			return self.commitInsertQuery(qry)
		
	
	def invoiceSaleJournalEntry (self, invoiceId, bill, discount, amtRecieved):
		af.invoiceEntry (bill, discount, amtRecieved, self.customerId, invoiceId, cheque=1)
	
	def makeInvoice (self, invoiceId):
		prods = []
		for x in range(len(self.cart.products)):
			prods.append([self.cart.products[x].name, '', self.cart.products[x].qty, self.cart.products[x].origPrice, self.cart.products[x].price])
		im.imaker(str(invoiceId), invoiceId, self.operatorId, self.customerId, self.customerName, self.customerContact, prods, discountNo=0)
	
	def makePrintout(self, filename):
		cmd = "lpr -P HP-LaserJet-M101-M106 " + str(filename)
		os.system(cmd)

	# ========== Invoice =================================
	
	# ========== Quotation =================================
	def saveQuote (self, expDate):
		if (len(self.cart.products) == 0):
			return
		
		bill = self.computeTotalBill()
		discount = self.computeTotalDiscount()
		
		quoteId = self.recordQuote(bill, discount, expDate)
		self.recordProductsInQuotation(quoteId)
		
		self.refresh()
	
	def recordQuote (self, bill, discount, expDate):
		qry = 'INSERT INTO `quotations` (customer, totalBill, discount, preparedBy, expiryDate) VALUES (%s, %d, %d, %s, "%s")' % (self.customerId, bill, discount, self.operatorId, expDate)
		return self.commitInsertQuery(qry)
	
	def recordProductsInQuotation (self, quoteId):
		for p in self.cart.products:
			qry = 'INSERT INTO productquotes (quoteId, product, quantity, price, discount) VALUES (%s, %s, %s, %s, %s)' % (quoteId, p.pid, p.qty, p.price, p.origPrice - p.price)
			self.commitInsertQuery(qry)
	# ========== Quotation =================================
	
	# ========== Purchase =================================
	def purchaseItems (self, amountPaid):
		if (len(self.cart.products) == 0):
			return
		
		bill = self.computeTotalBill()
		discount = self.computeTotalDiscount()
		
		purchaseId = self.recordPurchase(amountPaid, bill, discount)
		self.recordProductsInPurchase(purchaseId)
		self.makePurchaseInvoice(purchaseId)
		self.purchaseJournalEntry (bill, discount, amountPaid, purchaseId)
		self.refresh()
		
	def recordPurchase (self, amountPaid, bill, discount):
		qry = 'INSERT INTO `purchase` (supplier, totalBill, discount, amountPaid, preparedBy) VALUES (%s, %s, %s, %s, %s)' % (self.supplierId, bill, discount, amountPaid, self.operatorId)
		return self.commitInsertQuery(qry)
	
	def recordProductsInPurchase (self, purchaseId):
		for p in self.cart.products:
			qry = 'INSERT INTO productpurchase (purchaseId, product, quantity, price, discount) VALUES (%s, %s, %s, %s, %s)' % (purchaseId, p.pid, p.qty, p.price, p.origPrice - p.price)
			self.commitInsertQuery(qry)
			
			qry = 'UPDATE `currentinventory` SET `quantity`=`quantity`+%s WHERE `productId` = %s' % (p.qty, p.pid)
			
			self.commitInsertQuery(qry)
	
	def makePurchaseInvoice (self, invoiceId):
		prods = []
		for x in range(len(self.cart.products)):
			prods.append([self.cart.products[x].name, '', self.cart.products[x].qty, self.cart.products[x].origPrice, self.cart.products[x].price])
		pim.imaker(str(invoiceId), invoiceId, self.operatorId, self.customerId, self.customerName, self.customerContact, prods, discountNo=0)
	
	def purchaseJournalEntry (self, bill, discount, amountPaid, purchaseId):
		af.purchaseEntry (bill, discount, amountPaid, self.supplierId, purchaseId)
	
	def returnPurchase (purchaseId):
		conn = connectToDB()
		
		qry = 'UPDATE purchase SET returned=1 WHERE id = %s' % (purchaseId)
		curs = conn.cursor()
		curs.execute(qry)
	
		af.purchaseReturnEntry(purchaseId)
	# ========== Purchase =================================

		



