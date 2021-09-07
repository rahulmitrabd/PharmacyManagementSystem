import mysql.connector
from reportlab.pdfgen import canvas
user_name="root"
pass_word=""
host_name="localhost"

def grabdata(b,c):
    print(b,c)
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    #data = c.execute("SELECT * FROM finalinvoice WHERE invoicedate BETWEEN %s AND %s;", (b, c))
    #data= c.execute("SELECT * FROM finalinvoice ;")
    data= c.execute("SELECT * FROM finalinvoice WHERE date BETWEEN %s AND %s;",(b, c))
    rows = c.fetchall()
    lsp=120

    pagin=0
    totalinvamnt=0
    for row in rows:
        if pagin<2:
            p.setFont("Courier-Bold", 8)
            p.drawString(45, lsp, str(row[1]))
            p.drawString(130, lsp, str(row[2]))
            p.drawString(200, lsp, str(row[4][0:21]))
            p.drawString(350, lsp, str(row[5]))
            p.drawString(450, lsp, str(row[6]))
            p.drawString(510, lsp, str(row[8]))
            p.drawString(40, lsp+7 , "-----------------------------------------------------------------------------------------------------------")
            lsp=lsp+20
            pagin=pagin+1
            print(row[1])
            totalinvamnt=totalinvamnt+row[8]
        else:
            pagin=0
            lsp=120
            print(row[1])
            print("---")
            p.showPage()
            invtemplate()
            p.setFont("Courier-Bold", 8)
            p.drawString(45, lsp, str(row[1]))
            p.drawString(130, lsp, str(row[2]))
            p.drawString(200, lsp, str(row[4][0:21]))
            p.drawString(350, lsp, str(row[5]))
            p.drawString(450, lsp, str(row[6]))
            p.drawString(510, lsp, str(row[8]))
            p.drawString(40, lsp + 7, "-----------------------------------------------------------------------------------------------------------")
            lsp=lsp+20
            totalinvamnt = totalinvamnt + row[8]
    print(totalinvamnt)



def geninvreport(m,n):
    global p
    p = canvas.Canvas("Purchase Report.pdf", pagesize=(595, 842), bottomup=0)
    invtemplate()
    grabdata(m,n)
    p.showPage()
    p.save()
    print(m)

def invtemplate():
    p.translate(10, 40)
    p.scale(1, -1)
    p.scale(1, -1)
    p.translate(-10, -40)
    p.setFont("Helvetica-Bold", 12)
    p.drawCentredString(300, 30, "Pharmacy Management System")
    #p.roundRect(30, 20, 530, 800, 2, stroke=1, fill=0)
    p.setFont("Helvetica-Bold", 8)
    p.drawCentredString(300, 45, "75, Annaya Residential Area, CHITTAGONG")
    p.drawCentredString(300, 55, "PHONE: 01748807540, 77884746")
    p.line(30, 65, 560, 65)
    p.roundRect(150, 70, 300, 15, 5, stroke=1, fill=0)
    p.setFont("Courier-Bold", 10)
    p.drawCentredString(300, 80, "Purchase Bill From 2021-06-03 to 2021-06-03")
    #p.roundRect(40, 155, 190, 22, 0, stroke=1, fill=0)
    #p.roundRect(235, 155, 150, 22, 0, stroke=1, fill=0)
    #p.roundRect(390, 155, 160, 22, 0, stroke=1, fill=0)
    #p.roundRect(40, 180, 345, 22, 0, stroke=1, fill=0)
    #p.roundRect(390, 180, 160, 22, 0, stroke=1, fill=0)
    #p.roundRect(40, 210, 510, 550, 0, stroke=1, fill=0)
    #p.line(40, 230, 550, 230)

    #p.line(80, 210, 80, 760)
    #p.line(400, 210, 400, 760)
    #p.line(460, 210, 460, 760)
    #p.setFont("Times-Bold", 10)
    p.drawString(45, 100, "Invoice")
    p.drawString(130, 100, "Date")
    p.drawString(220, 100, "Supplier")
    p.drawString(350, 100, "Item")
    p.drawString(450, 100, "Quantity")
    p.drawString(510, 100, "Price")
    p.drawCentredString(300, 800, "--------------------------------------------------------------------------------")
    p.drawCentredString(300, 810, "This is software generated purchase report")
f=""
g=""
geninvreport(f, g)