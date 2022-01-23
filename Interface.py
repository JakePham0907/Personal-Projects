
import sqlite3

import os
import smtplib

import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter import messagebox


import datetime
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta

import re   

import uuid


def TableCreation():
    conn = sqlite3.connect('ClientInformation.db')
    curs = conn.cursor()

    open("ClientInformation.db","w")        # opens or creates a file name ClientInformation

# This whole section refreshes / creates the tables and inserts values into the TreatmentPrice Table   
    curs.execute("""CREATE TABLE Client (
        [Last Name] VARCHAR,
        [First Name] VARCHAR,
        [Email Address] VARCHAR PRIMARY KEY,
        [Phone Number] VARCHAR)
        """)

    curs.execute("""CREATE TABLE TreatmentPrice (
        Treatment VARCHAR PRIMARY KEY,
        Price NUMERIC)
        """)                

    curs.execute("""CREATE TABLE Appointments (
        AppointmentID VARCHAR PRIMARY KEY,
        [Email Address] VARCHAR REFERENCES Client ([EmailAddress]),
        [Date Booked] DATE,
        [Time Booked] TIME,
        Treatment VARCHAR REFERENCES TreatmentPrice(Treatment),
        Paid BOOLEAN)
        """)

# 2D Array for the values to be inputted into TreatmentPrice Table
    ServiceMenu = [
        ("Infill Acryllic",14.99),
        ("Infill Gel Powder",17.99),
        ("Full Set Acryllic",24.99),
        ("Full Set Gel Powder",29.99),
        ("SNS/Dipping Powder", 24.99),
        ("Manicure",11.99),
        ("Pedicure",21.99),
        ("Manicure & Pedicure",29.99),
        ("Manicure w/ Shellac",24.99),
        ("Pedicure w/ Shellac",34.99),
        ("Manicure & Pedicure w/ Shellac",52.99)]


    
    try:
        sql = "INSERT INTO TreatmentPrice([Treatment], [Price]) VALUES(?,?)"
        curs.executemany(sql,ServiceMenu)
        conn.commit()
        print("Treatment price added")
    except sqlite3.Error as e:
        print("An error occured: " + e.args[0])

    conn.close()


def GoToWindow(FromPage, ToPage):
    FromPage.grid_remove()
    ToPage.grid(row=0,column=8)

def RefreshCommand():
    conn = sqlite3.connect('ClientInformation.db')
    curs = conn.cursor()
    
    answer = tk.messagebox.askyesno(title = "Refresh Database",message = "Are you sure you wish to refresh your database?")

    if answer :
        TableCreation()

def startMenu(MenuFrame):

    # Creating the Buttons
    labelTitle = Label(MenuFrame,text="Main menu",width = 100)
    clientInfo = Button(MenuFrame,text = "Enter New Client Info", command = lambda:GoToWindow(MenuFrame,(ClientFrame)))
    bookingCreate = Button(MenuFrame,text = "Create New Booking",command = lambda:GoToWindow(MenuFrame,(BookingFrame)))
    databaseView = Button(MenuFrame,text = "Open Database",command = lambda:GoToWindow(MenuFrame,(ViewClientFrame)))
    payWindow = Button(MenuFrame,text = "Payment Window",command = lambda:GoToWindow(MenuFrame,(PayFrame)))
    RefreshButton = Button(MenuFrame, text = "Refresh Database", command = lambda:RefreshCommand())                                   #   Gridding the Buttons

    labelTitle.grid(row=0,column=0, pady=12, padx = 50)
    clientInfo.grid(row = 1, column = 0)
    bookingCreate.grid(row = 2, column = 0)
    databaseView.grid(row = 3, column = 0)
    payWindow.grid(row = 4, column = 0)
    RefreshButton.grid(row = 5, column = 0)




def addClientData(entLName, entFName, entEmail, entPhoneNumber):
    #retrieve the data from the entries
    conn = sqlite3.connect('ClientInformation.db')
    curs = conn.cursor()

    
    Lastname = entLName.get()
    Firstname = entFName.get()
    Email = entEmail.get()
    PhoneNumber = entPhoneNumber.get()
    
    
                #put the values in a tuple to be added to the database
    clientRecord = (Lastname,Firstname,Email,PhoneNumber)

                #attempt to add to the database
    try:
        curs.execute ("INSERT INTO Client([Last Name], [First name], [Email Address], [Phone Number]) VALUES(?,?,?,?)",clientRecord)
        conn.commit() #will not keep data if this instruction is ommitted
        conn.close()
        print("Client Information added!")

    except sqlite3.Error as e:
        print("An error occurred: " + e.args[0])


def emailValidation(entLName, entFName, entEmail, entPhoneNumber):

    Email = entEmail.get()

    emailFormat = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[-]?\w+[.]\w{2,3}$"

    ValidEmail = False

    def check(email):   
  
        if(re.search(emailFormat,email)):   
            ValidEmail = True   
        else:   
            tk.messagebox.showerror(title="ERROR", message="Email is Invalid!")
    return ValidEmail

    if check(Email):
        addClientData(entLName, entFName, entEmail, entPhoneNumber)

##    ValidStepOne = False
##    ValidStepTwo = False
##    ValidityResult = False
##    
##
##    for i in range(len(Email)):
##        if Email[i] == "@":
##            ValidStepOne = True
##
##    for i in range(len(Email)):
##        if Email[i] == ".":
##            if (Email[i+1] + Email[i+2] + Email[i+3]) == "com":
##                ValidStepTwo = True
##            elif (Email[i+1] + Email[i+2] + Email[i+3] + Email[i+4] + Email[i+5]) == "co.uk":
##                ValidStepTwo = True
##
##    if ValidStepOne == True and ValidStepTwo == True:
##        ValidityResult = True
##
##    if ValidityResult:
##        print("IT WORKS FAM")
##
##    return ValidityResult

        
def createClientWidgets(ClientFrame,MenuFrame):

    conn = sqlite3.connect('ClientInformation.db')
    curs = conn.cursor()
   
        
    TitleLabel = Label(ClientFrame,text = "Create a new Client", font = ("Arial",18),bg = "white",width = 25)
    TitleLabel.grid(row=0,column=0, pady=12, padx = 50)    
    #Name labelling and gridding
    surNameLabel = Label(ClientFrame,text = "Surname:",bg = "Sienna")
    surNameEntry = Entry(ClientFrame)
    firstNameLabel = Label(ClientFrame,text = "Firstname:",bg = "Sienna")
    firstNameEntry = Entry(ClientFrame)

    surNameLabel.grid(row = 1, column = 0)
    surNameEntry.grid(row = 1, column = 1)
    firstNameLabel.grid(row = 2, column = 0)
    firstNameEntry.grid(row = 2, column = 1)

    #Contact Information inputting
    emailLabel = Label(ClientFrame,text = "Email Address:",bg = "Sienna")
    emailEntry = Entry(ClientFrame)
    
    telephoneLabel = Label(ClientFrame,text = "Phone Number:",bg = "Sienna")
    telephoneEntry = Entry(ClientFrame)

    emailLabel.grid(row = 3, column = 0)
    emailEntry.grid(row = 3, column = 1)
    telephoneLabel.grid(row = 4, column = 0)
    telephoneEntry.grid(row = 4, column = 1)
    
    BackButton = Button(ClientFrame,text="Main Menu",command = lambda:GoToWindow(ClientFrame, MenuFrame))
    BackButton.grid(row = 6,column = 2)


    saveDetails = Button(ClientFrame,text = "Save details", command = lambda:addClientData(surNameEntry,firstNameEntry,emailEntry,telephoneEntry)) # Details are saved to Client Table
    saveDetails.grid(row = 5, column = 2)

    conn.close()


def SearchCustomers():  #https://www.youtube.com/watch?v=odt87CeLlro This is a Video by Codemy which talks about how to create a search engine that takes data from the SQLite database

    conn = sqlite3.connect('ClientInformation.db')
    curs = conn.cursor()

    SearchCustomers = Tk()
    SearchCustomers.title("Look for a client")
    SearchCustomers.geometry("1200x600")

    DropBox = ttk.Combobox(SearchCustomers, value=["Search by:","[Last Name]","[First Name]","[Email Address]","[Phone Number]"])
    DropBox.current(0)
    DropBox.grid(row=0,column=2)
    
    def Search(tree):
        for i in tree.get_children():
            tree.delete(i)
        
        searched = searchBox.get()
        SQLQuery = "SELECT * FROM Client WHERE "+DropBox.get()+" = '"+searched+"'"
        print(SQLQuery)
        curs.execute(SQLQuery)
        result = curs.fetchall()

        count = 0
        for client in result:
            tree.insert("",count,text="",values = (client[0],client[1],client[2],client[3]))
            count += 1

        scrollbar = ttk.Scrollbar(SearchCustomers,orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=3, column=1, sticky='ns')


    searchBox = Entry(SearchCustomers)
    searchBox.grid(row = 0, column = 1, padx = 10, pady = 10)

    SearchBoxLabel = Label(SearchCustomers, text = "Search Clients: ")
    SearchBoxLabel.grid(row=0, column=0, padx=10, pady=10)

    columns = ("1", "2", "3", "4")
    tree = ttk.Treeview(SearchCustomers,columns=columns, show='headings')
    tree.grid(row=3, column=0,pady = 10)

    tree.heading("1", text = "Last Name")
    tree.heading("2", text = "First Name")
    tree.heading("3", text = "Email")
    tree.heading("4", text = "Phone Number")

    SearchButton = Button(SearchCustomers, text="Search Clients", command = lambda:Search(tree))
    SearchButton.grid(row=1,column=0,padx=10)


def addAppointmentData(entEmail, entDateYear, entDateMonth, entDateDay, entHour, entMinute, entTreatment):
    conn = sqlite3.connect('ClientInformation.db')
    curs = conn.cursor()

    currentDateTime = date.today()

    
            
    Email = entEmail.get()
    DateSetConvert = date(int(entDateYear.get()),int(entDateMonth.get()),int(entDateDay.get()))
    Time = entHour.get()+":"+entMinute.get()
    Treatment = entTreatment.get()
    ID = str(uuid.uuid4())[:4] #https://stackoverflow.com/questions/13484726/safe-enough-8-character-short-unique-random-string
    Paid = "No"

    DateCheck = False

    print(DateSetConvert)
    print(Time)
    print(currentDateTime)

    if DateSetConvert >= currentDateTime:
        DateCheck = True
    else:
        tk.messagebox.showerror(title="ERROR", message="Date is Invalid!")
        
    appointmentRecord = (ID,Email,DateSetConvert,Time,Treatment,Paid)

                #attempt to add to the database
    
    if DateCheck == True:
        try:
            curs.execute ("INSERT INTO Appointments([AppointmentID], [Email Address], [Date Booked], [Time Booked],[Treatment],[Paid]) VALUES(?,?,?,?,?,?)",appointmentRecord)
            conn.commit() #will not keep data if this instruction is ommitted
            conn.close()
            print("Information added!")

        except sqlite3.Error as e:
            print("An error occurred: " + e.args[0])


def createBookingWidgets(BookingFrame,MenuFrame):

    conn = sqlite3.connect('ClientInformation.db')
    curs = conn.cursor()
    
    TodayDateTime = datetime.now()
    
    TitleLabel = Label(BookingFrame,text = "Book an Appointment", font = ("Arial",18),bg = "white",width = 25)
    TitleLabel.grid(row=0,column=0, pady=12, padx = 50)

    emailLabel = Label(BookingFrame,text = "Email Address:",bg = "cyan")
    emailEntry = Entry(BookingFrame)
    clientSearch = Button(BookingFrame, text = "Search for Client",command=SearchCustomers)
    dateLabel = Label(BookingFrame,text = "Date booked(YYYY/MM/DD):",bg = "cyan")
    #dateEntry = Entry(BookingFrame)

    dateEntryYear = tk.Spinbox(BookingFrame,from_= TodayDateTime.year, to=9999, bg="lightblue",width=4)

    currentMonth = TodayDateTime.month
    currentDay = TodayDateTime.day
    
    dateEntryMonth = tk.Spinbox(BookingFrame,from_= 1, to = 12,textvariable = TodayDateTime.month, bg="lightblue",width=2)
    dateEntryDay = tk.Spinbox(BookingFrame, from_= 1, to = 31,textvariable = TodayDateTime.day, bg="lightblue",width=2)

    timeLabel = Label(BookingFrame,text = "Time booked(Hrs/Min):",bg = "cyan")
    hourEntry = tk.Spinbox(BookingFrame,from_=1, to=24,bg="lightblue",width=2)
    minEntry = tk.Spinbox(BookingFrame,width=2,values=(0,15,30,45),bg="cyan")

    emailLabel.grid(row = 2,column = 0)
    emailEntry.grid(row = 2, column = 1)
    clientSearch.grid(row = 2, column = 2, padx = 5)
    dateLabel.grid(row = 3,column = 0)
    dateEntryYear.grid(row = 3,column = 1)
    dateEntryMonth.grid(row = 3,column = 2)
    dateEntryDay.grid(row = 3,column = 3)
    timeLabel.grid(row = 4,column = 0)
    hourEntry.grid(row = 4,column = 1)
    minEntry.grid(row = 4, column = 2, pady = 10)
    
    serviceSVar = StringVar()
    serviceSVar.set("Nail Treatment")


    bookingRadInfillAcryllic = Radiobutton(BookingFrame, text="Infill Acryllic",variable=serviceSVar,value = "Infill Acryllic",bg = "cyan")
    bookingRadInfillGelPowder = Radiobutton(BookingFrame, text="Infill Gel Powder",variable=serviceSVar,value = "Infill Gel Powder",bg = "cyan")
    
    bookingRadFullSetAcryllic= Radiobutton(BookingFrame, text="Full Set Acryllic",variable=serviceSVar,value = "Full Set Acryllic",bg = "cyan")
    bookingRadFullSetGelPowder = Radiobutton(BookingFrame, text="Full Set Gel Powder",variable=serviceSVar,value = "Full Set Gel Powder",bg = "cyan")
    
    bookingRadManicure = Radiobutton(BookingFrame, text="Manicure",variable=serviceSVar,value = "Manicure",bg = "cyan")
    bookingRadPedicure = Radiobutton(BookingFrame, text="Pedicure",variable=serviceSVar,value = "Pedicure",bg = "cyan")
    bookingRadManicurePedicure = Radiobutton(BookingFrame, text="Manicure & Pedicure",variable=serviceSVar,value = "Manicure & Pedicure",bg = "cyan")   
    
    bookingRadManicureShellac = Radiobutton(BookingFrame, text="Manicure w/ Shellac",variable=serviceSVar,value = "Manicure w/ Shellac",bg = "cyan")
    bookingRadPedicureShellac = Radiobutton(BookingFrame, text="Pedicure w/ Shellac",variable=serviceSVar,value = "Pedicure w/ Shellac",bg = "cyan")
    bookingRadManiPediShellac = Radiobutton(BookingFrame, text="Manicure & Pedicure w/ Shellac",variable=serviceSVar,value = "Manicure & Pedicure w/ Shellac",bg = "cyan")



    bookingRadInfillAcryllic.grid(row = 5, column = 0,sticky="W")
    bookingRadInfillGelPowder.grid(row = 6, column = 0,sticky="W")

    bookingRadFullSetAcryllic.grid(row = 7, column = 0,sticky="W")
    bookingRadFullSetGelPowder.grid(row = 8, column = 0,sticky="W")

    bookingRadManicure.grid(row = 9, column = 0,sticky="W")
    bookingRadPedicure.grid(row = 10, column = 0,sticky="W")
    bookingRadManicurePedicure.grid(row = 11, column = 0,sticky="W")

    bookingRadManicureShellac.grid(row = 12, column = 0,sticky="W")
    bookingRadPedicureShellac.grid(row = 13, column = 0,sticky="W")
    bookingRadManiPediShellac.grid(row = 14, column = 0,sticky="W")


    BackButton = Button(BookingFrame,text="Main Menu",command = lambda:GoToWindow(BookingFrame, MenuFrame))
    BackButton.grid(row = 7,column = 2)

    saveDetails = Button(BookingFrame,text = "Save details", command = lambda:addAppointmentData(emailEntry,dateEntryYear,dateEntryMonth,dateEntryDay,hourEntry,minEntry,serviceSVar))
    saveDetails.grid(row = 5, column = 2)




def DeleteClientData(tree):
    conn = sqlite3.connect('CLientInformation.db')
    curs = conn.cursor()

    selected = tree.selection()

    query = ("DELETE FROM [Client] WHERE [Email Address] = %s")
    rs = curs.execute(query, selected)

    if(rs.rowcount==1):
        tree.delete(x)

    print(rs)

    conn.execute()

def DeleteAppointmentData(tree):
    conn = sqlite3.connect('CLientInformation.db')
    curs = conn.cursor()

    selectedData = tree.selection()
    selectedInfo = tree.get_children()# Selects the Tree row
    print(selectedInfo)
    #tree.delete(selectedData)  # Deletes the selected Tree row

    ### GET SELECT TO READ THE APPOINTMENT ID / FIRST CRITERIA. USE APPOINTMENT ID TO DELETE INFORMATION FROM DATABASE
            
    #deleteDataQuery = curs.execute("DELETE FROM [Appointments] WHERE [AppointmentID] = '"+selectedData+"'") #TODO: Fix data type (Str, not Tuple)
    #deleteData.commit(selectedData)
    #print(selected)

    conn.execute()
    
def databaseView(ViewClientFrame,MenuFrame):
    
    conn = sqlite3.connect('ClientInformation.db')
    curs = conn.cursor()

    
    databaseLabel = Label(ViewClientFrame, text = "Current Client List", font = ("Arial",18),bg = "lightgreen",width = 25)
    databaseLabel.grid(row = 0, column = 0)
    
    columns = ("1", "2", "3", "4")
    tree = ttk.Treeview(ViewClientFrame, columns=columns, show='headings')
    tree.grid(row=1, column=0)

    tree.heading("1", text = "Last Name")
    tree.heading("2", text = "First Name")
    tree.heading("3", text = "Email")
    tree.heading("4", text = "Phone Number")

    curs.execute("SELECT * FROM Client ORDER BY [Last Name]")
    allClients = curs.fetchall()
    count = 0

    for client in allClients:
        values = (client[0],client[1],client[2],client[3])
        tree.insert("",count,text="",values = values)
        count += 1
     
    scrollbar = ttk.Scrollbar(ViewClientFrame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=1, column=1, sticky='ns')


    #dataFrame = LabelFrame(ViewClientFrame, text = "Record")
    #dataFrame.pack(fill="x", expand = "yes", padx=20)

    fName_label = Label(ViewClientFrame, text = "First Name")
    sName_label = Label(ViewClientFrame, text = "Last Name")
    EAddr_label = Label(ViewClientFrame, text = "Email Address")
    PNumb_label = Label(ViewClientFrame, text = "Phone Number")

    fName_label.grid(row=5, column=1, padx=10, pady=10)
    sName_label.grid(row=5, column=2, padx=10, pady=10)
    EAddr_label.grid(row=5, column=3, padx=10, pady=10)
    PNumb_label.grid(row=5, column=4, padx=10, pady=10)

    fName_entry = Entry(ViewClientFrame, text = "First Name")
    sName_entry = Entry(ViewClientFrame, text = "Last Name")
    EAddr_entry = Entry(ViewClientFrame, text = "Email Address")
    PNumb_entry = Entry(ViewClientFrame, text = "Phone Number")

    fName_entry.grid(row=6, column=1, padx=10, pady=10)
    sName_entry.grid(row=6, column=2, padx=10, pady=10)
    EAddr_entry.grid(row=6, column=3, padx=10, pady=10)
    PNumb_entry.grid(row=6, column=4, padx=10, pady=10)

    def selectData():
        fName_entry.delete(0, END)
        sName_entry.delete(0, END)
        EAddr_entry.delete(0, END)
        PNumb_entry.delete(0, END)

        selected = tree.focus()
        values = tree.item(selected, 'values')

        fName_entry.insert(0, values[0])
        sName_entry.insert(0, values[1])
        EAddr_entry.insert(0, values[2])
        PNumb_entry.insert(0, values[3])
        
##    curs.execute("""UPDATE Client SET
##        LastName = :last,
##        FirstName = :first,
##        EmailAddress = :email,
##        PhoneNumb = :phonenumber,
##
##        WHERE [Last Name] = :last""",
##        {
##           "first" : fName_entry.get(),
##           "last" : lName_entry.get(),
##           "email" : EAddr_entry.get(),
##           "phonenumber" : PNumb_entry.get()}
##        )
##
##    fName_entry.delete(0, END)
##    lName_entry.delete(0, END)
##    EAddr_entry.delete(0, END)
##    PNumb_entry.delete(0, END)

    conn.commit()
    conn.close()

    SwitchButton = Button(ViewClientFrame,text="Appointments",command = lambda:GoToWindow(ViewClientFrame, ViewAppointmentFrame))
    SwitchButton.grid(row = 4,column = 2)

    SelectButton = Button(ViewClientFrame, text="Show Selected", command = selectData())
    SelectButton.grid(row = 4, column = 0)

    BackButton = Button(ViewClientFrame,text="Main Menu",command = lambda:GoToWindow(ViewClientFrame, MenuFrame))
    BackButton.grid(row = 1,column = 2)




    def AppointmentInfo(ViewAppointmentFrame, ViewClientFrame, MenuFrame):
            
        conn = sqlite3.connect('ClientInformation.db')
        curs = conn.cursor()

        
        databaseLabel = Label(ViewAppointmentFrame, text = "Current Appointment List", font = ("Arial",18),bg = "lightgreen",width = 25)
        databaseLabel.grid(row = 0, column = 0)
        
        columns = ("1", "2", "3", "4", "5","6")
        tree = ttk.Treeview(ViewAppointmentFrame, columns=columns, show='headings')
        tree.grid(row=1, column=0)
        
        tree.heading("1", text = "Appointment ID")
        tree.heading("2", text = "Email")
        tree.heading("3", text = "Date Booked")
        tree.heading("4", text = "Time Booked")
        tree.heading("5", text = "Treatment")
        tree.heading("6", text = "Paid?")

        curs.execute("SELECT * FROM Appointments ORDER BY [Date Booked] ASC , [Time Booked] ASC")   # Selects all appointments and orders them by date and time
        allAppointments = curs.fetchall()
        count = 0

        for appointment in allAppointments:
            tree.insert("",count,text="",values = (appointment[0],appointment[1],appointment[2],appointment[3],appointment[4],appointment[5]))
            count += 1
  
        scrollbar = ttk.Scrollbar(ViewClientFrame, orient=tk.VERTICAL, command=tree.yview) #Inserts a Scrollbar
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky='ns')


        SwitchButton = Button(ViewAppointmentFrame,text="Client List",command = lambda:GoToWindow(ViewAppointmentFrame, ViewClientFrame))
        SwitchButton.grid(row = 4,column = 2)

        DeleteButton = Button(ViewAppointmentFrame, text="Delete Selected", command = lambda:DeleteAppointmentData(tree))
        DeleteButton.grid(row = 4, column = 0)
        
        BackButton = Button(ViewAppointmentFrame,text="Main Menu",command = lambda:GoToWindow(ViewAppointmentFrame, MenuFrame))
        BackButton.grid(row = 1,column = 2)

    AppointmentInfo(ViewAppointmentFrame, ViewClientFrame, MenuFrame)

    

def addPayConfirmation(entAppID,entPaid):
    conn = sqlite3.connect('ClientInformation.db')
    curs = conn.cursor()
    conn.execute()

### THIS SECTION DOES NOT WORK ON SCHOOL COMPUTERS AND REQUIRES USAGE OF OS ENVIROMENT ###  
    Paid = entPaid.get()
    AppID = entAppID.get()

    EMAIL_ADDRESS = os.environ.get('DB_USER')
    EMAIL_PASSWORD =  os.environ.get('DB_PASS')

    #Price = curs.execute("

    if Paid == "Yes":
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

            subject = "Nail Technicion Invoice"
            body = "Thank you for purchasing my services. Your payment has gone through."

            msg = f'Subject:{subject}\n\n{body}'

            smtp.sendmail(EMAIL_ADDRESS, EmailAddressEntry.get(), msg)
            
    try:
        curs.execute ("UPDATE Appointments SET Paid ='"+Paid+"'WHERE [AppointmentID] ='"+AppID+"'")
        conn.commit()
        conn.close()
        print("Information added!")

    except sqlite3.Error as e:
        print("An error occurred: " + e.args[0])

    conn.execute()

def getPayCost(entAppID):
    conn = sqlite3.connect('ClientInformation.db')
    curs = conn.cursor()

    AppID = entAppID.get()

    Price = curs.execute("""SELECT [Price] FROM Appointments, TreatmentPrice
                    WHERE AppointmentID = '"""+AppID+"""' AND
                    WHERE Appointment.Treatment = TreatmentPrice.Treatment""")
    print(Price)

    AppointmentInfo = curs.execute("SELECT * FROM Appointments WHERE AppointmentID = '"+AppID+"'")


    TotalPrice = Price * 1.2 #20% VAT

    DisplayString = ""
    DisplayString += "Service Cost :" + Price + "\nPlus VAT :" + TotalPrice + "\n"

    DisplayPrice.config(text = DisplayString)

    
def createPayWindow(PayFrame,MenuFrame):

    conn = sqlite3.connect('ClientInformation.db')
    curs = conn.cursor()        
            
    AppointmentIDLabel = Label(PayFrame,text = "Appointment ID:")
    AppointmentIDEntry = Entry(PayFrame)
    EmailAddressLabel = Label(PayFrame, text = "Email Address of Buyer:")
    EmailAddressEntry = Entry(PayFrame)

    AppointmentIDLabel.grid(row=0,column=0)
    AppointmentIDEntry.grid(row=0,column=1)
    EmailAddressLabel.grid(row=1,column=0)
    EmailAddressEntry.grid(row=1,column=1)

    paidSVar = StringVar()
    paidSVar.set("No")
    RadPaidNo = Radiobutton(PayFrame, text="No",variable=paidSVar,value = "No",bg = "cyan")
    RadPaidYes = Radiobutton(PayFrame, text="Yes",variable=paidSVar,value = "Yes",bg = "cyan")
    RadPaidNo.grid(row = 3,column = 0)
    RadPaidYes.grid(row = 3, column = 1)

    BillingInformation = Button(PayFrame, text = "Display Cost", command = lambda:getPayCost(AppointmentIDEntry))
    BillingInformation.grid(row = 5, column = 2)
    
    saveDetails = Button(PayFrame,text = "Save details", command=lambda:addPayConfirmation(AppointmentIDEntry,paidSVar))
    saveDetails.grid(row = 6, column = 2)

    DisplayPrice = Label(PayFrame, height=6, width = 50,bg="yellow")
    DisplayPrice.grid(row = 6, column = 0)

    BackButton = Button(PayFrame,text="Main Menu",command = lambda:GoToWindow(PayFrame, MenuFrame))
    BackButton.grid(row = 4,column = 2)


root = Tk()
root.title("Nail Technician's Appointment Bookings")

#TableCreation()

MenuFrame = Frame(root,bg="Grey")
ClientFrame = Frame(root,bg="Sienna")
BookingFrame = Frame(root,bg="cyan")
ViewClientFrame = Frame(root,bg ="lightgreen")
PayFrame = Frame(root,bg = "cyan")
ViewAppointmentFrame = Frame(root,bg = "lightgreen")

startMenu(MenuFrame)
createClientWidgets(ClientFrame,MenuFrame)
createBookingWidgets(BookingFrame,MenuFrame)
databaseView(ViewClientFrame,MenuFrame)
createPayWindow(PayFrame,MenuFrame)
MenuFrame.grid(row=0,column=0)

root.mainloop()
