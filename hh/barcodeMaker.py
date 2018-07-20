from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

#I"ll be generating code39 barcodes, others are available
from reportlab.graphics.barcode import code39

def makeBarcodeFile (brc, width, height):
	brc = str(brc)
	width = float(width) * mm
	height = float(height) * mm
	# generate a canvas (A4 in this case, size doesn"t really matter)
	c=canvas.Canvas(brc+".pdf",pagesize=A4)
	# create a barcode object
	# (is not displayed yet)
	# The encode text is "123456789"
	# barHeight encodes how high the bars will be
	# barWidth encodes how wide the "narrowest" barcode unit is
	barcode=code39.Extended39(brc, barWidth=width*mm, barHeight=height*mm)
	# drawOn puts the barcode on the canvas at the specified coordinates
	
	x, y = (10*mm, 10*mm)
	while y + barcode.height < 290*mm:
		while x + barcode.width < 200*mm:
			barcode.drawOn(c, x, y)
			x = x + (1 + barcode.width)
		x = 10*mm
		y = y + (1 + barcode.height)*mm 

	# now create the actual PDF
	c.showPage()
	c.save()

makeBarcodeFile("ACSCS", .05, 3)
