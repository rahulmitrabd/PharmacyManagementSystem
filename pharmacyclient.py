from tkinter import *
import tkinter
import mysql.connector
elements = []
global loginstatus
import sys
import os
import datetime
import time
global date1
date1="2020-09-15"
global date2
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
global ipset
ipset="localhost"
usr_name="root"
pass_word=""
date2="2020-09-15"
doc = SimpleDocTemplate("report.pdf")
data1=[("__MED__ID__","____MED__NAME___","___IN STOCK (PCS)____","___TOTAL SOLD (PCS)__")]

def dumpreport():
    conn = mysql.connector.connect(
        host=ipset,
        user=usr_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    data = c.execute("DELETE FROM `rep`")

    conn.commit()
    conn.close()
def getting_instock(f1):
    conn = mysql.connector.connect(
        host=ipset,
        user=usr_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    data = c.execute("SELECT instock FROM med WHERE medname=%s",(f1,))
    rows = c.fetchone()[0]
    #print(rows)
    return rows
def getting_meddata(b1,b2,b3):
    m1=str(b1)
    m2 = str(b2)
    m3 = str(b3)

    conn = mysql.connector.connect(
        host=ipset,
        user=usr_name,
        password=pass_word,
        database="ncpharmacy"
    )
    state="0"
    c = conn.cursor()
    data = c.execute("SELECT SUM(quantity) FROM finalbill WHERE medname=%s AND status =%s AND date BETWEEN %s AND %s;", (m1,state,m2,m3,))
    rowse = c.fetchone()
    #print(rowse)
    return rowse[0]
def getting_medid(g1):
    conn = mysql.connector.connect(
        host=ipset,
        user=usr_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    data = c.execute("SELECT medid FROM med WHERE medname=%s", (g1,))
    rows = c.fetchone()[0]
    # print(rows)
    return rows
def inputmedname(e1):
    conn = mysql.connector.connect(
        host=ipset,
        user=usr_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    data = c.execute("INSERT INTO rep (medname) VALUES (%s)", (e1,))
    conn.commit()
def inputstock(r1,r2):
    conn = mysql.connector.connect(
        host=ipset,
        user=usr_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    data = c.execute("UPDATE rep SET instock = %s WHERE medname = %s", (r1,r2))
    conn.commit()

def inputmedid(r1,r2):
    conn = mysql.connector.connect(
        host=ipset,
        user=usr_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    data = c.execute("UPDATE rep SET medid = %s WHERE medname = %s", (r1,r2))
    conn.commit()

def inputmeddata(r1,r2):
    conn = mysql.connector.connect(
        host=ipset,
        user=usr_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    data = c.execute("UPDATE rep SET sold = %s WHERE medname = %s", (r1,r2))
    conn.commit()
def createpdf():
    conn = mysql.connector.connect(
        host=ipset,
        user=usr_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    data = c.execute("SELECT * FROM rep ")
    rows = c.fetchall()
    # print(rows)
    for row in rows:
        # print(row)
        data1.append(row)
    # print(data1)
    # data1= [['00', '010000', '02', '03', '04','10', '11', '12', '13', '14'],
    #  ['10', '11', '12', '13', '14', '10', '11', '12', '13', '14'],
    #  ['20', '21', '22', '23', '24', '10', '11', '12', '13', '14'],
    #  ['30', '31', '32', '33', '34', '10', '11', '12', '13', '14']]

    t1 = Table(data1)
    t1.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                            ('BOX', (0, 0), (-1, -1), 1, colors.black),
                            ]))

    data2 = [[x] for x in range(40)]

    # t2=Table(data2)
    # t2.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    #                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    #                       ]))

    elements.append(t1)
    # elements.append(t2)

    doc.build(elements)
def getting_mednames(y1,y2):
    dumpreport()
    global date1
    date1= y1
    global date2
    date2 = y2
    conn = mysql.connector.connect(
        host=ipset,
        user=usr_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    data = c.execute("SELECT medname FROM med")
    rows = c.fetchall()
    for row in rows:
        medids=getting_medid(row[0])
        inputmedname(row[0])
        inputmedid(medids,row[0])
        medstk=getting_instock(row[0])
        inputstock(medstk,row[0])
        meddata=getting_meddata(row[0],date1,date2)
        inputmeddata(meddata,row[0])
    createpdf()
def openpdffile(btndata):
    print(btndata)
    filename = str(btndata) + '.pdf'
    try:
        os.startfile(filename)
    except:
        messagebox.showinfo("Error","No Bill Found. Please try After Generating This Bill ")

from tkinter import messagebox
from reportlab.pdfgen import canvas
#ptn_name="Rahul"
loginstatus = 1
root = tkinter.Tk()
# root = ThemedTk(theme="arc")
p1 = PhotoImage(file='fav2.png')
root.iconphoto(False, p1)
root.title('Stock Management application Developed By IT Solution BD')
root.resizable(width=False, height=False)
root.geometry('{}x{}'.format(1000, 500))
#regi_no="eer"
#cbn_no="56"
#date="asda"
def getbilldata():
    conn = mysql.connector.connect(
        host=ipset,
        user=usr_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    data = c.execute("SELECT * FROM finalbill WHERE billno=%s", (slno,))
    rows = c.fetchall()
    # print(rows[1][3])
    # global slno
    # slno = rows[0][1]
    linesp = 250
    serialno = 1
    global date
    date = rows[0][8]
    # print(date)
    p.setFont("Times-Bold", 11)
    for row in rows:
        # print(row[4])
        # print(row[5])
        # print(row[6])

        p.drawRightString(65, linesp, str(serialno))
        p.drawString(110, linesp, row[4])
        p.drawCentredString(430, linesp, str(row[5]))
        p.drawCentredString(500, int(linesp), str(row[7]))
        linesp = linesp + 20
        serialno = serialno + 1

def get_ptn_info():
    conn = mysql.connector.connect(
        host=ipset,
        user=usr_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    ptn = c.execute("SELECT cabinno,patientname FROM patient WHERE regno=%s;",(regi_no,))
    ptn_info=c.fetchone()
    print(ptn_info)
    global ptn_name
    ptn_name = ptn_info[1]
    global cbn_no
    cbn_no = ptn_info[0]
def getbillinfo(b1):
    global slno
    slno=str(b1)
    conn = mysql.connector.connect(
        host=ipset,
        user=usr_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    data = c.execute("SELECT billno,regid,date FROM finalbill WHERE billno=%s;",(slno,))
    getdata = c.fetchone()
    global regi_no
    regi_no = getdata[1]
    global date
    date=getdata[2]
    print(regi_no)
    print(getdata)
    get_ptn_info()
def totalbillfinal():
    conn = mysql.connector.connect(
        host=ipset,
        user=usr_name,
        password=pass_word,
        database="ncpharmacy"
    )

    c = conn.cursor()
    data = c.execute("SELECT SUM(total) AS totalbill FROM finalbill WHERE billno=%s;",(slno,))
    getdata = c.fetchone()[0]
    # print(getdata)
    p.drawCentredString(500, 775, str(getdata))
    p.drawRightString(460, 775, "Total Bill : ")

def billgenerator(v1):
    getbillinfo(v1)
    global p
    p = canvas.Canvas(slno + ".pdf", pagesize=(595, 842), bottomup=0)
    p.translate(10, 40)
    p.scale(1, -1)
    p.scale(1, -1)
    p.translate(-10, -40)
    p.setFont("Helvetica-Bold", 30)
    p.drawCentredString(300, 60, "Pharmacy Management System")
    p.roundRect(30, 20, 530, 800, 2, stroke=1, fill=0)
    p.setFont("Helvetica-Bold", 12)
    p.drawCentredString(300, 80, "75, Annaya Residential Area, CHITTAGONG")
    p.drawCentredString(300, 95, "PHONE: 01748807540, 8938493849")
    p.line(30, 110, 560, 110)
    p.roundRect(200, 120, 200, 20, 10, stroke=1, fill=0)
    p.setFont("Courier-Bold", 15)
    p.drawCentredString(300, 134, "Medicine Bill")
    p.roundRect(40, 155, 190, 22, 0, stroke=1, fill=0)
    p.roundRect(235, 155, 150, 22, 0, stroke=1, fill=0)
    p.roundRect(390, 155, 160, 22, 0, stroke=1, fill=0)
    p.roundRect(40, 180, 345, 22, 0, stroke=1, fill=0)
    p.roundRect(390, 180, 160, 22, 0, stroke=1, fill=0)
    p.roundRect(40, 210, 510, 550, 0, stroke=1, fill=0)
    p.line(40, 230, 550, 230)
    p.setFont("Times-Bold", 12)
    p.drawRightString(120, 170, "Serial NO :")
    p.drawString(130, 170, slno)
    p.drawString(65, 194, "Name :")
    p.drawString(130, 194, str(ptn_name))
    p.drawRightString(300, 170, "Reg. No :")
    p.drawString(310, 170, str(regi_no))
    p.drawRightString(450, 170, "Cabin No :")
    p.drawString(460, 170, str(cbn_no))
    p.drawRightString(450, 194, "Date :")
    p.drawString(460, 194, str(date))
    p.line(80, 210, 80, 760)
    p.line(400, 210, 400, 760)
    p.line(460, 210, 460, 760)
    p.setFont("Times-Bold", 11)
    p.drawString(45, 223, "SL No")
    p.drawString(210, 223, "Description")
    p.drawString(410, 223, "Quantity")
    p.drawString(480, 223, "Amount")
    p.drawCentredString(100, 800, "-----------------------------")
    p.drawCentredString(100, 810, "Receiver's Signature")
    p.roundRect(400, 762, 150, 20, 5, stroke=1, fill=0)
    getbilldata()

    totalbillfinal()
    p.showPage()
    # Saving the PDF
    p.save()
    print("SA")
    bill_no.delete(0,END)
    messagebox.showinfo("Notification","Bill Generated")


def search_bill():
    global clearframe
    clearframe = Frame(content_frame,
                       width=785, height=423,
                       highlightbackground="red",
                       highlightthickness=1)
    clearframe.grid(row=0, column=1, padx=0, pady=0)
    clearframe.grid_propagate(False)

    bill_frm = LabelFrame(clearframe,
                              text="Search Bill",
                              width=775, height=80,
                              highlightbackground="#bdbdbd",
                              highlightthickness=0
                              )
    bill_frm.grid(row=0, column=0, pady=5, padx=5)
    bill_frm.grid_propagate(False)
    bill_no_lbl = Label(bill_frm, text="Registration NO : ", width=20, font=("Arial", 12))
    bill_no_lbl.grid(row=0, column=0, pady=5, padx=5, sticky="W")
    global bill_no
    bill_no = Entry(bill_frm, font=("Arial", 12))
    bill_no.grid(row=0, column=1, pady=5, padx=5)
    save_patient = Button(
        bill_frm,
        text="Search",
        height=1,
        width=25,
        command=lambda: search_result(bill_no.get())
    )
    save_patient.grid(row=0, column=2, padx=20)

def search_result(d1):
    result_frm = LabelFrame(clearframe,
                          text="Results",
                          width=775, height=350,
                          highlightbackground="#bdbdbd",
                          highlightthickness=0
                          )
    result_frm.grid(row=2, column=0, pady=5, padx=5)
    result_frm.grid_propagate(False)
    conn = mysql.connector.connect(
        host=ipset,
        user=usr_name,
        password=pass_word,
        database="ncpharmacy"
    )
    status = 0
    billdata = []
    c = conn.cursor()
    data = c.execute("SELECT billno FROM finalbill WHERE regid=%s AND status =%s", (str(d1), status,))
    rows = c.fetchall()
    for row in rows:
        billno = row[0]
        # print(billno)
        if billno not in billdata:
            billdata.append(billno)
    datano = 0
    for bills in billdata:
        for i in range(0, 8):
            for j in range(0, 5):
                print(j)
                prev_bill_btn = Button(
                    result_frm,
                    text="Bill No: " + str(billdata[datano]),
                    height=1,
                    width=20,
                    command=lambda i=datano: openpdffile(billdata[i])
                )

                prev_bill_btn.grid(row=i, column=j, padx=2, pady=2)
                datano = datano + 1


def report_gen():
    clearframe = Frame(content_frame,
                       width=785, height=423,
                       highlightbackground="black",
                       highlightthickness=1)
    clearframe.grid(row=0, column=1, padx=0, pady=0)
    clearframe.grid_propagate(False)

    gen_bill_frm = LabelFrame(clearframe,
                              text="Generate Bill",
                              width=775, height=100,
                              highlightbackground="#bdbdbd",
                              highlightthickness=0
                              )
    gen_bill_frm.grid(row=0, column=0, pady=5, padx=5)
    gen_bill_frm.grid_propagate(False)
    from_date_lbl = Label(gen_bill_frm, text="From : ", width=10, font=("Arial", 12))
    from_date_lbl.grid(row=0, column=0, pady=5, padx=5, sticky="W")
    global from_date
    from_date = Entry(gen_bill_frm, font=("Arial", 12))
    from_date.grid(row=0, column=1, pady=5, padx=5)


    to_date_lbl = Label(gen_bill_frm, text="To : ", width=5, font=("Arial", 12))
    to_date_lbl.grid(row=0, column=2, pady=5, padx=5, sticky="W")
    global to_date
    to_date = Entry(gen_bill_frm, font=("Arial", 12))
    to_date.grid(row=0, column=3, pady=5, padx=5)

    save_patient = Button(
        gen_bill_frm,
        text="Generate Report",
        height=1,
        width=25,
        command=lambda: getting_mednames(from_date.get(),to_date.get())
    )

    save_patient.grid(row=0, column=4, padx=20)

def create_bill():
    print("create bill")
    clearframe = Frame(content_frame,
                          width=785, height=423,
                          highlightbackground="black",
                          highlightthickness=1)
    clearframe.grid(row=0, column=1, padx=0, pady=0)
    clearframe.grid_propagate(False)

    gen_bill_frm = LabelFrame(clearframe, 
                            text="Generate Bill",
                            width=775,height=80,
                            highlightbackground="#bdbdbd",
                            highlightthickness=0
                            )
    gen_bill_frm.grid(row=0,column=0,pady=5, padx=5)
    gen_bill_frm.grid_propagate(False)

    bill_no_lbl = Label(gen_bill_frm, text="Enter Bill Number : ", width=20,font=("Arial", 12))
    bill_no_lbl.grid(row=0, column=0, pady=5, padx=5,sticky="W")
    global bill_no
    bill_no = Entry(gen_bill_frm,font=("Arial", 12))
    bill_no.grid(row=0, column=1, pady=5, padx=5)
    save_patient=Button(
                gen_bill_frm,
                text="Search",
                height=1,
                width=25,
                command=lambda: billgenerator(bill_no.get())
                )

    save_patient.grid(row=0,column=2,padx=20)

    


main_container=Frame(root,
                        width=990,height=490,
                        highlightbackground="#bdbdbd",
                        highlightthickness=1)
main_container.grid(row=0,column=0, padx=5,pady=5)
main_container.grid_propagate(False)


banner_container=Frame(main_container,
                        width=988,height=60,
                        bg = "black",
                        highlightbackground="red",
                        highlightthickness=0)
banner_container.grid(row=0,column=0, padx=0,pady=0)
banner_container.grid_propagate(False)
tool_container=Frame(main_container,
                        width=988,height=425,
                        highlightbackground="blue",
                        highlightthickness=0)
tool_container.grid(row=1,column=0, padx=0,pady=0)
tool_container.grid_propagate(False)

left_btn_container=Frame(tool_container,
                        width=200,height=423,
                        highlightbackground="red",
                        highlightthickness=0)
left_btn_container.grid(row=0,column=0, padx=0,pady=0)
left_btn_container.grid_propagate(False)
global content_frame
content_frame=Frame(tool_container,
                        width=785,height=423,
                        highlightbackground="red",
                        highlightthickness=0)
content_frame.grid(row=0,column=1, padx=0,pady=0)
content_frame.grid_propagate(False)

btncreate_bill=Button(
                left_btn_container,
                text="Create Bill",
                height=3,
                width=25,
                command=create_bill
                )
btncreate_bill.grid(row=0,column=0,padx=5,pady=5)

search_bill=Button(
                left_btn_container,
                text="Search Bill",
                height=3,
                width=25,
                command=search_bill
                )
search_bill.grid(row=1,column=0,padx=5,pady=5)



report_btn=Button(
                left_btn_container,
                text="Report",
                height=3,
                width=25,
                command=report_gen
                )
report_btn.grid(row=2,column=0,padx=5,pady=5)




#getbilldata()
root.mainloop()