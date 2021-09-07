from tkinter import *
import tkinter
from tkinter.ttk import Treeview

import mysql.connector

global loginstatus
import sys
import os
import datetime
import time
import tkinter.font as font
from datetime import date

# from ttkthemes import ThemedTk
global today
today = date.today()
actbg = "#002975"
actfg = "yellow"
ntactbg = "#e9ffde"
ntactfg = "black"
user_name="root"
pass_word="admin"
host_name="localhost"
from tkinter import ttk
import pandas as pd
from tkinter import messagebox
from reportlab.pdfgen import canvas

loginstatus = 1
root = tkinter.Tk()
# root = ThemedTk(theme="arc")
p1 = PhotoImage(file='fav2.png')
root.iconphoto(False, p1)

scrwidth = root.winfo_screenwidth()
scrheight = root.winfo_screenheight()
posx = 0
posy = 0
global slno
slno = 0
conn = mysql.connector.connect(
   user=user_name,
   password=pass_word,
   database="ncpharmacy"
)
# margincenter=((scrwidth-1366)/2)
margincenter = 0
root.title('Stock Management application Developed By IT Solution BD')
root.resizable(width=True, height=True)
root.geometry('{}x{}+{}+{}'.format(1366, 768, posx, posy))
# image = photoimage,
# compound = LEFT
# =============functions=================
__version__ = "1.0.1"

tkinter_umlauts = ['odiaeresis', 'adiaeresis', 'udiaeresis', 'Odiaeresis', 'Adiaeresis', 'Udiaeresis', 'ssharp']


class AutocompleteEntry(tkinter.Entry):
    """
    Subclass of tkinter.Entry that features autocompletion.

    To enable autocompletion use set_completion_list(list) to define
    a list of possible strings to hit.
    To cycle through hits use down and up arrow keys.
    """

    def set_completion_list(self, completion_list):
        self._completion_list = completion_list
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)

    def autocomplete(self, delta=0):
        """autocomplete the Entry, delta may be 0/1/-1 to cycle through possible hits"""
        if delta:  # need to delete selection otherwise we would fix the current position
            self.delete(self.position, tkinter.END)
        else:  # set position to end so selection starts where textentry ended
            self.position = len(self.get())
        # collect hits
        _hits = []
        for element in self._completion_list:
            if element.lower().startswith(self.get().lower()):
                _hits.append(element)

        # if we have a new hit list, keep this in mind
        if _hits != self._hits:
            self._hit_index = 0
            self._hits = _hits
        # only allow cycling if we are in a known hit list
        if _hits == self._hits and self._hits:
            self._hit_index = (self._hit_index + delta) % len(self._hits)
        # now finally perform the auto completion
        if self._hits:
            self.delete(0, tkinter.END)
            self.insert(0, self._hits[self._hit_index])
            self.select_range(self.position, tkinter.END)

    def handle_keyrelease(self, event):
        """event handler for the keyrelease event on this widget"""
        if event.keysym == "BackSpace":
            if self.position < self.index(tkinter.END):  # delete the selection
                self.delete(self.position, tkinter.END)
            else:
                self.position = self.index(tkinter.END)
        if event.keysym == "Left":
            if self.position < self.index(tkinter.END):  # delete the selection
                self.delete(self.position, tkinter.END)
        if event.keysym == "Right":
            self.position = self.index(tkinter.END)  # go to end (no selection)
        if event.keysym == "Down":
            self.autocomplete(1)  # cycle to next hit
        if event.keysym == "Up":
            self.autocomplete(-1)  # cycle to previous hit
        # perform normal autocomplete if event is a single key or an umlaut
        if len(event.keysym) == 1:
            self.autocomplete()


def test(test_list):
    """Run a mini application to test the AutocompleteEntry Widget."""
    # root = tkinter.Tk(className=' AutocompleteEntry demo')
    # entry = AutocompleteEntry(root)
    # entry.set_completion_list(test_list)
    # entry.pack()
    # entry.focus_set()
    # root.mainloop()


if __name__ == '__main__':
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    mednames = []
    c = conn.cursor()
    data = c.execute("SELECT * FROM med")
    rows = c.fetchall()
    for row in rows:
        # print(row[1])
        mednames.append(row[1])
    # print(mednames)
    test_list = mednames
    test(test_list)


def login():
    loginstatus = 1
    if (loginstatus == 1):
        loginbtn = Button(maincontainer, text="login", height=5, width=50, command=login)
        loginbtn.grid(row=1, column=0)
    else:
        logoutbtn = Button(maincontainer, text="Logout", height=5, width=50, command=logout)
        logoutbtn.grid(row=1, column=0)


def logout():
    loginstatus = 0
    if (loginstatus == 1):
        loginbtn = Button(maincontainer, text="login", height=5, width=50, command=login)
        loginbtn.grid(row=1, column=0)
    else:
        logoutbtn = Button(maincontainer, text="Logout", height=5, width=50, command=logout)
        logoutbtn.grid(row=1, column=0)


def openpdffile(btndata):
    print(btndata)
    filename = str(btndata) + '.pdf'
    os.startfile(filename)
def opensummaryfile():
    filename = 'Summary Bill.pdf'
    os.startfile(filename)

def save_medicine_to_database(m1, m2, m3, m4, m5):
    if len(m1) != 0:
        if len(m5) != 0:
            if len(m4) != 0:
                conn = mysql.connector.connect(
                    host=host_name,
                    user=user_name,
                    password=pass_word,
                    database="ncpharmacy"
                )
                c = conn.cursor()
                med_details = [m1, m3, m5, m2, m4]
                c.execute("INSERT INTO med (medname,medgroup, medprice, medcompany,instock) VALUES (%s,%s,%s,%s,%s)",
                          (med_details))
                conn.commit()
                # print ("Sucessfully submitted data")
                conn.close()
                med_name.delete(0, END)
                selling_price.delete(0, END)
                group_name.delete(0, END)
                com_name.delete(0, END)
                med_qnty.delete(0, END)

            else:
                messagebox.showinfo("Error", "Please Input Stock")

        else:
            messagebox.showinfo("Error", " Please input Medicine price")


    else:
        messagebox.showinfo("Error", "Please Enter Medicine Name")


def totalbillfinal():
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )

    c = conn.cursor()
    data = c.execute("SELECT SUM(total) AS totalbill FROM tempbill;")
    getdata = c.fetchone()[0]
    # print(getdata)
    p.drawCentredString(500, 775, str(getdata))
    p.drawRightString(460, 775, "Total Bill : ")


def stocksub():
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )

    c = conn.cursor(buffered=True)
    rows = c.execute("SELECT * FROM tempbill")
    data = c.fetchall()
    for row in data:
        item = row[0]
        # print(item)
        # stk_check=c.execute("SELECT * FROM med WHERE medname=%s", (item,))
        # in_stock = int(c.fetchone()[5])
        red_qnty = c.execute("SELECT medname,quantity FROM tempbill WHERE slno=%s", (item,))
        red_qnty = c.fetchall()
        for rt in red_qnty:
            stk_check = c.execute("SELECT instock FROM med WHERE medname=%s", (rt[0],))
            in_stock = int(c.fetchone()[0])
            new_stk = (int(in_stock) - int(rt[1]))
            print(in_stock)
            print(rt[1])
            print(new_stk)
            update_stock = c.execute("UPDATE med SET instock = %s WHERE medname =%s", (new_stk, rt[0],))
            conn.commit()
    generatebill()


def savetofinalbill():
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    data = c.execute(
        "INSERT INTO finalbill (billno,regid,medid,medname,quantity,rate,total) SELECT billno,regid,medid,medname,quantity,rate,total FROM tempbill")
    conn.commit()
    billnoupdate()
    totalbillpreview_amnt.config(text="000")


def billnogenerator():
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )

    c = conn.cursor()
    getlastnumber = c.execute("SELECT billno FROM finalbill ORDER BY slno DESC LIMIT 1 ")
    rows = c.fetchone()
    # print(rows[0])
    previnvoice = int(rows[0])
    global slno
    slno = (previnvoice + 1)


# print(slno)
# dt=datetime.datetime.today()
# year=str(dt.year)
# month=str(dt.month)
# day=str(dt.day)
# hour=str(dt.hour)
# minute=str(dt.minute)
# second=str(dt.second)
# global slno
# slno=year+month+day+hour+minute+second
def billnoupdate():
    serial_no.config(text=slno)


def getslno():
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    data = c.execute("SELECT * FROM tempbill")
    rows = c.fetchall()
    # print(rows[1][3])
    global slno
    slno = rows[0][1]


def getnames():
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    data = c.execute("SELECT * FROM patient WHERE regno=%s", (regno,))
    rows = c.fetchall()

    global ptn_name
    global cbn_no
    global phn_no
    global regi_no
    ptn_name = rows[0][4]
    cbn_no = rows[0][2]
    phn_no = rows[0][3]
    regi_no = rows[0][1]


def getbilldata():
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    data = c.execute("SELECT * FROM tempbill")
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


# print(slno)

def modtofinal():
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    data = c.execute(
        "INSERT INTO finalbill (billno,regid,medid,medname,quantity,rate,total) SELECT billno,regid,medid,medname,quantity,rate,total FROM tempbill")
    conn.commit()
    billnoupdate()
    totalbillpreview_amnt.config(text="000")


def generatebill():
    savetofinalbill()
    getnames()
    getslno()

    # Creating Canvas

    global p
    p = canvas.Canvas(slno + ".pdf", pagesize=(595, 842), bottomup=0)
    getbilldata()
    totalbillfinal()
    p.translate(10, 40)
    p.scale(1, -1)
    p.scale(1, -1)
    p.translate(-10, -40)
    p.setFont("Helvetica-Bold", 30)
    p.drawCentredString(300, 60, "Pharmacy management system")
    p.roundRect(30, 20, 530, 800, 2, stroke=1, fill=0)
    p.setFont("Helvetica-Bold", 12)
    p.drawCentredString(300, 80, "75, Annaya Residential, CHITTAGONG")
    p.drawCentredString(300, 95, "PHONE: 01748807540, 4958868888")
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
    p.showPage()
    # Saving the PDF
    p.save()
    dumptempbill()
    updatetempbill()
    btnstatechk()
    billnogenerator()
    billnoupdate()
    screate_bill()


def add_medicine():
    check_bill.configure(bg=ntactbg, fg=ntactfg)
    edit_medicine.configure(bg=ntactbg, fg=ntactfg)
    edit_patient.configure(bg=ntactbg, fg=ntactfg)
    print_bill.configure(bg=ntactbg, fg=ntactfg)
    btncreate_bill.configure(bg=ntactbg, fg=ntactfg)
    add_patient.configure(bg=ntactbg, fg=ntactfg)
    add_medicine.configure(bg=actbg, fg=actfg)
    search_medicine_container = Frame(rightcontainer,
                                  width=1145, height=587,
                                  highlightbackground="#bdbdbd",
                                  highlightthickness=1)
    search_medicine_container.grid(row=0, column=0, padx=5, pady=5)
    search_medicine_container.grid_propagate(False)

    med_selection = LabelFrame(search_medicine_container,
                                   text="Add Medicine",
                                   width=1130, height=250,
                                   highlightbackground="#bdbdbd",
                                   highlightthickness=0,
                                    bg="#eaf2d0"
                                   )
    med_selection.grid(row=1, column=0, pady=5, padx=5)
    med_selection.grid_propagate(False)
    med_info = LabelFrame(search_medicine_container,
                              text="Add Suppliers",
                              width=1130, height=150,
                              highlightbackground="#bdbdbd",
                              highlightthickness=0,
                          bg="#d0edf2"
                              )
    med_info.grid(row=2, column=0, pady=5, padx=5)
    med_info.grid_propagate(False)

    #=====================
    s_name_lbl = Label(med_info, text="Medicine Name: ", width=20, font=("Arial", 12))
    s_name_lbl.grid(row=1, column=0, pady=5, padx=5, sticky="W")
    global s_name
    s_name = Entry(med_info, font=("Arial", 12), border=1, relief="solid")
    s_name.grid(row=1, column=1, pady=5, padx=5)
    global s_contact
    s_contact_lbl = Label(med_info, text="Contact: ", width=20, font=("Arial", 12))
    s_contact_lbl.grid(row=2, column=0, pady=5, padx=5, sticky="W")

    s_contact = Entry(med_info, font=("Arial", 12), border=1, relief="solid")
    s_contact.grid(row=2, column=1, pady=5, padx=5)

    s_email_lbl = Label(med_info, text="Email:  ", width=20, font=("Arial", 12))
    s_email_lbl.grid(row=1, column=2, pady=5, padx=5, sticky="W")
    global s_email
    s_email = Entry(med_info, font=("Arial", 12), border=1, relief="solid")
    s_email.grid(row=1, column=3, pady=5, padx=5)

    s_address_lbl = Label(med_info, text="Supplier's Address: ", width=20, font=("Arial", 12))
    s_address_lbl.grid(row=2, column=2, pady=5, padx=5, sticky="W")
    global s_address
    s_address = Entry(med_info, font=("Arial", 12), border=1, relief="solid")
    s_address.grid(row=2, column=3, pady=5, padx=5)
    save_supplier = Button(
        med_info,
        text="Save Supplier",
        height=2,
        width=25,
        command=lambda: save_supplier_to_database(
            s_name.get(),
            s_contact.get(),
            s_email.get(),
            s_address.get()
        )
        , border=1, relief="solid", bg="green", fg="yellow"
    )

    save_supplier.grid(row=4, column=3)

    #======================

    #med_name_lbl = Label(med_selection, text="Medicine Name: ", width=20, font=("Arial", 10))
    #med_name_lbl.grid(row=0, column=0, pady=10, padx=5, sticky="W")
    #med_name = Entry(med_selection, font=("Arial", 10))
    #med_name.grid(row=0, column=1, pady=10, padx=5)
    global med_name
    global selling_price
    global com_name
    global group_name
    #add_medicine_container = Frame(
    #    rightcontainer,
    #    width=1145, height=587,
    #    highlightbackground="#bdbdbd",
    #    highlightthickness=1
    #)

    #add_medicine_container.grid(row=0, column=0, padx=5, pady=5)
    #add_medicine_container.grid_propagate(False)

    #sampletext = Label(add_medicine_container, text="Add Medicine Page")
    #sampletext.grid(row=0, column=0, padx=5)
    #sampletext.config(font=("Times new roman", 20))

    med_name_lbl = Label(med_selection, text="Medicine Name: ", width=20, font=("Arial", 12))
    med_name_lbl.grid(row=1, column=0, pady=5, padx=5, sticky="W")

    med_name = Entry(med_selection, font=("Arial", 12),border=1,relief="solid")
    med_name.grid(row=1, column=1, pady=5, padx=5)

    com_name_lbl = Label(med_selection, text="Supplier's Name: ", width=20, font=("Arial", 12))
    com_name_lbl.grid(row=2, column=0, pady=5, padx=5, sticky="W")

    com_name = Entry(med_selection, font=("Arial", 12),border=1,relief="solid")
    com_name.grid(row=2, column=1, pady=5, padx=5)

    group_name_lbl = Label(med_selection, text="Group Name: ", width=20, font=("Arial", 12))
    group_name_lbl.grid(row=2, column=2, pady=5, padx=5, sticky="W")

    group_name = Entry(med_selection, font=("Arial", 12),border=1,relief="solid")
    group_name.grid(row=2, column=3, pady=5, padx=5)

    med_qnty_lbl = Label(med_selection, text="Quantity: ", width=20, font=("Arial", 12))
    med_qnty_lbl.grid(row=3, column=0, pady=5, padx=5, sticky="W")
    global med_qnty
    med_qnty = Entry(med_selection, font=("Arial", 12),border=1,relief="solid")
    med_qnty.grid(row=3, column=1, pady=5, padx=5)

    selling_price_lbl = Label(med_selection, text="Selling Price: ", width=20, font=("Arial", 12))
    selling_price_lbl.grid(row=3, column=2, pady=5, padx=5, sticky="W")

    selling_price = Entry(med_selection, font=("Arial", 12),border=1,relief="solid")
    selling_price.grid(row=3, column=3, pady=5, padx=5)

    save_medicine = Button(
        med_selection,
        text="Save",
        height=2,
        width=25,
        command=lambda: save_medicine_to_database(
            med_name.get(),
            com_name.get(),
            group_name.get(),
            med_qnty.get(),
            selling_price.get()
        )
        , border=1, relief="solid", bg="green",fg="yellow"
    )

    save_medicine.grid(row=4, column=3)

def save_supplier_to_database(h,j,k,l):
    if len(h) != 0:
        if len(j) != 0:
            if len(k) != 0:
                conn = mysql.connector.connect(
                    host=host_name,
                    user=user_name,
                    password=pass_word,
                    database="ncpharmacy"
                )
                c = conn.cursor()
                med_details = [h, j, k, l]
                c.execute("INSERT INTO supplier (sname,scontact, semail, saddress) VALUES (%s,%s,%s,%s)",
                          (med_details))
                conn.commit()
                # print ("Sucessfully submitted data")
                conn.close()
                s_name.delete(0,END)
                s_contact.delete(0,END)
                s_email.delete(0,END)
                s_address.delete(0,END)


            else:
                messagebox.showinfo("Error", "Please Input Email")

        else:
            messagebox.showinfo("Error", " Please input Contact Number")


    else:
        messagebox.showinfo("Error", "Please Enter Supplier's Name")


def add_patient():
    check_bill.configure(bg=ntactbg, fg=ntactfg)
    edit_medicine.configure(bg=ntactbg, fg=ntactfg)
    edit_patient.configure(bg=ntactbg, fg=ntactfg)
    print_bill.configure(bg=ntactbg, fg=ntactfg)
    btncreate_bill.configure(bg=ntactbg, fg=ntactfg)
    add_patient.configure(bg=actbg, fg=actfg)
    add_medicine.configure(bg=ntactbg, fg=ntactfg)

    add_patient_container = Frame(rightcontainer,
                                  width=1145, height=587,
                                  highlightbackground="#bdbdbd",
                                  highlightthickness=1,
                                  bg="#d0edf2")
    add_patient_container.grid(row=0, column=0, padx=5, pady=5)
    add_patient_container.grid_propagate(False)
    sampletext = Label(add_patient_container, text="Add Patient Page")
    sampletext.grid(row=0, column=0, padx=5)
    sampletext.config(font=("Times new roman", 20))

    bed_no_lbl = Label(add_patient_container, text="Bed NO: ", width=20, font=("Arial", 12))
    bed_no_lbl.grid(row=1, column=0, pady=5, padx=5, sticky="W")

    bed_no = Entry(add_patient_container, font=("Arial", 12))
    bed_no.grid(row=1, column=1, pady=5, padx=5)

    registration_no_lbl = Label(add_patient_container, text="Registration NO: ", width=20, font=("Arial", 12))
    registration_no_lbl.grid(row=1, column=0, pady=5, padx=5, sticky="W")
    global registration_no
    registration_no = Entry(add_patient_container, font=("Arial", 12))
    registration_no.grid(row=1, column=1, pady=5, padx=5)

    global cabin_no
    cabin_no_lbl = Label(add_patient_container, text="Cabin No: ", width=20, font=("Arial", 12))
    cabin_no_lbl.grid(row=1, column=2, pady=5, padx=5, sticky="")

    cabin_no = Entry(add_patient_container, font=("Arial", 12))
    cabin_no.grid(row=1, column=3, pady=5, padx=5)

    patient_name_lbl = Label(add_patient_container, text="Patient Name: ", width=20, font=("Arial", 12))
    patient_name_lbl.grid(row=2, column=0, pady=5, padx=5, sticky="W")
    global patient_name
    patient_name = Entry(add_patient_container, font=("Arial", 12))
    patient_name.grid(row=2, column=1, pady=5, padx=5)

    father_name_lbl = Label(add_patient_container, text="Father's Name: ", width=20, font=("Arial", 12))
    father_name_lbl.grid(row=2, column=2, pady=5, padx=5, sticky="W")
    global father_name
    father_name = Entry(add_patient_container, font=("Arial", 12))
    father_name.grid(row=2, column=3, pady=5, padx=5)

    age_lbl = Label(add_patient_container, text="Contact No: ", width=20, font=("Arial", 12))
    age_lbl.grid(row=3, column=0, pady=5, padx=5, sticky="W")
    global age
    age = Entry(add_patient_container, font=("Arial", 12))
    age.grid(row=3, column=1, pady=5, padx=5)

    gender_lbl = Label(add_patient_container, text="Gender: ", width=20, font=("Arial", 12))
    gender_lbl.grid(row=3, column=2, pady=5, padx=5, sticky="W")
    global gender
    gender = Entry(add_patient_container, font=("Arial", 12))
    gender.grid(row=3, column=3, pady=5, padx=5)

    religion_lbl = Label(add_patient_container, text="Religion: ", width=20, font=("Arial", 12))
    religion_lbl.grid(row=4, column=0, pady=5, padx=5, sticky="W")
    global religion
    religion = Entry(add_patient_container, font=("Arial", 12))
    religion.grid(row=4, column=1, pady=5, padx=5)

    present_address_lbl = Label(add_patient_container, text="Present Address: ", width=20, font=("BebasNeue-Regular", 12))
    present_address_lbl.grid(row=4, column=2, pady=5, padx=5, sticky="W")
    global present_address
    present_address = Entry(add_patient_container, font=("Arial", 12))
    present_address.grid(row=4, column=3, pady=5, padx=5)

    permanent_address_lbl = Label(add_patient_container, text="Permanent Address: ", width=20, font=("Arial", 12))
    permanent_address_lbl.grid(row=5, column=0, pady=5, padx=5, sticky="W")
    global permanent_address
    permanent_address = Entry(add_patient_container, font=("Arial", 12))
    permanent_address.grid(row=5, column=1, pady=5, padx=5)

    emergency_contact_lbl = Label(add_patient_container, text="Emergency Contact: ", width=20, font=("Arial", 12))
    emergency_contact_lbl.grid(row=5, column=2, pady=5, padx=5, sticky="W")
    global emergency_contact
    emergency_contact = Entry(add_patient_container, font=("Arial", 12))
    emergency_contact.grid(row=5, column=3, pady=5, padx=5)

    admission_date_time_lbl = Label(add_patient_container, text="Admission Date with time: ", width=20,
                                    font=("Arial", 12))
    admission_date_time_lbl.grid(row=6, column=0, pady=5, padx=5, sticky="W")
    global admission_date_time
    admission_date_time = Entry(add_patient_container, font=("Arial", 12))
    admission_date_time.grid(row=6, column=1, pady=5, padx=5)

    discharge_date_time_lbl = Label(add_patient_container, text="Discharge Date with Time: ", width=20,
                                    font=("Arial", 12))
    discharge_date_time_lbl.grid(row=6, column=2, pady=5, padx=5, sticky="W")
    global discharge_date_time
    discharge_date_time = Entry(add_patient_container, font=("Arial", 12))
    discharge_date_time.grid(row=6, column=3, pady=5, padx=5)

    death_date_time_lbl = Label(add_patient_container, text="Date and time of death: ", width=20, font=("Arial", 12))
    death_date_time_lbl.grid(row=7, column=0, pady=5, padx=5, sticky="W")
    global death_date_time
    death_date_time = Entry(add_patient_container, font=("Arial", 12))
    death_date_time.grid(row=7, column=1, pady=5, padx=5)

    name_consultant_lbl = Label(add_patient_container, text="Name of consultant: ", width=20, font=("Arial", 12))
    name_consultant_lbl.grid(row=7, column=2, pady=5, padx=5, sticky="W")
    global name_consultant_time
    name_consultant_time = Entry(add_patient_container, font=("Arial", 12))
    name_consultant_time.grid(row=7, column=3, pady=5, padx=5)

    diagnosis_lbl = Label(add_patient_container, text="Diagnosis: ", width=20, font=("Arial", 12))
    diagnosis_lbl.grid(row=8, column=0, pady=5, padx=5, sticky="W")
    global diagnosis
    diagnosis = Entry(add_patient_container, font=("Arial", 12))
    diagnosis.grid(row=8, column=1, pady=5, padx=5)

    treatment_given_lbl = Label(add_patient_container, text="treatment Given: ", width=20, font=("Arial", 12))
    treatment_given_lbl.grid(row=8, column=2, pady=5, padx=5, sticky="W")
    global treatment_given
    treatment_given = Entry(add_patient_container, font=("Arial", 12))
    treatment_given.grid(row=8, column=3, pady=5, padx=5)

    operation_performed_lbl = Label(add_patient_container, text="Operation Performed: ", width=20, font=("Arial", 12))
    operation_performed_lbl.grid(row=9, column=0, pady=5, padx=5, sticky="W")
    global operation_performed
    operation_performed = Entry(add_patient_container, font=("Arial", 12))
    operation_performed.grid(row=9, column=1, pady=5, padx=5)

    discharge_note_lbl = Label(add_patient_container, text="Discharge Note: ", width=20, font=("Arial", 12))
    discharge_note_lbl.grid(row=9, column=2, pady=5, padx=5, sticky="W")
    global discharge_note
    discharge_note = Entry(add_patient_container, font=("Arial", 12))
    discharge_note.grid(row=9, column=3, pady=5, padx=5)
    save_patient = Button(
        add_patient_container,
        text="Save",
        height=2,
        width=25,
        command=lambda: save_ptn_to_db(registration_no.get(),
                                       cabin_no.get(),
                                       patient_name.get(),
                                       father_name.get(),
                                       age.get(),
                                       gender.get(),
                                       religion.get(),
                                       present_address.get(),
                                       permanent_address.get(),
                                       emergency_contact.get(),
                                       admission_date_time.get(),
                                       discharge_date_time.get(),
                                       death_date_time.get(),
                                       name_consultant_time.get(),
                                       diagnosis.get(),
                                       treatment_given.get(),
                                       operation_performed.get(),
                                       discharge_note.get()

                                       )
    )

    save_patient.grid(row=10, column=2)

    reset_patient = Button(
        add_patient_container,
        text="Reset",
        height=2,
        width=25,
        command=clearptnentry
    )

    reset_patient.grid(row=10, column=3)


def clearptnentry():
    registration_no.delete(0, END),
    cabin_no.delete(0, END),
    patient_name.delete(0, END),
    father_name.delete(0, END),
    age.delete(0, END),
    gender.delete(0, END),
    religion.delete(0, END),
    present_address.delete(0, END),
    permanent_address.delete(0, END),
    emergency_contact.delete(0, END),
    admission_date_time.delete(0, END),
    discharge_date_time.delete(0, END),
    death_date_time.delete(0, END),
    name_consultant_time.delete(0, END),
    diagnosis.delete(0, END),
    treatment_given.delete(0, END),
    operation_performed.delete(0, END),
    discharge_note.delete(0, END)


def save_ptn_to_db(var1, var2, var3, var4, var5, var6, var7, var8, var9, var10, var11, var12, var13, var14, var15,
                   var16, var17, var18):
    # print(var1)
    if len(var1) != 0:
        if len(var2) != 0:
            if len(var3) != 0:
                ptn_details = [var1, var2, var3, var4, var5, var7, var8, var9, var11, var10, var12, var13, var14, var15,
                               var16, var17, var18]
                conn = mysql.connector.connect(
                    host=host_name,
                    user=user_name,
                    password=pass_word,
                    database="ncpharmacy"
                )
                c = conn.cursor()
                c.execute(
                    "INSERT INTO patient (regno,cabinno,patientname,fathersname,contact,religion,presentaddress,parmanentaddress,admissiondate,emergencycontact,dischargedate,dateofdeath,nameofconsultant,diagnosis,treatment,operation,dischargenote) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (ptn_details))
                conn.commit()
                # print ("Sucessfully submitted data")
                conn.close()
                clearptnentry()

            else:
                messagebox.showinfo("Error", "Patient Name Can't be Blank")
        else:
            messagebox.showinfo("Error", "Cabin No Can't be Blank")
    else:
        messagebox.showinfo("Error", "Registration Number Can't be Blank")


def btnstatechk():
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )

    c = conn.cursor()
    data = c.execute("SELECT * FROM tempbill")
    rows = c.fetchone()
    if rows != None:
        save_bill_btn['state'] = "normal"
        mod_bill_btn['state'] = "normal"
    # print("Data Found")
    else:
        # print("no data")
        save_bill_btn['state'] = "disabled"
        mod_bill_btn['state'] = "disabled"
    conn.close()


def dumptempbill():
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    data = c.execute("DELETE FROM `tempbill`")

    conn.commit()
    conn.close()
def dumpinvbill():
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    data = c.execute("DELETE FROM `purchaseinvoice`")

    conn.commit()
    conn.close()


def totalbillpreview():
    totalbillpreview_lbl = Label(billing_btn_container, text="Total Bill: ", width=20)
    totalbillpreview_lbl.grid(row=0, column=0, sticky="nsew")
    totalbillpreview_lbl.config(font=("Times new roman", 10))

    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )

    c = conn.cursor()
    data = c.execute("SELECT SUM(total) AS totalbill FROM tempbill;")
    getdata = c.fetchone()[0]
    # print(getdata)
    totalbillpreview_lbl = Label(billing_btn_container, text="Total Bill: ",
                                 width=15,
                                 bg="#6760a6",
                                 fg="white")
    totalbillpreview_lbl.grid(row=0, column=0, sticky="nsew")
    totalbillpreview_lbl.config(font=("Times new roman", 12))

    global totalbillpreview_amnt
    totalbillpreview_amnt = Label(billing_btn_container, text=str(getdata), width=20,
                                  bg="#4d4c4c",
                                  fg="yellow")
    totalbillpreview_amnt.grid(row=0, column=2, sticky="nsew")
    totalbillpreview_amnt.config(font=("Times new roman", 12))


def billing_info():
    global regno
    regno = select_patient_for_billing.get()
    print(regno)
    # select_patient_for_billing.delete(0,END)
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    data = c.execute("SELECT * FROM patient WHERE regno=%s", (regno,))
    rows = c.fetchone()
    if rows != None:
        print(rows[0])
        selected_patient_reg_no_from_db_lbl.config(text=rows[1])
        selected_patient_name_from_db_lbl.config(text=rows[4])
        selected_patient_cabin_from_db_lbl.config(text=rows[2])
        selected_patient_contact_from_db_lbl.config(text=rows[3])
        billing_items()
    else:
        selected_patient_reg_no_from_db_lbl.config(text="-----")
        selected_patient_name_from_db_lbl.config(text="-----")
        selected_patient_cabin_from_db_lbl.config(text="-----")
        selected_patient_contact_from_db_lbl.config(text="-----")


def billing_items():
    print(slno)
    time.sleep(0)
    serial_no_lbl = Label(add_medicine_to_bill, text="SL No: ", width=5, font=("Arial", 10),border=1,relief="solid")
    serial_no_lbl.grid(row=0, column=0, pady=5, padx=5, sticky="W")
    billnogenerator()
    global serial_no
    serial_no = Label(add_medicine_to_bill, text=slno, width=12, font=("Arial", 10),border=1,relief="solid")
    serial_no.grid(row=0, column=1, pady=5, padx=5, sticky="W")

    billing_med_lbl = Label(add_medicine_to_bill, text="Medicine Name: ", width=12, font=("Arial", 10),border=1,relief="solid")
    billing_med_lbl.grid(row=0, column=2, pady=5, padx=5, sticky="W")
    global billing_med
    billing_med = AutocompleteEntry(add_medicine_to_bill, font=("Arial", 11), width=30,border=1,relief="solid")
    billing_med.set_completion_list(test_list)
    billing_med.grid(row=0, column=3, pady=5, padx=5)
    billing_med.focus_set()
    global billing_quantity
    quantity_lbl = Label(add_medicine_to_bill, text="Quantiy: ", width=10, font=("Arial", 10),border=1,relief="solid")
    quantity_lbl.grid(row=0, column=4, pady=5, padx=5, sticky="W")
    billing_quantity = Entry(add_medicine_to_bill, font=("Arial", 12), width=4,border=1,relief="solid")
    billing_quantity.grid(row=0, column=5, pady=5, padx=5)

    add_items_for_billing = Button(
        add_medicine_to_bill,
        text="Add items",
        height=1,
        width=20,
        command=lambda: savetotempbill(billing_med.get(), billing_quantity.get())
        , border=1, relief="solid"
    )
    add_items_for_billing.grid(row=0, column=6, padx=5, pady=5)
    add_items_for_billing.configure(bg="green",fg="yellow")


# =====================items to temporary bill============================
def updatetempbill():
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    records = c.execute("SELECT * FROM tempbill")
    tempbilldata = c.fetchall()

    # print(tempbilldata)
    fatcheddata = tree.get_children()
    for elements in fatcheddata:
        tree.delete(elements)
    # print (fatcheddata)
    for row in tempbilldata:
        tree.insert("", tkinter.END, values=(row[3], row[4], row[5], row[6], row[7]))
    conn.commit()
    conn.close()


def updatetempbill2():
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    records = c.execute("SELECT * FROM tempbill")
    tempbilldata = c.fetchall()

    # print(tempbilldata)
    fatcheddata = tree.get_children()
    for elements in fatcheddata:
        tree.delete(elements)
    # print (fatcheddata)
    for row in tempbilldata:
        tree.insert("", tkinter.END, values=(row[3], row[4], row[5], row[6], row[7]))
        tree.bind("Double-1", onDoubleClick)
    conn.commit()
    conn.close()


# print(rows)
def chk_med(c1):
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()

    med_name_chk = c.execute("SELECT * FROM tempbill WHERE medname=%s", (c1,))
    temp_med = c.fetchone()
    if temp_med != None:
        print("Med found")
        return 1
    else:
        print("No med found")
        return 0


def savetotempbill(val1, val2):
    ff = chk_med(val1)
    fff = int(ff)
    if fff == 1:
        messagebox.showinfo("Error", "Sorry Medicine is Already in the Bill")

    else:
        conn = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=pass_word,
            database="ncpharmacy"
        )
        c = conn.cursor()

        stk_check = c.execute("SELECT * FROM med WHERE medname=%s", (val1,))
        in_stock = int(c.fetchone()[5])

        print(in_stock)
        if in_stock >= int(val2):
            billing_med.delete(0, END)
            billing_quantity.delete(0, END)
            # print("Stock available")
            data = c.execute("SELECT * FROM med WHERE medname=%s", (val1,))
            rows = c.fetchone()
            if rows != None:
                medicineid = rows[0]
                medicinename = rows[1]
                unit_price = rows[3]
                instock = rows[5]
                unit_total_price = (int(unit_price) * int(val2))
                # print(unit_total_price)
                bill_data = [slno, regno, medicineid, medicinename, val2, unit_price, unit_total_price]
                c.execute(
                    "INSERT INTO tempbill (billno,regid, medid, medname, quantity, rate, total) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                    (bill_data))
                conn.commit()
                # print(slno)
                # print("submited")
                updatetempbill()
            else:
                return
        else:
            # print("Not available")
            messagebox.showinfo("Error", str(val1) + "__Available__ " + str(in_stock) + "Pcs")

    updatetempbill()
    btnstatechk()
    totalbillpreview()


def screate_bill():
    check_bill.configure(bg=ntactbg, fg=ntactfg)
    edit_medicine.configure(bg=ntactbg, fg=ntactfg)
    edit_patient.configure(bg=ntactbg, fg=ntactfg)
    print_bill.configure(bg=ntactbg, fg=ntactfg)
    btncreate_bill.configure(bg=actbg, fg=actfg)
    add_patient.configure(bg=ntactbg, fg=ntactfg)
    add_medicine.configure(bg=ntactbg, fg=ntactfg)

    dumptempbill()
    # print("working")
    add_patient_container = Frame(rightcontainer,
                                  width=1145, height=587,
                                  highlightbackground="#bdbdbd",
                                  highlightthickness=1)
    add_patient_container.grid(row=0, column=0, padx=5, pady=5)
    add_patient_container.grid_propagate(False)
    # sampletext=Label(add_patient_container, text="Create Bill")
    # sampletext.grid(row=0,column=0, padx=5)
    # sampletext.config(font=("Times new roman", 20))

    patient_selection = LabelFrame(add_patient_container,
                                   text="Select Patient",
                                   width=1130, height=60,
                                   highlightbackground="#bdbdbd",
                                   highlightthickness=0
                                   )
    patient_selection.grid(row=1, column=0, pady=5, padx=5)
    patient_selection.grid_propagate(False)
    patient_info = LabelFrame(add_patient_container,
                              text="Patient Information",
                              width=1130, height=80,
                              highlightbackground="#bdbdbd",
                              highlightthickness=0
                              )
    patient_info.grid(row=2, column=0, pady=5, padx=5)
    patient_info.grid_propagate(False)

    global product_info
    product_info = LabelFrame(add_patient_container,
                              text="Billing Items",
                              width=1130, height=420,
                              highlightbackground="#bdbdbd",
                              highlightthickness=0,
                              bg="#9ecbff"
                              )
    product_info.grid(row=3, column=0, pady=5, padx=5)
    product_info.grid_propagate(False)
    global add_medicine_to_bill
    add_medicine_to_bill = Frame(product_info,
                                 width=1115, height=40,
                                 highlightbackground="#bdbdbd",
                                 highlightthickness=1)
    add_medicine_to_bill.grid(row=0, column=0, padx=5, pady=5)
    add_medicine_to_bill.grid_propagate(False)
    global added_medicine_to_bill
    added_medicine_to_bill = Frame(product_info,
                                   width=1115, height=300,
                                   highlightbackground="gray",
                                   highlightthickness=1)
    added_medicine_to_bill.grid(row=2, column=0, padx=(0, 5), pady=5)
    added_medicine_to_bill.grid_propagate(False)
    global billing_btn_container
    billing_btn_container = Frame(product_info,
                                  width=1115, height=30,
                                  highlightbackground="#bdbdbd",
                                  highlightthickness=1,
                                  bg="yellow")
    billing_btn_container.grid(row=3, column=0, padx=1, pady=5)
    billing_btn_container.grid_propagate(False)

    global save_bill_btn
    save_bill_btn = Button(
        billing_btn_container,
        text="Generate Bill",
        height=1,
        width=15,
        command=stocksub,
        highlightcolor="black",
        highlightthickness=1
    )
    save_bill_btn.grid(row=0, column=3, padx=1, pady=1)
    save_bill_btn.configure(bg="#0051b5",fg="#b4f224")
    global mod_bill_btn
    mod_bill_btn = Button(
        billing_btn_container,
        text="Modify Item",
        height=1,
        width=15,
        command=edit_item,
        highlightcolor="black",
        highlightthickness=1
    )
    mod_bill_btn.grid(row=0, column=4, padx=1, pady=1)
    mod_bill_btn.configure(bg="blue", fg="yellow")
    global tree
    tree = ttk.Treeview(added_medicine_to_bill, show="headings", height=20,
                        columns=("medid", "medname", "quantity", "rate", "total"))
    treecolumnwid = 150
    tree.heading('medid', text="ID", anchor=W)
    tree.column("medid", minwidth=0, width=50, stretch=NO)
    tree.heading('medname', text="Medicine Name", anchor=CENTER)
    tree.column("medname", minwidth=0, width=400, stretch=NO)
    tree.heading('quantity', text="Quantiy", anchor=CENTER)
    tree.column("quantity", minwidth=0, width=200, stretch=NO)
    tree.heading('rate', text="Unit Price", anchor=CENTER)
    tree.column("rate", minwidth=0, width=200, stretch=NO)
    tree.heading('total', text="Total", anchor=CENTER)
    tree.column("total", minwidth=0, width=200, stretch=NO)
    tree.grid(row=2, column=0)

    global select_patient_for_billing
    select_patient_for_billing_lbl = Label(patient_selection, text="Registration Number: ", bg="white", width=20,
                                           font=("Arial", 12))
    select_patient_for_billing_lbl.grid(row=1, column=0, padx=5, pady=10)
    select_patient_for_billing = Entry(patient_selection, font=("Arial", 10),border=1,relief="solid")
    select_patient_for_billing.grid(row=1, column=1)
    selected_patient = Button(
        patient_selection,
        text="Select",
        height=1,
        width=25,
        command=billing_info,
        highlightcolor="black",
        highlightthickness=1,
        border=1,relief="solid"
    )
    selected_patient.grid(row=1, column=2, padx=5, pady=5)
    selected_patient.configure(bg="green",fg="yellow")

    selected_patient_reg_no_lbl = Label(patient_info, text="REG NO: ", width=15, font=("Times", 12))
    selected_patient_reg_no_lbl.grid(row=2, column=0, pady=1, padx=1, sticky="W")

    global selected_patient_reg_no_from_db_lbl
    selected_patient_reg_no_from_db_lbl = Label(patient_info, text="n/a", bg="white", width=20, font=("Times", 12),
                                                highlightcolor="black", highlightthickness=1)
    selected_patient_reg_no_from_db_lbl.grid(row=2, column=1, pady=1, padx=1, sticky="W")

    selected_patient_name_lbl = Label(patient_info, text="Patient Name: ", width=15, font=("Times", 12))
    selected_patient_name_lbl.grid(row=2, column=2, pady=1, padx=1, sticky="W")

    global selected_patient_name_from_db_lbl
    selected_patient_name_from_db_lbl = Label(patient_info, text="n/a", bg="white", width=40, font=("Times", 12))
    selected_patient_name_from_db_lbl.grid(row=2, column=3, pady=1, padx=1, sticky="W")

    global selected_patient_cabin_from_db_lbl
    selected_patient_cabin_lbl = Label(patient_info, text="Cabin: ", width=15, font=("Times", 12))
    selected_patient_cabin_lbl.grid(row=3, column=0, pady=1, padx=1, sticky="W")
    selected_patient_cabin_from_db_lbl = Label(patient_info, text="n/a ", bg="white", width=20, font=("Times", 12))
    selected_patient_cabin_from_db_lbl.grid(row=3, column=1, pady=1, padx=1, sticky="N")

    selected_patient_contact_lbl = Label(patient_info, text="Contact No: ", width=15, font=("Times", 12))
    selected_patient_contact_lbl.grid(row=3, column=2, pady=1, padx=1, sticky="W")

    global selected_patient_contact_from_db_lbl
    selected_patient_contact_from_db_lbl = Label(patient_info, text="n/a", bg="white", width=40, font=("Times", 12))
    selected_patient_contact_from_db_lbl.grid(row=3, column=3, pady=1, padx=1, sticky="W")

    updatetempbill()
    btnstatechk()


def print_bills():
    check_bill.configure(bg=ntactbg, fg=ntactfg)
    edit_medicine.configure(bg=ntactbg, fg=ntactfg)
    edit_patient.configure(bg=ntactbg, fg=ntactfg)
    print_bill.configure(bg=actbg, fg=actfg)
    btncreate_bill.configure(bg=ntactbg, fg=ntactfg)
    add_patient.configure(bg=ntactbg, fg=ntactfg)
    add_medicine.configure(bg=ntactbg, fg=ntactfg)

    add_patient_container = Frame(rightcontainer,
                                  width=1145, height=587,
                                  highlightbackground="#bdbdbd",
                                  highlightthickness=1)
    add_patient_container.grid(row=0, column=0, padx=5, pady=5)
    add_patient_container.grid_propagate(False)
    global print_bill_container
    print_bill_container = Frame(add_patient_container,
                                 width=1130, height=580,
                                 highlightbackground="#bdbdbd",
                                 highlightthickness=0)
    print_bill_container.grid(row=0, column=0, padx=5, pady=5)
    print_bill_container.grid_propagate(False)

    billll = LabelFrame(print_bill_container,
                        text="Search Bills",
                        width=1120, height=80,
                        highlightbackground="#bdbdbd",
                        highlightthickness=0,
                        bg="#497fd6"
                        )
    billll.grid(row=0, column=0, pady=5, padx=5)
    billll.grid_propagate(False)

    global printablebills

    enter_rid_lbl = Label(billll, text="Enter Reg No: ", width=20, font=("Arial", 12))
    enter_rid_lbl.grid(row=0, column=0, pady=5, padx=5, sticky="W")
    global enter_rid
    enter_rid = Entry(billll, font=("Arial", 12))
    enter_rid.grid(row=0, column=1, pady=15, padx=5)
    bills = Button(
        billll,
        text="Get Bill",
        height=1,
        width=25,
        border=1,
        relief="solid",
        bg="#78bbf5",
        fg="yellow",
        command=lambda: get_print_bill(enter_rid.get())
    )

    bills.grid(row=0, column=2, padx=10)
    sumbills = Button(
        billll,
        text="Print Bill Summary",
        height=1,
        border=1,
        relief="solid",
        bg="#d5f578",
        width=25,
        fg="red",
        command=lambda: multipagebill(enter_rid.get())
    )

    sumbills.grid(row=0, column=3, padx=10)
#Summary bill generator
def multipagebill(mmc):
    print(mmc)
    regnumber = mmc
    global p
    getnamess(mmc)
    print_sum_bill_2(regnumber)
    # Saving the PDF
    global slno
    slno = "SUM-"+ mmc
    # p = canvas.Canvas("Summary Bill For "+ str(nn1) +".pdf", pagesize=(595, 842), bottomup=0)
    p = canvas.Canvas("Summary Bill.pdf", pagesize=(595, 842), bottomup=0)
    getsumbilldata2(regnumber)
    p.showPage()
    p.save()
    opensummaryfile()
def getsumbilldata2(mm1):
    global idd
    idd=mm1
    stts=0
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    data = c.execute("SELECT * FROM finalbill WHERE regid=%s AND  status = %s;",(idd,stts,))
    rows = c.fetchall()
    # print(rows[1][3])
    # global slno
    # slno = rows[0][1]
    linesp = 245
    serialno = 1
    global date
    date = rows[0][8]
    # print(date)
    p.setFont("Helvetica", 10.5)
    total_payable=0
    pagignator=0
    billtempalate()
    for row in range(len(medidls)):
        #print(row[4])
        #print(row[5])
        #print(row[6])

        if pagignator < 41:

            total_payable=total_payable+int(totalprice[row])
            p.drawRightString(65, linesp, str(serialno))
            p.drawString(110, linesp, mednamels[row])
            p.drawCentredString(430, linesp, meddata[row])
            p.drawCentredString(500, int(linesp), totalprice[row])
            linesp = linesp + 12
            serialno = serialno + 1
            print(total_payable)
            pagignator=pagignator+1
        else:
            linesp = 245
            pagignator = 0
            p.showPage()
            billtempalate()
    p.roundRect(400, 762, 150, 20, 5, stroke=1, fill=0)
    p.drawCentredString(500, 775, str(total_payable))
    p.drawRightString(460, 775, "Total Bill : ")
def billtempalate():
    p.translate(10, 40)
    p.scale(1, -1)
    p.scale(1, -1)
    p.translate(-10, -40)
    p.setFont("Helvetica-Bold", 30)
    p.drawCentredString(300, 60, "Pharmacy Management Sytem")
    p.roundRect(30, 20, 530, 800, 2, stroke=1, fill=0)
    p.setFont("Helvetica-Bold", 12)
    p.drawCentredString(300, 80, "75, Anannya Residential Area, CHITTAGONG")
    p.drawCentredString(300, 95, "PHONE: 01748807540, 9384777477")
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
    p.drawString(310, 170, str(idd))
    p.drawRightString(450, 170, "Cabin No :")
    p.drawString(460, 170, str(cbn_no))
    p.drawRightString(450, 194, "Date :")
    p.drawString(460, 194, str(today))
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

def print_sum_bill_2(p1):
    status = 0
    global medidls
    global mednamels
    global meddata
    global totalprice
    medidls = []
    mednamels = []
    meddata = []
    totalprice = []
    billnols = []
    medidls.clear()
    mednamels.clear()
    meddata.clear()
    totalprice.clear()
    billnols.clear()
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    data = c.execute("SELECT * FROM finalbill WHERE regid=%s AND status =%s", (p1, status,))
    rows = c.fetchall()

    for row in rows:
        print(row)
        medname = row[4]
        medid = row[3]
        billid = row[1]
        #print(billid)
        if medid not in medidls:
            medidls.append(medid)
            mednamels.append(medname)
        if billid not in billnols:
            billnols.append(billid)
            #print(billnols)

    # print(len(medidls))
    for meds in medidls:
        c = conn.cursor()
        data = c.execute("SELECT SUM(quantity) AS totalbill FROM finalbill WHERE medid=%s AND regid=%s AND status =%s;", (meds, p1, status,))
        global getdata
        getdata = c.fetchone()[0]
        getdata = str(getdata)
        meddata.append(getdata)
        # print(meddata)
    for meds in medidls:
        c = conn.cursor()
        data = c.execute("SELECT SUM(total) AS totalbill FROM finalbill WHERE medid=%s AND regid=%s AND status =%s;", (meds, p1, status,))
        getdata = c.fetchone()[0]
        getdata = str(getdata)
        totalprice.append(getdata)
    print(mednamels)
    print(medidls)
    print(meddata)
    print(totalprice)
def getnamess(regno):
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    data = c.execute("SELECT * FROM patient WHERE regno=%s", (regno,))
    rows = c.fetchall()

    global ptn_name
    global cbn_no
    global phn_no
    global regi_no
    ptn_name = rows[0][4]
    cbn_no = rows[0][2]
    phn_no = rows[0][3]
    regi_no = rows[0][1]
def get_ptn_info_sumbill(nn1):
    c = conn.cursor()
    ptn = c.execute("SELECT cabinno,patientname FROM patient WHERE regno=%s;",(nn1,))
    ptn_info=c.fetchone()
    print(ptn_info)
    global ptn_name
    ptn_name = ptn_info[1]
    global cbn_no
    cbn_no = ptn_info[0]
def getsumbilldata(mm1):
    idd=mm1
    stts=0
    c = conn.cursor()
    data = c.execute("SELECT * FROM finalbill WHERE regid=%s AND  status = %s;",(idd,stts,))
    rows = c.fetchall()
    # print(rows[1][3])
    # global slno
    # slno = rows[0][1]
    linesp = 245
    serialno = 1
    global date
    date = rows[0][8]
    # print(date)
    p.setFont("Helvetica", 10.5)
    total_payable=0
    for row in range(len(medidls)):
        #print(row[4])
        #print(row[5])
        #print(row[6])
        total_payable=total_payable+int(totalprice[row])
        p.drawRightString(65, linesp, str(serialno))
        p.drawString(110, linesp, mednamels[row])
        p.drawCentredString(430, linesp, meddata[row])
        p.drawCentredString(500, int(linesp), totalprice[row])
        linesp = linesp + 12
        serialno = serialno + 1
        print(total_payable)
    p.drawCentredString(500, 775, str(total_payable))
    p.drawRightString(460, 775, "Total Bill : ")
def gen_sum_bill(nn1):
    global p
    slno = "SUM-"+str(nn1)
    #p = canvas.Canvas("Summary Bill For "+ str(nn1) +".pdf", pagesize=(595, 842), bottomup=0)
    p = canvas.Canvas("Summary Bill.pdf", pagesize=(595, 842), bottomup=0)

    p.translate(10, 40)
    p.scale(1, -1)
    p.scale(1, -1)
    p.translate(-10, -40)
    p.setFont("Helvetica-Bold", 30)
    p.drawCentredString(300, 60, "Pharmacy Management System")
    p.roundRect(30, 20, 530, 800, 2, stroke=1, fill=0)
    p.setFont("Helvetica-Bold", 12)
    p.drawCentredString(300, 80, "75, Anannya Residential Area, CHITTAGONG")
    p.drawCentredString(300, 95, "PHONE: 01748807540, 873477374")
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
    p.drawString(310, 170, str(nn1))
    p.drawRightString(450, 170, "Cabin No :")
    p.drawString(460, 170, str(cbn_no))
    p.drawRightString(450, 194, "Date :")
    p.drawString(460, 194, str(today))
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
    getsumbilldata(nn1)
    p.showPage()
    # Saving the PDF
    p.save()
def print_sum_bill(p1):
    get_ptn_info_sumbill(p1)
    status = 0
    global medidls
    global mednamels
    global meddata
    global totalprice
    medidls = []
    mednamels = []
    meddata = []
    totalprice = []
    billnols = []
    medidls.clear()
    mednamels.clear()
    meddata.clear()
    totalprice.clear()
    billnols.clear()
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    data = c.execute("SELECT * FROM finalbill WHERE regid=%s AND status =%s", (p1, status,))
    rows = c.fetchall()

    for row in rows:
        print(row)
        medname = row[4]
        medid = row[3]
        billid = row[1]
        #print(billid)
        if medid not in medidls:
            medidls.append(medid)
            mednamels.append(medname)
        if billid not in billnols:
            billnols.append(billid)
            #print(billnols)

    # print(len(medidls))
    for meds in medidls:
        c = conn.cursor()
        data = c.execute("SELECT SUM(quantity) AS totalbill FROM finalbill WHERE medid=%s AND regid=%s AND status =%s;", (meds, p1, status,))
        global getdata
        getdata = c.fetchone()[0]
        getdata = str(getdata)
        meddata.append(getdata)
        # print(meddata)
    for meds in medidls:
        c = conn.cursor()
        data = c.execute("SELECT SUM(total) AS totalbill FROM finalbill WHERE medid=%s AND regid=%s AND status =%s;", (meds, p1, status,))
        getdata = c.fetchone()[0]
        getdata = str(getdata)
        totalprice.append(getdata)
    print(mednamels)
    print(medidls)
    print(meddata)
    print(totalprice)
    gen_sum_bill(p1)
    opensummaryfile()
# End of print sum bills
def get_print_bill(n1):
    printablebills = LabelFrame(print_bill_container,
                                text="Printable Bills",
                                width=1120, height=450,
                                highlightbackground="#bdbdbd",
                                highlightthickness=0,
                                bg="white"
                                )
    printablebills.grid(row=1, column=0, pady=5, padx=5)
    printablebills.grid_propagate(False)
    print(n1)
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    status = 0
    billdata = []
    c = conn.cursor()
    data = c.execute("SELECT billno FROM finalbill WHERE regid=%s AND status =%s ORDER BY billno DESC", (n1, status,))
    rows = c.fetchall()
    for row in rows:
        billno = row[0]
        # print(billno)
        if billno not in billdata:
            billdata.append(billno)
    datano = 0
    for bills in billdata:
        for i in range(0, 10):
            for j in range(0, 7):
                print(j)
                prev_bill_btn = Button(
                    printablebills,
                    text="Bill No: " + str(billdata[datano]),
                    height=1,
                    width=20,
                    border=1,
                    relief="solid",
                    bg="#d5f578",
                    fg="red",
                    command=lambda i=datano: openpdffile(billdata[i])
                )

                prev_bill_btn.grid(row=i, column=j, padx=2, pady=2)
                datano = datano + 1


def edit_patient():
    add_patient_container = Frame(rightcontainer,
                                  width=1145, height=587,
                                  highlightbackground="#bdbdbd",
                                  highlightthickness=1)
    add_patient_container.grid(row=0, column=0, padx=5, pady=5)
    add_patient_container.grid_propagate(False)
    patient_selection = LabelFrame(add_patient_container,
                                   text="Select Patient",
                                   width=1130, height=60,
                                   highlightbackground="#bdbdbd",
                                   highlightthickness=0,
                                   bg="#d0edf2"
                                   )
    patient_selection.grid(row=1, column=0, pady=5, padx=5)
    patient_selection.grid_propagate(False)

    select_patient_for_billing_lbl = Label(patient_selection, text="Registration Number: ", bg="white", width=20,
                                           font=("Arial", 12))
    select_patient_for_billing_lbl.grid(row=1, column=0, padx=5, pady=10)
    select_patient_for_billing = Entry(patient_selection, font=("Arial", 10), border=1, relief="solid")
    select_patient_for_billing.grid(row=1, column=1)
    selected_patient = Button(
        patient_selection,
        text="View",
        height=1,
        width=25,
        command=lambda: getptninfo(select_patient_for_billing.get()),
        highlightcolor="black",
        highlightthickness=1,
        border=1, relief="solid"
    )
    selected_patient.grid(row=1, column=2, padx=5, pady=5)
    selected_patient.configure(bg="green", fg="yellow")


    patient_info = LabelFrame(add_patient_container,
                              text="Patient Information",
                              width=1130, height=200,
                              highlightbackground="#bdbdbd",
                              highlightthickness=0,
                              bg="white"
                              )
    patient_info.grid(row=2, column=0, pady=5, padx=5)
    patient_info.grid_propagate(False)
    global patient_id
    global patient_doa
    global patient_cabin
    global patient_regno
    global patient_contact
    patient_id_lbl = Label(patient_info, text="Patient ID: ", width=12, font=("Arial", 10), border=1, relief="solid")
    patient_id_lbl.grid(row=0, column=0, pady=5, padx=5, sticky="W")
    patient_id = Label(patient_info, text="----- ", width=12, font=("Arial", 10), border=1, relief="solid", bg="white")
    patient_id.grid(row=0, column=1, pady=5, padx=5, sticky="W")

    patient_regno_lbl = Label(patient_info, text="Registration No:  ", width=18, font=("Arial", 10), border=1,
                              relief="solid")
    patient_regno_lbl.grid(row=1, column=0, pady=5, padx=5, sticky="W")
    patient_regno = Label(patient_info, text="----- ", width=18, font=("Arial", 10), border=1, relief="solid",
                          bg="white")
    patient_regno.grid(row=1, column=1, pady=5, padx=5, sticky="W")

    patient_cabin_lbl = Label(patient_info, text="Cabin No:  ", width=18, font=("Arial", 10), border=1,
                              relief="solid")
    patient_cabin_lbl.grid(row=0, column=2, pady=5, padx=5, sticky="W")
    patient_cabin = Label(patient_info, text="----- ", width=18, font=("Arial", 10), border=1, relief="solid",
                          bg="white")
    patient_cabin.grid(row=0, column=3, pady=5, padx=5, sticky="W")

    patient_doa_lbl = Label(patient_info, text="Date of admission:  ", width=18, font=("Arial", 10), border=1,
                              relief="solid")
    patient_doa_lbl.grid(row=1, column=2, pady=5, padx=5, sticky="W")
    patient_doa = Label(patient_info, text="----- ", width=18, font=("Arial", 10), border=1, relief="solid",
                          bg="white")
    patient_doa.grid(row=1, column=3, pady=5, padx=5, sticky="W")

    patient_contact_lbl = Label(patient_info, text="Contact No:  ", width=18, font=("Arial", 10), border=1,
                              relief="solid")
    patient_contact_lbl.grid(row=2, column=0, pady=5, padx=5, sticky="W")
    patient_contact = Label(patient_info, text="----- ", width=18, font=("Arial", 10), border=1, relief="solid",
                          bg="white")
    patient_contact.grid(row=2, column=1, pady=5, padx=5, sticky="W")





    check_bill.configure(bg=ntactbg, fg=ntactfg)
    edit_medicine.configure(bg=ntactbg, fg=ntactfg)
    edit_patient.configure(bg=actbg, fg=actfg)
    print_bill.configure(bg=ntactbg, fg=ntactfg)
    btncreate_bill.configure(bg=ntactbg, fg=ntactfg)
    add_patient.configure(bg=ntactbg, fg=ntactfg)
    add_medicine.configure(bg=ntactbg, fg=ntactfg)
def getptninfo(p):
    global regno
    regno = p
    print(regno)
    # select_patient_for_billing.delete(0,END)
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
        )
    c = conn.cursor()
    data = c.execute("SELECT * FROM patient WHERE regno=%s", (regno,))
    rows = c.fetchone()
    print(rows)
    patient_id.config(text=rows[0])
    patient_cabin.config(text=rows[2])
    patient_regno.config(text=rows[1])
    patient_contact.config(text=rows[3])
    patient_doa.config(text=rows[10])

def edit_medicine():
    check_bill.configure(bg=ntactbg, fg=ntactfg)
    edit_medicine.configure(bg=actbg, fg=actfg)
    edit_patient.configure(bg=ntactbg, fg=ntactfg)
    print_bill.configure(bg=ntactbg, fg=ntactfg)
    btncreate_bill.configure(bg=ntactbg, fg=ntactfg)
    add_patient.configure(bg=ntactbg, fg=ntactfg)
    add_medicine.configure(bg=ntactbg, fg=ntactfg)

    add_patient_container = Frame(rightcontainer,
                                  width=1145, height=587,
                                  highlightbackground="#bdbdbd",
                                  highlightthickness=1)
    add_patient_container.grid(row=0, column=0, padx=5, pady=5)
    add_patient_container.grid_propagate(False)
    global transfer_medicine
    transfer_medicine = LabelFrame(add_patient_container,
                                   text="ADD Medicine Stock",
                                   width=1130, height=170,
                                   highlightbackground="#bdbdbd",
                                   highlightthickness=0,
                                   font=("Times", 20)
                                   )
    transfer_medicine.grid(row=0, column=0, pady=5, padx=5)
    transfer_medicine.grid_propagate(False)

    chng_from_med_lbl = Label(transfer_medicine, text="Medicine Name: ", width=14, font=("Arial", 10))
    chng_from_med_lbl.grid(row=0, column=0, pady=10, padx=5, sticky="W")
    chng_from_med = AutocompleteEntry(transfer_medicine, font=("Arial", 12), width=30)
    chng_from_med.set_completion_list(test_list)
    chng_from_med.grid(row=0, column=1, pady=5, padx=5)
    chng_from_med.focus_set()
    add_stock = Button(
        transfer_medicine,
        text="Get Info",
        height=1,
        width=20,
        command=lambda: getstock(chng_from_med.get())
    )
    add_stock.grid(row=0, column=2, padx=5, pady=5)
    available_stock_lbl = Label(transfer_medicine, text="In Stock: ", width=12, font=("Arial", 10))
    available_stock_lbl.grid(row=1, column=0, pady=10, padx=5, sticky="W")
    global available_stock


def new_stk_update(d1, d2, d3):
    print(d2)
    print(d1)
    new = (int(d1) + int(d2))
    print(new)
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )

    c = conn.cursor()
    update_stock = c.execute("UPDATE med SET instock = %s WHERE medname =%s", (new, d3,))
    conn.commit()
    new_add_stock.delete(0, END)
    getstock(d3)


def getstock(s1):
    print(s1)
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    records = c.execute("SELECT * FROM med WHERE medname=%s", (s1,))
    tt = c.fetchall()[0][5]
    print(tt)
    ttt = int(tt)
    available_stock = Entry(transfer_medicine, font=("Arial", 12), width=12)
    available_stock.grid(row=1, column=1, pady=5, padx=5)
    available_stock.insert(0, tt)
    available_stock.configure(state='disabled')
    new_add_stock_lbl = Label(transfer_medicine, text="ADD Stock: ", width=12, font=("Arial", 10))
    new_add_stock_lbl.grid(row=2, column=0, pady=10, padx=5, sticky="W")
    global new_add_stock
    new_add_stock = Entry(transfer_medicine, font=("Arial", 12), width=12)
    new_add_stock.grid(row=2, column=1, pady=5, padx=5)
    add_stock2 = Button(
        transfer_medicine,
        text="Add Stock",
        height=1,
        width=20,
        command=lambda: new_stk_update(new_add_stock.get(), tt, s1)
    )
    add_stock2.grid(row=2, column=2, padx=5, pady=5)


def modify_bill():
    check_bill.configure(bg=actbg, fg=actfg)
    edit_medicine.configure(bg=ntactbg, fg=ntactfg)
    edit_patient.configure(bg=ntactbg, fg=ntactfg)
    print_bill.configure(bg=ntactbg, fg=ntactfg)
    btncreate_bill.configure(bg=ntactbg, fg=ntactfg)
    add_patient.configure(bg=ntactbg, fg=ntactfg)
    add_medicine.configure(bg=ntactbg, fg=ntactfg)
    dumptempbill()
    add_patient_container = Frame(rightcontainer,
                                  width=1145, height=587,
                                  highlightbackground="#bdbdbd",
                                  highlightthickness=1)
    add_patient_container.grid(row=0, column=0, padx=5, pady=5)
    add_patient_container.grid_propagate(False)
    global modify_bill_container
    modify_bill_container = Frame(add_patient_container,
                                  width=1130, height=580,
                                  highlightbackground="#bdbdbd",
                                  highlightthickness=0)
    modify_bill_container.grid(row=0, column=0, padx=5, pady=5)
    modify_bill_container.grid_propagate(False)

    billll = LabelFrame(modify_bill_container,
                        text="Modify Bill",
                        width=1120, height=80,
                        highlightbackground="#bdbdbd",
                        highlightthickness=0
                        )
    billll.grid(row=0, column=0, pady=1, padx=5)
    billll.grid_propagate(False)
    serial_no_frame = Frame(modify_bill_container,
                            width=1120, height=40,
                            highlightbackground="#bdbdbd",
                            highlightthickness=1
                            )
    serial_no_frame.grid(row=1, column=0, pady=5, padx=5)
    serial_no_frame.grid_propagate(False)

    serial_no_lbl = Label(serial_no_frame, text="New Serial No: ", width=20, font=("Arial", 10))
    serial_no_lbl.grid(row=0, column=0, pady=5, padx=5, sticky="W")
    billnogenerator()
    global serial_no
    serial_no = Label(serial_no_frame, text=slno, width=20, font=("Arial", 10))
    serial_no.grid(row=0, column=1, pady=5, padx=5, sticky="W")

    modify_bill_tree_container = Frame(modify_bill_container,
                                       width=1120, height=390,
                                       highlightbackground="#bdbdbd",
                                       highlightthickness=0
                                       )
    modify_bill_tree_container.grid(row=2, column=0, pady=5, padx=5)
    modify_bill_tree_container.grid_propagate(False)
    global modify_bill_btn_container
    modify_bill_btn_container = Frame(modify_bill_container,
                                      width=1120, height=40,
                                      highlightbackground="#bdbdbd",
                                      highlightthickness=1
                                      )
    modify_bill_btn_container.grid(row=3, column=0, pady=5, padx=5)
    modify_bill_btn_container.grid_propagate(False)

    enter_prev_lbl = Label(billll, text="Enter Previous Bill No: ", width=20, font=("Arial", 12))
    enter_prev_lbl.grid(row=0, column=0, pady=5, padx=5, sticky="W")
    enter_prev = Entry(billll, font=("Arial", 12))
    enter_prev.grid(row=0, column=1, pady=15, padx=5)

    prev_bill_btn = Button(
        billll,
        text="Get Bill",
        height=1,
        width=25,
        command=lambda: get_prev_bill(enter_prev.get())
    )

    prev_bill_btn.grid(row=0, column=2, padx=10)
    global tree
    tree = ttk.Treeview(modify_bill_tree_container, show="headings", height=20,
                        columns=("medid", "medname", "quantity", "rate", "total"))
    treecolumnwid = 150
    tree.heading('medid', text="ID", anchor=W)
    tree.column("medid", minwidth=0, width=70, stretch=NO)
    tree.heading('medname', text="Medicine Name", anchor=CENTER)
    tree.column("medname", minwidth=0, width=450, stretch=NO)
    tree.heading('quantity', text="Quantiy", anchor=CENTER)
    tree.column("quantity", minwidth=0, width=200, stretch=NO)
    tree.heading('rate', text="Unit Price", anchor=CENTER)
    tree.column("rate", minwidth=0, width=200, stretch=NO)
    tree.heading('total', text="Total", anchor=CENTER)
    tree.column("total", minwidth=0, width=200, stretch=NO)
    tree.grid(row=0, column=0)


def onDoubleClick():
    print("Working")


def get_prev_bill(v1):
    dumptempbill()
    billnogenerator
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    global slno
    global vbill
    vbill = v1
    c = conn.cursor()
    data = c.execute(
        "INSERT INTO tempbill (billno,regid,medid,medname,quantity,rate,total) SELECT %s,regid,medid,medname,quantity,rate,total FROM finalbill WHERE billno =%s",
        (slno, v1))
    conn.commit()

    conn.close()
    updatetempbill2()
    totalbillprev2()
    edit_bill = Button(
        modify_bill_btn_container,
        text="Edit Quantity",
        height=1,
        width=25,
        command=edit_temp_bill,
        highlightcolor="black",
        highlightthickness=1
    )
    edit_bill.grid(row=0, column=2, padx=5, pady=5)
    gen_bill = Button(
        modify_bill_btn_container,
        text="Generate New Bill",
        height=1,
        width=25,
        command=gen_new_bill,
        highlightcolor="black",
        highlightthickness=1
    )
    gen_bill.grid(row=0, column=3, padx=0, pady=5)


def totalbillprev2():
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )

    c = conn.cursor()
    data = c.execute("SELECT SUM(total) AS totalbill FROM tempbill;")
    getdata = c.fetchone()[0]
    # print(getdata)
    totalbillpreview_lbl = Label(modify_bill_btn_container, text="Total Bill: ",
                                 width=15,
                                 bg="#6760a6",
                                 fg="white")
    totalbillpreview_lbl.grid(row=0, column=0, sticky="nsew")
    totalbillpreview_lbl.config(font=("Times new roman", 12))

    global totalbillpreview_amnt
    totalbillpreview_amnt = Label(modify_bill_btn_container, text=str(getdata), width=20,
                                  bg="#4d4c4c",
                                  fg="yellow")
    totalbillpreview_amnt.grid(row=0, column=1, sticky="nsew")
    totalbillpreview_amnt.config(font=("Times new roman", 12))


def savetofinalbill2():
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    data = c.execute(
        "INSERT INTO finalbill (billno,regid,medid,medname,quantity,rate,total) SELECT billno,regid,medid,medname,quantity,rate,total FROM tempbill")
    conn.commit()
    billnoupdate()


def get_details():
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    data = c.execute("SELECT * FROM tempbill")
    rows = c.fetchall()
    # print(rows[1][3])
    global slno2
    slno2 = rows[0][1]
    print(slno2)
    global regid2
    regid2 = rows[0][2]
    print(regid2)


def getnames2():
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    data = c.execute("SELECT * FROM patient WHERE regno=%s", (regid2,))
    rows = c.fetchall()

    global ptn_name
    global cbn_no
    global phn_no
    global regi_no
    ptn_name = rows[0][4]
    cbn_no = rows[0][2]
    phn_no = rows[0][3]
    regi_no = rows[0][1]


def chng_stk_update(g1, g2):
    print("------------")
    print(g1)
    print(g2)
    print("------------")

    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )

    c = conn.cursor()
    update_stock = c.execute("UPDATE med SET instock = %s WHERE medid =%s", (g2, g1,))
    conn.commit()


def chng_rtn_stk(f1, f2):
    crn_stk = chk_crn_stk(f1)
    upd_stk = (int(crn_stk) + int(f2))
    chng_stk_update(f1, upd_stk)


def chk_crn_stk(u1):
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    records = c.execute("SELECT * FROM med WHERE medid=%s", (u1,))
    tt = c.fetchall()[0][5]
    print(tt)
    return tt

def fpurchase_bill():
    dumpinvbill()
    add_patient_container = Frame(rightcontainer,
                                  width=1145, height=587,
                                  highlightbackground="#bdbdbd",
                                  highlightthickness=1)
    add_patient_container.grid(row=0, column=0, padx=5, pady=5)
    add_patient_container.grid_propagate(False)

    product_info = LabelFrame(add_patient_container,
                              text="Purchase Info / Stock Inventory",
                              width=1130, height=420,
                              highlightbackground="#bdbdbd",
                              highlightthickness=0,
                              bg="white"
                              )
    product_info.grid(row=3, column=0, pady=5, padx=5)
    product_info.grid_propagate(False)
    purchase_info = Frame(product_info,
                                 width=1115, height=90,
                                 highlightbackground="#bdbdbd",
                                 highlightthickness=1,
                          bg="#ccfcbb")
    purchase_info.grid(row=0, column=0, padx=5, pady=5)
    purchase_info.grid_propagate(False)

    purchase_items = Frame(product_info,
                                 width=1115, height=40,
                                 highlightbackground="#bdbdbd",
                                 highlightthickness=1)
    purchase_items.grid(row=1, column=0, padx=5, pady=5)
    purchase_items.grid_propagate(False)
    purchase_bill_items = Frame(product_info,
                           width=1115, height=150,
                           highlightbackground="#bdbdbd",
                           highlightthickness=1)
    purchase_bill_items.grid(row=2, column=0, padx=5, pady=5)
    purchase_bill_items.grid_propagate(False)
    #===============Invoice adding=======================
    invoice_no_lbl = Label(purchase_info, text="Invoice No: ", width=10,
                                           font=("AdobeGothicStd-Bold", 11),bg="#ccfcbb")
    invoice_no_lbl.grid(row=0, column=0, padx=5, pady=10)
    invoice_no = Entry(purchase_info, font=("Arial", 10),border=1,relief="solid")
    invoice_no.grid(row=0, column=1)

    invoice_date_lbl = Label(purchase_info, text="Invoice Date: ", width=10,
                                           font=("AdobeGothicStd-Bold", 11),bg="#ccfcbb")
    invoice_date_lbl.grid(row=0, column=2, padx=15, pady=10)
    invoice_date = Entry(purchase_info, font=("Arial", 10),border=1,relief="solid")
    invoice_date.grid(row=0, column=3)


    supplier_name_lbl = Label(purchase_info, text="Supplier's Name: ", width=20,
                                           font=("AdobeGothicStd-Bold", 11),bg="#ccfcbb")
    supplier_name_lbl.grid(row=1, column=0, padx=15, pady=5)

    #supplier_name = Entry(purchase_info, font=("Arial", 10),border=1,relief="solid")
    #supplier_name.grid(row=1, column=1)

    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    s_name = []
    c = conn.cursor()
    data = c.execute("SELECT * FROM supplier")
    rows = c.fetchall()
    for row in rows:
        # print(row[1])
        s_name.append(row[1])
    # print(mednames)
    global variables
    variables=StringVar(purchase_info)
    variables.set(s_name[0])
    supplier=OptionMenu(purchase_info,variables,*s_name,)
    supplier.grid(row=1,column=1)

    medi_name_lbl = Label(purchase_items, text="Medicine Name: ", width=15,
                              font=("AdobeGothicStd-Bold", 11))
    medi_name_lbl.grid(row=0, column=0, padx=5, pady=5)
    puchased_med = AutocompleteEntry(purchase_items, font=("Arial", 11), width=25, border=1, relief="solid")
    puchased_med.set_completion_list(test_list)
    puchased_med.grid(row=0, column=1, pady=5, padx=5)
    puchased_med.focus_set()
    medi_qnty_lbl = Label(purchase_items, text="Quantity (In Pcs): ", width=15,
                          font=("AdobeGothicStd-Bold", 11))
    medi_qnty_lbl.grid(row=0, column=2, padx=5, pady=5)
    med_qnty = Entry(purchase_items, font=("Arial", 11), border=1, width=10, relief="solid")
    med_qnty.grid(row=0, column=3, padx=5, pady=5)
    medi_price_lbl = Label(purchase_items, text="Total Cost (incl. VAT/TAX) : ", width=25,
                          font=("AdobeGothicStd-Bold", 11))
    medi_price_lbl.grid(row=0, column=4, padx=2, pady=5)
    med_price = Entry(purchase_items, font=("Arial", 11), border=1, width=10, relief="solid")
    med_price.grid(row=0, column=5, padx=5, pady=5)
    add_med = Button(
        purchase_items,
        text="ADD",
        height=1,
        width=20,
        command=lambda: savetotempinv(invoice_no.get(), invoice_date.get(),variables.get(),puchased_med.get(),med_qnty.get(),med_price.get()),
        highlightcolor="black",
        highlightthickness=1,
        border=1, relief="solid"
    )
    add_med.grid(row=0, column=6, padx=5, pady=5)
    add_med.configure(bg="green", fg="yellow")
    global treebill
    treebill = ttk.Treeview(purchase_bill_items, show="headings", height=20,
                        columns=("medid", "medname", "quantity", "rate", "total"))
    treecolumnwid = 150
    treebill.heading('medid', text="ID", anchor=W)
    treebill.column("medid", minwidth=0, width=50, stretch=NO)
    treebill.heading('medname', text="Medicine Name", anchor=CENTER)
    treebill.column("medname", minwidth=0, width=300, stretch=NO)
    treebill.heading('quantity', text="Quantiy", anchor=CENTER)
    treebill.column("quantity", minwidth=0, width=200, stretch=NO)
    treebill.heading('rate', text="Unit Price", anchor=CENTER)
    treebill.column("rate", minwidth=0, width=200, stretch=NO)
    treebill.heading('total', text="Total", anchor=CENTER)
    treebill.column("total", minwidth=0, width=200, stretch=NO)
    treebill.grid(row=2, column=0)

    billing_btn_containerinv = Frame(product_info,
                                  width=1115, height=30,
                                  highlightbackground="#bdbdbd",
                                  highlightthickness=1,
                                  bg="yellow")
    billing_btn_containerinv.grid(row=3, column=0, padx=1, pady=5)
    billing_btn_containerinv.grid_propagate(False)
    save_bill_btn_inv = Button(
        billing_btn_containerinv,
        text="Save Invoice",
        height=1,
        width=15,
        command=save_invoice,
        highlightcolor="black",
        highlightthickness=1
    )
    save_bill_btn_inv.grid(row=0,column=0)
    mod_bill_btn = Button(
        billing_btn_containerinv,
        text="Modify Invoice",
        height=1,
        width=15,
        command=edit_invoice,
        highlightcolor="black",
        highlightthickness=1
    )
    mod_bill_btn.grid(row=0, column=1, padx=1, pady=1)
    mod_bill_btn.configure(bg="blue", fg="yellow")


    down_bill_btn = Button(
        billing_btn_containerinv,
        text="Download Purchase Report",
        height=1,
        width=25,
        command=down_inv_report,
        highlightcolor="black",
        highlightthickness=1
    )
    down_bill_btn.grid(row=0, column=2, padx=1, pady=1)
    down_bill_btn.configure(bg="red", fg="yellow")

def down_inv_report():
    win = tkinter.Tk()
    win.title('Download Purchase History')
    win.resizable(width=False, height=False)
    win.geometry('{}x{}'.format(400, 200))
    win.configure(bg="#99c7ff")
    #medi_name_lbl = Label(win, text="Medicine Name: ", width=15,
    #                          font=("AdobeGothicStd-Bold", 11))
    #medi_name_lbl.grid(row=0, column=0, padx=5, pady=5)
    #query_med = AutocompleteEntry(win, font=("Arial", 11), width=25, border=1, relief="solid")
    #query_med.set_completion_list(test_list)
    #query_med.grid(row=0, column=1, pady=5, padx=5)
    #query_med.focus_set()

    date1_lbl = Label(win, text="Date From: ", width=15,
                      font=("AdobeGothicStd-Bold", 11))
    date1_lbl.grid(row=1, column=0, padx=5, pady=5)
    date1 = Entry(win, font=("Arial", 10), border=1, relief="solid")
    date1.grid(row=1, column=1)


    date2_lbl = Label(win, text="Date From: ", width=15,
                      font=("AdobeGothicStd-Bold", 11))
    date2_lbl.grid(row=2, column=0, padx=5, pady=5)
    date2 = Entry(win, font=("Arial", 10), border=1, relief="solid")
    date2.grid(row=2, column=1)

    view_med = Button(
        win,
        text="View Report",
        height=1,
        width=20,
        command=lambda: geninvreport(date1.get(),date2.get()),
        highlightcolor="black",
        highlightthickness=1,
        border=1, relief="solid"
    )
    view_med.grid(row=3, column=1, padx=5, pady=5)
    view_med.configure(bg="green", fg="yellow")

    def grabdata(b, d):
        print(b, d)
        conn = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=pass_word,
            database="ncpharmacy"
        )
        c = conn.cursor()
        # data = c.execute("SELECT * FROM finalinvoice WHERE invoicedate BETWEEN %s AND %s;", (b, c))
        # data= c.execute("SELECT * FROM finalinvoice ;")
        print("2222233334")
        data = c.execute("SELECT * FROM finalinvoice WHERE invoicedate BETWEEN %s AND %s;", (b, d,))
        #data = c.execute("SELECT * FROM finalinvoice WHERE invoicedate BETWEEN '2000-01-01' AND  '2022-01-01';")

        print("22222")
        rows = c.fetchall()
        lsp = 120

        pagin = 0
        totalinvamnt = 0
        for row in rows:
            if pagin < 40:
                p.setFont("Courier-Bold", 8)
                p.drawString(45, lsp, str(row[1]))
                p.drawString(130, lsp, str(row[2]))
                p.drawString(200, lsp, str(row[4][0:21]))
                p.drawString(350, lsp, str(row[5]))
                p.drawString(450, lsp, str(row[6]))
                p.drawString(510, lsp, str(row[8]))
                p.drawString(40, lsp + 7,
                             "-----------------------------------------------------------------------------------------------------------")
                lsp = lsp + 20
                pagin = pagin + 1
                print(row[1])
                totalinvamnt = totalinvamnt + row[8]
            else:
                pagin = 0
                lsp = 120
                print(row[1])
                print("---")
                p.showPage()
                invtemplate(b,d)
                p.setFont("Courier-Bold", 8)
                p.drawString(45, lsp, str(row[1]))
                p.drawString(130, lsp, str(row[2]))
                p.drawString(200, lsp, str(row[4][0:21]))
                p.drawString(350, lsp, str(row[5]))
                p.drawString(450, lsp, str(row[6]))
                p.drawString(510, lsp, str(row[8]))
                p.drawString(40, lsp + 7,
                             "-----------------------------------------------------------------------------------------------------------")
                lsp = lsp + 20
                totalinvamnt = totalinvamnt + row[8]
        print(totalinvamnt)

    def geninvreport(m, n):
        global p
        p = canvas.Canvas("Purchase Report.pdf", pagesize=(595, 842), bottomup=0)
        invtemplate(m,n)
        grabdata(m, n)
        p.showPage()
        p.save()
        print(m)

    def invtemplate(u,i):
        p.translate(10, 40)
        p.scale(1, -1)
        p.scale(1, -1)
        p.translate(-10, -40)
        p.setFont("Helvetica-Bold", 12)
        p.drawCentredString(300, 30, "Pharmacy Management System")
        # p.roundRect(30, 20, 530, 800, 2, stroke=1, fill=0)
        p.setFont("Helvetica-Bold", 8)
        p.drawCentredString(300, 45, "75, Ananya Residential Area, CHITTAGONG")
        p.drawCentredString(300, 55, "PHONE: 01748807540, 653524899")
        p.line(30, 65, 560, 65)
        p.roundRect(150, 70, 300, 15, 5, stroke=1, fill=0)
        p.setFont("Courier-Bold", 10)
        p.drawCentredString(300, 80, "Purchase Bill From "+ u +" to "+ i )
        # p.roundRect(40, 155, 190, 22, 0, stroke=1, fill=0)
        # p.roundRect(235, 155, 150, 22, 0, stroke=1, fill=0)
        # p.roundRect(390, 155, 160, 22, 0, stroke=1, fill=0)
        # p.roundRect(40, 180, 345, 22, 0, stroke=1, fill=0)
        # p.roundRect(390, 180, 160, 22, 0, stroke=1, fill=0)
        # p.roundRect(40, 210, 510, 550, 0, stroke=1, fill=0)
        # p.line(40, 230, 550, 230)

        # p.line(80, 210, 80, 760)
        # p.line(400, 210, 400, 760)
        # p.line(460, 210, 460, 760)
        # p.setFont("Times-Bold", 10)
        p.drawString(45, 100, "Invoice")
        p.drawString(130, 100, "Date")
        p.drawString(220, 100, "Supplier")
        p.drawString(350, 100, "Item")
        p.drawString(450, 100, "Quantity")
        p.drawString(510, 100, "Price")
        p.drawCentredString(300, 800,
                            "--------------------------------------------------------------------------------")
        p.drawCentredString(300, 810, "This is software generated purchase report")

    win.mainloop()
def save_invoice():
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    records = c.execute("SELECT * FROM purchaseinvoice")
    rows = c.fetchall()
    for row in rows:
        medname=row[5]
        print(medname)
        medquantity=int(row[6])
        print("med quantity")
        print(medquantity)
        stock=int(available_med(medname))
        print("avaiable stock")
        print(stock)
        new_quantity=(medquantity+stock)
        print("New Quantity"+str(new_quantity))
        add_stk_update(medname,new_quantity)
    savetofinalinvoice()
    dumpinvbill()
    updateinvbill()    

def savetofinalinvoice():
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    data = c.execute(
        "INSERT INTO finalinvoice (slno,invoiceno,invoicedate,inputdate,supplier,med,quantity,unitprice,totalprice) SELECT slno,invoiceno,invoicedate,inputdate,supplier,med,quantity,unitprice,totalprice FROM purchaseinvoice")
    conn.commit()    
def add_stk_update(d1, d2):
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )

    c = conn.cursor()
    update_stock = c.execute("UPDATE med SET instock = %s WHERE medname =%s", (d2, d1,))
    conn.commit()
    conn.close()
def available_med(s1):
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    records = c.execute("SELECT * FROM med WHERE medname=%s", (s1,))
    tt = c.fetchall()[0][5]
    print(tt)
    return tt

def savetotempinv(m1,m2,m3,m4,m5,m6):
    dt=chk_inv_med(m4)
    dtt=int(dt)
    if dtt == 1:
        messagebox.showinfo("Error", "Sorry Medicine is Already in the Bill")
    else:
        m7=int(m6)/int(m5)
        conn = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=pass_word,
            database="ncpharmacy"
        )
        c = conn.cursor()
        c.execute(
            "INSERT INTO purchaseinvoice (invoiceno,invoicedate,supplier,med,quantity,unitprice,totalprice) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (m1,m2,m3,m4,m5,m7,m6))
        conn.commit()
        print ("Sucessfully submitted data to invoice")
        conn.close()
        print(m1)
        print(m2)
        print(m3)
        print(m4)
        print(m5)
        print(m6)
        updateinvbill()
def chk_inv_med(c1):
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()

    med_name_chk = c.execute("SELECT * FROM purchaseinvoice WHERE med=%s", (c1,))
    temp_med = c.fetchone()
    if temp_med != None:
        print("Med found")
        return 1
    else:
        print("No med found")
        return 0
def updateinvbill():
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    c = conn.cursor()
    records = c.execute("SELECT * FROM purchaseinvoice")
    tempbilldata = c.fetchall()

    # print(tempbilldata)
    fatcheddata = treebill.get_children()
    for elements in fatcheddata:
        treebill.delete(elements)
    # print (fatcheddata)
    for row in tempbilldata:
        treebill.insert("", tkinter.END, values=(row[3], row[4], row[5], row[6], row[7]))
    conn.commit()
    conn.close()

def chng_state():
    # print("+++++++++")
    # print(vbill)
    # print("+++++++++")
    statee = 1
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )

    c = conn.cursor()
    update_stock = c.execute("UPDATE finalbill SET status = %s WHERE billno =%s", (statee, vbill,))
    conn.commit()


def gen_new_bill():
    chng_rtn_stk(chnge_medid, chnge_qnty)
    chng_state()
    savetofinalbill2()
    get_details()
    getnames2()
    global p

    p = canvas.Canvas(slno2 + ".pdf", pagesize=(595, 842), bottomup=0)
    getbilldata()
    totalbillfinal()
    p.translate(10, 40)
    p.scale(1, -1)
    p.scale(1, -1)
    p.translate(-10, -40)
    p.setFont("Helvetica-Bold", 30)
    p.drawCentredString(300, 60, "Pharmacy Managenet System")
    p.roundRect(30, 20, 530, 800, 2, stroke=1, fill=0)
    p.setFont("Helvetica-Bold", 12)
    p.drawCentredString(300, 80, "75, Anannya Resident Area, CHITTAGONG")
    p.drawCentredString(300, 95, "PHONE: 01748807540, 0994959845")
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
    p.drawString(130, 170, slno2)
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
    p.showPage()
    # Saving the PDF
    p.save()
    dumptempbill()
    updatetempbill()
    billnogenerator()
    billnoupdate()
def edit_invoice():
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    mednames = []
    c = conn.cursor()
    data = c.execute("SELECT * FROM purchaseinvoice")
    rows = c.fetchall()
    for row in rows:
            # print(row[1])
        mednames.append(row[5])
        print(mednames)
    win = tkinter.Tk()
    win.title('Edit Item')
    win.resizable(width=False, height=False)
    win.geometry('{}x{}'.format(400, 200))
    win.configure(bg="#99c7ff")

    global variable
    variable = StringVar(win)
    variable.set(mednames[0])
    meds = OptionMenu(win, variable, *mednames)
    meds.grid(row=0, column=1)
    med_id_lbl = Label(win, text="Select Medicine: ", width=20, font=("Arial", 12))
    med_id_lbl.grid(row=0, column=0, pady=20, padx=5, sticky="W")
    global med_id_rsv
    # med_id_rsv = Entry(win, font=("Arial", 12))
    # med_id_rsv.grid(row=0, column=1, pady=20, padx=5)


        # Delete button
    delete_item = Button(
            win,
            text="Remove",
            height=2,
            width=25,
            command=lambda: delete_inv_item(variable.get())
        )

    delete_item.grid(row=3, column=0)
    delete_item.configure(bg="red", fg="yellow")
        #End of invoice
def delete_inv_item(c1):
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    print(c1)
    print("Printing from delete item")
    c = conn.cursor()
    get_med_rate = c.execute("DELETE FROM purchaseinvoice WHERE med=%s", (c1,))
    conn.commit()
    updateinvbill()

def edit_item():
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    mednames = []
    c = conn.cursor()
    data = c.execute("SELECT * FROM tempbill")
    rows = c.fetchall()
    for row in rows:
        # print(row[1])
        mednames.append(row[4])
    # print(mednames)
    win = tkinter.Tk()
    win.title('Edit Item')
    win.resizable(width=False, height=False)
    win.geometry('{}x{}'.format(400, 200))
    win.configure(bg="#99c7ff")

    global variable
    variable=StringVar(win)
    variable.set(mednames[0])
    meds=OptionMenu(win,variable,*mednames)
    meds.grid(row=0,column=1)
    med_id_lbl = Label(win, text="Select Medicine: ", width=20, font=("Arial", 12))
    med_id_lbl.grid(row=0, column=0, pady=20, padx=5, sticky="W")
    global med_id_rsv
    #med_id_rsv = Entry(win, font=("Arial", 12))
    #med_id_rsv.grid(row=0, column=1, pady=20, padx=5)

    new_qnty_lbl = Label(win, text="New Quantity: ", width=20, font=("Arial", 12))
    new_qnty_lbl.grid(row=1, column=0, pady=10, padx=5, sticky="W")
    global rtn_qnty
    new_qnty = Entry(win, font=("Arial", 12))
    new_qnty.grid(row=1, column=1, pady=10, padx=5)
    save_new_qnty = Button(
        win,
        text="Save",
        height=2,
        width=25,
        command=lambda: new_item_qnty(variable.get(), new_qnty.get())
    )

    save_new_qnty.grid(row=3, column=1)
    save_new_qnty.configure(bg="green",fg="yellow")
    #Delete button
    delete_item = Button(
        win,
        text="Remove",
        height=2,
        width=25,
        command=lambda: delete_bill_item(variable.get())
    )

    delete_item.grid(row=3, column=0)
    delete_item.configure(bg="red", fg="yellow")
def delete_bill_item(c1):
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    print(c1)
    print("Printing from delete item")
    c = conn.cursor()
    get_med_rate = c.execute("DELETE FROM tempbill WHERE medname=%s", (c1,))
    conn.commit()
    updatetempbill()
    totalbillpreview()

def get_medrate(p1):
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    print(p1)
    print("Printing from medrate")
    c = conn.cursor()
    get_med_rate = c.execute("SELECT rate FROM tempbill WHERE medname=%s",(p1,))
    rows = c.fetchone()[0]
    #print (rows)
    return rows
def new_item_qnty(n1,n2):
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    t1="00"
    rate=get_medrate(n1)
    print(rate)
    new_total=int(n2)*int(rate)
    print("this is med rate")
    c = conn.cursor()
    update_stock = c.execute("UPDATE tempbill SET quantity = %s,total=%s WHERE medname =%s",
                             (n2, new_total,n1))
    conn.commit()
    print(n1)
    print(n2)
    totalbillpreview()
    updatetempbill()

def edit_temp_bill():
    win = tkinter.Tk()
    win.title('Edit Quantity')
    win.resizable(width=False, height=False)
    win.geometry('{}x{}'.format(400, 200))

    med_id_lbl = Label(win, text="Medicine ID: ", width=20, font=("Arial", 12))
    med_id_lbl.grid(row=0, column=0, pady=20, padx=5, sticky="W")
    global med_id_rsv
    med_id_rsv = Entry(win, font=("Arial", 12))
    med_id_rsv.grid(row=0, column=1, pady=20, padx=5)

    rtn_qnty_lbl = Label(win, text="Returned Quantity: ", width=20, font=("Arial", 12))
    rtn_qnty_lbl.grid(row=1, column=0, pady=10, padx=5, sticky="W")
    global rtn_qnty
    rtn_qnty = Entry(win, font=("Arial", 12))
    rtn_qnty.grid(row=1, column=1, pady=10, padx=5)
    save_rtn_qnty = Button(
        win,
        text="Save",
        height=2,
        width=25,
        command=lambda: rsv_stk_chng(med_id_rsv.get(), rtn_qnty.get())
    )

    save_rtn_qnty.grid(row=3, column=1)

    def crnt_med_rate(r1):
        conn = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=pass_word,
            database="ncpharmacy"
        )

        c = conn.cursor()
        crnt_rate = c.execute("SELECT medprice FROM med WHERE medid=%s ", (r1,))
        rows = c.fetchone()[0]
        # print(rows)

        return rows

    def chk_stk(t1, t2):
        conn = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=pass_word,
            database="ncpharmacy"
        )
        c = conn.cursor()
        records = c.execute("SELECT * FROM med WHERE medid=%s", (t1,))
        tt = c.fetchall()[0][5]
        tt = int(tt)
        if int(t2) <= tt:
            return 1
        else:
            return 0

    def new_qntity(y1, y2):

        global add_rtn_quanty
        add_rtn_quanty = int(y2)
        conn = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=pass_word,
            database="ncpharmacy"
        )
        c = conn.cursor()
        records = c.execute("SELECT quantity FROM tempbill WHERE medid=%s", (y1,))
        tt = c.fetchone()[0]
        # print(tt)
        tt = int(tt) - int(y2)
        print(tt)
        if int(tt) < 0:
            return "x"
        else:
            return tt
        # print(tt)

    def rsv_stk_chng(e1, e2):
        global chnge_medid
        global chnge_qnty
        chnge_medid = int(e1)
        chnge_qnty = int(e2)
        new_qntity_data = new_qntity(e1, e2)
        print(new_qntity_data)
        if new_qntity_data == "x":
            messagebox.showinfo("Error", "Returned Quantity Can't be Greater then Sold Quantity")
        # print(new_qntity_data)
        else:
            chk_data = int(chk_stk(e1, e2))
            if chk_data == 1:
                rate = int(crnt_med_rate(e1))
                total = (rate * int(new_qntity_data))
                # print(total)
                conn = mysql.connector.connect(
                    host=host_name,
                    user=user_name,
                    password=pass_word,
                    database="ncpharmacy"
                )

                c = conn.cursor()
                update_stock = c.execute("UPDATE tempbill SET quantity = %s,total=%s WHERE medid =%s",
                                         (new_qntity_data, total, e1,))
                conn.commit()
                med_id_rsv.delete(0, END)
                rtn_qnty.delete(0, END)
                updatetempbill()
                totalbillprev2()
                win.destroy()
            else:
                messagebox.showinfo("Error", "This Medicine is not is stock")

    win.mainloop()


# =============functions ending==========

# photo = PhotoImage(file = r"C:\Users\user\PycharmProjects\PharmacyManagement\test.png")
# photoimage = photo.subsample(10, 10)

# ===========Containers===============
displaycontainer = Frame(
    root,
    width=1366,
    height=768,
    highlightbackground="#bdbdbd",
    highlightthickness=1
)
displaycontainer.grid(row=0, column=0, padx=margincenter)
displaycontainer.grid_propagate(False)

bannercontainer = Frame(
    displaycontainer,
    width=1366,
    height=80,
    bg="#2426d1",
    highlightbackground="#bdbdbd",
    highlightthickness=1
)
bannercontainer.grid(row=0, column=0)
bannercontainer.grid_propagate(False)

maincontainer = Frame(
    displaycontainer,
    width=1366,
    height=600,
    highlightbackground="#bdbdbd",
    highlightthickness=1
)
maincontainer.grid(row=1, column=0, pady=5)
maincontainer.grid_propagate(False)

leftmenucontainer = Frame(
    maincontainer,
    width=200,
    height=598,
    bg="#638be0",
    highlightbackground="#bdbdbd",
    highlightthickness=1
)
leftmenucontainer.grid(row=0, column=0)
leftmenucontainer.grid_propagate(False)

rightcontainer = Frame(
    maincontainer,
    width=1155,
    height=598,
    bg="#d9e6fa",
    highlightbackground="#bdbdbd",
    highlightthickness=1
)
rightcontainer.grid(row=0, column=1)
rightcontainer.grid_propagate(False)

copyrightcontainer = Frame(
    displaycontainer,
    width=1366,
    height=30,
    highlightbackground="#bdbdbd",
    highlightthickness=1
)
copyrightcontainer.grid(row=2, column=0, pady=5)
copyrightcontainer.grid_propagate(False)

# ============Container Ending===================

# =====button =========
# b1 = Button(maincontainer, text="True", height=5, width=50,command=toggle)
# b1.grid(row=0, column=0)
# b1['state']="disabled"
myFont = font.Font(family='times', size=12, weight='normal')

add_medicine = Button(
    leftmenucontainer,
    text="Add Medicine/Supplier",
    height=2,
    width=20,
    font=myFont,
    border=2,
    relief="solid",
    command=add_medicine
)
add_medicine.grid(row=0, column=0, padx=5, pady=5)

add_patient = Button(
    leftmenucontainer,
    text="Add patient",
    height=2,
    width=20,
    font=myFont,
    border=2,
    relief="solid",
    command=add_patient
)
add_patient.grid(row=1, column=0, padx=5, pady=5)

btncreate_bill = Button(
    leftmenucontainer,
    text="Create Bill",
    height=2,
    width=20,
    font=myFont,
    border=2,
    relief="solid",
    command=screate_bill
)
btncreate_bill.grid(row=2, column=0, padx=5, pady=5)

print_bill = Button(
    leftmenucontainer,
    text="Print Bill",
    height=2,
    width=20,
    font=myFont,
    border=2,
    relief="solid",
    command=print_bills
)
print_bill.grid(row=3, column=0, padx=5, pady=5)

edit_patient = Button(
    leftmenucontainer,
    text="Patient View",
    height=2,
    width=20,
    font=myFont,
    border=2,
    relief="solid",
    command=edit_patient
)
edit_patient.grid(row=4, column=0, padx=5, pady=5)

edit_medicine = Button(
    leftmenucontainer,
    text="Edit Medicine",
    height=2,
    border=2,
    relief="solid",
    width=20,
    font=myFont,
    command="edit_medicine"
)
edit_medicine.grid(row=5, column=0, padx=5, pady=5)
check_bill = Button(
    leftmenucontainer,
    text="Modify Bill",
    height=2,
    width=20,
    border=2,

    font=myFont,
    relief="solid",
    #bg="#caffc9",
    command=modify_bill
)
check_bill.grid(row=6, column=0, padx=5, pady=5)

purchase_bill = Button(
    leftmenucontainer,
    text="Purchase Bill",
    height=2,
    width=20,
    border=2,

    font=myFont,
    relief="solid",
    #bg="#caffc9",
    command=fpurchase_bill
)
purchase_bill.grid(row=7, column=0, padx=5, pady=5)


def report_viewf():
    add_patient_container = Frame(rightcontainer,
                                  width=1145, height=587,
                                  highlightbackground="#bdbdbd",
                                  highlightthickness=1)
    add_patient_container.grid(row=0, column=0, padx=5, pady=5)
    add_patient_container.grid_propagate(False)

    product_info = LabelFrame(add_patient_container,
                              text="Report View",
                              width=1130, height=420,
                              highlightbackground="#bdbdbd",
                              highlightthickness=0,
                              bg="white"
                              )
    product_info.grid(row=3, column=0, pady=5, padx=5)
    product_info.grid_propagate(False)


    searchbar = Frame(product_info,
                                 width=1115, height=40,
                                 highlightbackground="#bdbdbd",
                                 highlightthickness=1)
    searchbar.grid(row=1, column=0, padx=5, pady=5)
    searchbar.grid_propagate(False)

    medi_name_lbl = Label(searchbar, text="Medicine Name: ", width=15,
                              font=("AdobeGothicStd-Bold", 11))
    medi_name_lbl.grid(row=0, column=0, padx=5, pady=5)
    query_med = AutocompleteEntry(searchbar, font=("Arial", 11), width=25, border=1, relief="solid")
    query_med.set_completion_list(test_list)
    query_med.grid(row=0, column=1, pady=5, padx=5)
    query_med.focus_set()
    date1_lbl = Label(searchbar, text="Date From: ", width=15,
                      font=("AdobeGothicStd-Bold", 11))
    date1_lbl.grid(row=0, column=2, padx=5, pady=5)
    date1 = Entry(searchbar, font=("Arial", 10), border=1, relief="solid")
    date1.grid(row=0, column=3)


    date2_lbl = Label(searchbar, text="Date From: ", width=15,
                      font=("AdobeGothicStd-Bold", 11))
    date2_lbl.grid(row=0, column=4, padx=5, pady=5)
    date2 = Entry(searchbar, font=("Arial", 10), border=1, relief="solid")
    date2.grid(row=0, column=5)

    view_med = Button(
        searchbar,
        text="Check",
        height=1,
        width=20,
        command=lambda: check_med(query_med.get(),date1.get(),date2.get()),
        highlightcolor="black",
        highlightthickness=1,
        border=1, relief="solid"
    )
    view_med.grid(row=0, column=6, padx=5, pady=5)
    view_med.configure(bg="green", fg="yellow")
    #===========================
    resultview = Frame(product_info,
                                 width=1115, height=200,
                                 highlightbackground="#bdbdbd",
                                 highlightthickness=1)
    resultview.grid(row=2, column=0, padx=5, pady=5)
    resultview.grid_propagate(False)

    global treeres
    treeres = ttk.Treeview(resultview, show="headings", height=20,
                        columns=("billno", "regid", "medname", "quantity", "date"))
    treecolumnwid = 150
    treeres.heading('billno', text="Bill No", anchor=W)
    treeres.column("billno", minwidth=0, width=50, stretch=NO)
    treeres.heading('regid', text="Registration No", anchor=CENTER)
    treeres.column("regid", minwidth=0, width=200, stretch=NO)
    treeres.heading('medname', text="Medicine Name", anchor=CENTER)
    treeres.column("medname", minwidth=0, width=400, stretch=NO)
    treeres.heading('quantity', text="Quantiy", anchor=CENTER)
    treeres.column("quantity", minwidth=0, width=200, stretch=NO)
    treeres.heading('date', text="Date", anchor=CENTER)
    treeres.column("date", minwidth=0, width=200, stretch=NO)
    treeres.grid(row=2, column=0)


def check_med(m1,m2,m3):
    conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pass_word,
        database="ncpharmacy"
    )
    state = "0"
    c = conn.cursor()
    records = c.execute("SELECT * FROM finalbill WHERE medname=%s AND status =%s AND date BETWEEN %s AND %s;",
                     (m1, state, m2, m3,))

    med_data=c.fetchall()
    print(med_data)
    fatcheddata = treeres.get_children()
    for elements in fatcheddata:
        treeres.delete(elements)
    # print (fatcheddata)
    for row in med_data:
        treeres.insert("", tkinter.END, values=(row[1], row[2], row[4], row[5], row[8]))
    conn.commit()
    conn.close()

report_view = Button(
    leftmenucontainer,
    text="Report View",
    height=2,
    width=20,
    border=2,

    font=myFont,
    relief="solid",
    #bg="#caffc9",
    command=report_viewf
    )
report_view.grid(row=8, column=0, padx=5, pady=5)



# =====button ending========
#727375
headername = Label(bannercontainer, text="Pharmacy Management System", bg="#2426d1", fg="#fafcff")
headername.grid(row=0, column=0, padx=15, pady=10)
headername.config(font=("Times new roman", 30))

copyrightinfo = Label(copyrightcontainer, text="Developed by Rahul Mitra", width=180)
copyrightinfo.grid(row=0, column=0, sticky="nsew")
copyrightinfo.config(font=("Times new roman", 10))
# print(scrheight)
# print(scrwidth)

root.mainloop()