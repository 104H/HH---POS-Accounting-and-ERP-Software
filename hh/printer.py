from escpos.printer import Usb
from escpos.exceptions import USBNotFoundError

import usb.core
import usb.util

def connectToPrinter():
	try:
		p = Usb(0x0416, 0x5011, in_ep=81, out_ep=3)
	except USBNotFoundError:
		p = None
		print("Printer not connected")
	return p

def printReciept(cart, date, invoiceId, bill, discount):
	p = connectToPrinter()
	
	if p is None:
		return None
	
	'''
	p.set(align='center', bold=True, double_height=True, double_width=True)
	#p.textln('Salman Wholeseller')

	p.set(align='center', bold=True, double_height=False, double_width=False)
	#p.textln('Chhadi Lane, Karachi')
	#p.textln('Phone: 0336 2510 211')
	#p.textln('-------------------------------------------')
	'''
	
	lines = [line.rstrip('\n') for line in open('data/recieptInfo.txt')]
	
	p.set(align='center', bold=True, double_height=True, double_width=True)
	p.textln(lines[:1])
	p.set(align='center', bold=True, double_height=False, double_width=False)
	for l in lines[1:]:
		p.textln(l)
	
	p.textln('===============================================')
	p.ln(1)
	p.textln('Invoice ID: '+str(invoiceId)+'         Date: '+ str(date))
	p.ln(2)

	p.set(align='center', bold=True, double_height=False, double_width=False)

	# width of paper -> 48 chars
	# Product
	p.textln("No |Product |Qty  |Price |Discount |Total Price ")
	p.textln("------------------------------------------------")

	for prd in cart:
		# if the name of the product exceeds 7 characters, print only the first 7
		if len(prd.name) > 7:
			nm = prd.name[:7]
		else:
			nm = prd.name
		p.textln(prepareLine(prd.pid, nm, prd.qty, prd.origPrice, (prd.origPrice - prd.price) * prd.qty, prd.price * prd.qty))
	#p.textln(prepareLine(4, 'Brush', 10, 200, 10000))
	
	'''
	p.textln("2   | Toothpick    | 50  |    20   |      1000  ")
	p.textln("578 | Battery      | 10  |   100   |      1000  ")
	p.textln("89  | Brush        |  5  |    40   |       200  ")
	'''
	
	p.textln("------------------------------------------------")
	p.textln("                            Total:  "+ str(bill + discount))
	p.textln("                         Discount: -"+ str(discount))
	p.textln("                   After Discount:  "+ str(bill))

	p.ln(9)

	p.textln("------------------------------------------------")
	p.textln("                     Notes                      ")

	p.ln(1)

	#p.set(align='center', bold=False, double_height=False, double_width=False)
	#p.textln("Ganyani, Kirmani and Allahwala IT Consulting")

	#p.image("logo.gif")
	#p.barcode('3422323', 'EAN13', 64, 2, '', '')

	p.cut(mode='PART')
	
def prepareLine (pid, name, qty, price, discount, tPrice):
	ln = ''
	pid = str(pid)
	ln = ln + preparePhrase(pid, 3)
	ln = ln + preparePhrase(name, 8)
	ln = ln + preparePhrase(qty, 5)
	ln = ln + preparePhrase(price, 6)
	ln = ln + preparePhrase(discount, 9)
	ln = ln + preparePhrase(tPrice, 10)
	
	return ln
	
def preparePhrase (itm, l):
	itm = str(itm)
	return itm + ' '*(l-len(itm)) + '|'

#p = connectToPrinter()
#printReciept(p)
