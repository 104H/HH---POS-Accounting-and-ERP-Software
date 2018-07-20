from reportlab.lib.pagesizes import letter


from datetime import datetime

def makeHeader(canvas):
	canvas.drawString(20,703,'Date')
	canvas.drawString(90,703,'Time')
	canvas.drawString(150,703,'Transaction')
	canvas.drawString(280,703,'Cheque No')
	canvas.drawString(360,703,'Debit')
	canvas.drawString(420,703,'Credit')
	canvas.drawString(480,703,'Balance')
	canvas.line(00,700,580,700)

def makeAccountStatement (holder, rows, date=datetime.now()):
	from reportlab.pdfgen import canvas
	date = str(date)

	canvas = canvas.Canvas("accounts/" + holder.replace('/', "") + ".pdf", pagesize=letter)
	canvas.setLineWidth(.3)
	canvas.setFont('Helvetica', 12)
	
	canvas.drawString(30,750, 'Account Statement of ' + holder)
	canvas.drawString(30,735, 'At ACME INDUSTRIES')
	canvas.drawString(420,750, date)

	# heading
	makeHeader(canvas)

	diff = 0
	for r in rows:
		verticalPos = 650-diff
		
		if verticalPos == 50:
			canvas.showPage()
			makeHeader(canvas)
			verticalPos = 650
			diff = 0
			
		
		canvas.drawString(20,verticalPos,r[0])
		canvas.drawString(90,verticalPos,r[1][:-1])
		canvas.drawString(150,verticalPos,r[2])
		canvas.drawString(280,verticalPos,r[3])
		canvas.drawString(360,verticalPos,r[4])
		canvas.drawString(420,verticalPos,r[5])
		canvas.drawString(480,verticalPos,r[6])
		
		diff = diff + 50
	
	canvas.save()


'''
canvas.drawString(150,650,'Carried Forward')
canvas.drawString(480,650,'1000')
canvas.drawString(30,600,'3-07-2018')
canvas.drawString(90,600,'3:55')
canvas.drawString(150,600,'Inv-31')
canvas.drawString(250,600,'MCB349')
canvas.drawString(340,600,'1323')
canvas.drawString(400,600,'')
canvas.drawString(480,600,'2323')

canvas.drawString(30,550,'8-07-2018')
canvas.drawString(90,550,'5:55')
canvas.drawString(150,550,'Inv-31')
canvas.drawString(250,550,'MCB345')
canvas.drawString(340,550,'1223')
canvas.drawString(400,550,'')
canvas.drawString(480,550,'3546')
'''

