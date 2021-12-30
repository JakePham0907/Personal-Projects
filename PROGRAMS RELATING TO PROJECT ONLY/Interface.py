
import sqlite3

import os
import smtplib

import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import showinfo

import datetime
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta

##def connectDatabase():
##    conn = sqlite3.connect('ClientInformation.db')
##    curs = conn.cursor()

def TableCreation():
    conn = sqlite3.connect('ClientInformation.db')
    curs = conn.cursor()
    curs.commit()

    open("ClientInformation.db","w")        # opens or creates a file name ClientInformation

# This whole section creates the tables and inserts values into the TreatmentPrice Table   
    curs.execute("""CREATE TABLE if not exists Client (
        [Last Name] VARCHAR,
        [First Name] VARCHAR,
        [Email Address] VARCHAR PRIMARY KEY,
        [Phone Number] VARCHAR)
        """)

    curs.execute("""CREATE TABLE if not exists TreatmentPrice (
        Treatment VARCHAR PRIMARY KEY,
        Price NUMERIC)
        """)                

    curs.execute("""CREATE TABLE if not exists Appointments (
        AppointmentID VARCHAR PRIMARY KEY,
        [Email Address] VARCHAR REFERENCES Client ([EmailAddress]),
        [Date Booked] DATE,
        [Time Booked] TIME,
        Treatment VARCHAR REFERENCES TreatmentPrice(Treatment),
        Paid BOOLEAN)
        """)

# 2D Array for the values to be inputted into TreatmentPrice Table
    ServiceMenu = [
        ["Pedicure",39.99],
        ["Nail Treatment",24.99],
        ["Nail Art",14.99],
        ["Pedicure + Acrylic", 59.99],
    ]

    try:
        sql = "INSERT INTO TreatmentPrice(Treatment, Price) VALUES(?,?)"
        curs.executemany(sql,ServiceMenu)
        print("Treatment price added")
    except sqlite3.Error as e:
        print("An error occured: " + e.args[0])

    conn.commit()

def GoToWindow(FromPage, ToPage):
    FromPage.grid_remove()
    ToPage.grid(row=0,column=8)

def startMenu(MenuFrame):

    #Creating the Buttons
    labelTitle = Label(MenuFrame,text="Main menu",width = 100)
    clientInfo = Button(MenuFrame,text = "Enter New Client Info", command = lambda:GoToWindow(MenuFrame,(ClientFrame)))
    bookingCreate = Button(MenuFrame,text = "Create New Booking",command = lambda:GoToWindow(MenuFrame,(BookingFrame)))
    databaseView = Button(MenuFrame,text = "Open Database",command = lambda:GoToWindow(MenuFrame,(ViewClientFrame)))
    payWindow = Button(MenuFrame,text = "Payment Window",command = lambda:GoToWindow(MenuFrame,(PayFrame)))

    labelTitle.grid(row=0,column=0, pady=12, padx = 50)
    clientInfo.grid(row = 1, column = 0)
    bookingCreate.grid(row = 2, column = 0)
    databaseView.grid(row = 3, column = 0)
    payWindow.grid(row = 4, column = 0)



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
        print("Client Information added!")

    except sqlite3.Error as e:
        print("An error occurred: " + e.args[0])

def emailValidation(entEmail):

    Email = entEmail.get()

    ValidStepOne = False
    ValidStepTwo = False
    ValidityResult = False
    

    for i in range(len(Email)):
        if Email[i] == "@":
            ValidStepOne = True

    for i in range(len(Email)):
        if Email[i] == ".":
            if (Email[i+1] + Email[i+2] + Email[i+3]) == "com" or (Email[i+1] + Email[i+2] + Email[i+3] + Email[i+4] + Email[i+5]) == "co.uk":
                ValidStepTwo = True

    if ValidStepOne == True and ValidStepTwo == True:
        ValidityResult = True

    return ValidityResult
        

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


    saveDetails = Button(ClientFrame,text = "Save details", command = lambda:emailValidation) 
    if saveDetails == True:
        addClientData(surNameEntry,firstNameEntry,emailEntry,telephoneEntry)

#   saveDetails = Button(ClientFrame,text = "Save details", command = lambda:addClientData(surNameEntry,firstNameEntry,emailEntry,telephoneEntry)) # Details are saved to Client Table
    saveDetails.grid(row = 5, column = 2)



def SearchCustomers():

    conn = sqlite3.connect('ClientInformation.db')
    curs = conn.cursor()
    curs.commit()

    
    SearchCustomers = Tk()
    SearchCustomers.title("Look for a client")
    SearchCustomers.geometry("1200x600")

##    DropBox = ttk.Combobox(SearchCustomers, value=["Search by:","Last Name","First Name","Email Address","Phone Number"])
##    DropBox.current(0)
##    DropBox.grid(row=0,column=2)
    
    def Search(tree):
        for i in tree.get_children():
            tree.delete(i)
        
        searched = searchBox.get()
        SQLQuery = "SELECT * FROM Client WHERE [Last Name] = '"+searched+"'"
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

        

##        if not result:
##            result = "Record Not Found..."
##
##        
##        SearchLabel = Label(SearchCustomers, text=result)
##        SearchLabel.grid(row=1,column=1, padx = 10, columnspan = 2)

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
    curs.commit()


    currentDateTime = date.today()
    
    def getLatestID():
        try:
            curs.execute("SELECT AppointmentID FROM Appointments ORDER BY AppointmentID DESC")
            record = curs.fetchall()
            print(record)
               
        except sqlite3.Error as err: print("An error occured", err)
            
    Email = entEmail.get()
    DateSetConvert = date(int(entDateYear.get()),int(entDateMonth.get()),int(entDateDay.get()))
    Time = entHour.get()+":"+entMinute.get()
    Treatment = entTreatment.get()
    ID = getLatestID()
    Paid = "No"

    DateCheck = False

    print(DateSetConvert)
    print(Time)
    print(currentDateTime)

    if DateSetConvert >= currentDateTime:
        DateCheck = True
    else:
        tk.messagebox.showerror(title="ERROR", message="Date is Invalid!",)
        
    appointmentRecord = (ID,Email,DateSetConvert,Time,Treatment,Paid)

                #attempt to add to the database
    
    if DateCheck == True:
        try:
            curs.execute ("INSERT INTO Appointments([AppointmentID], [Email Address], [Date Booked], [Time Booked],[Treatment],[Paid]) VALUES(?,?,?,?,?,?)",appointmentRecord)
            conn.commit() #will not keep data if this instruction is ommitted
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
    dateEntryMonth = tk.Spinbox(BookingFrame,from_= 1, to = 12, bg="lightblue",width=2)
    dateEntryDay = tk.Spinbox(BookingFrame, from_= 1, to = 31, bg="lightblue",width=2)

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

    bookingRadNailTreatment = Radiobutton(BookingFrame, text="Nail Treatment",variable=serviceSVar,value = "Nail Treatment",bg = "cyan")
    bookingRadPedicure = Radiobutton(BookingFrame, text="Pedicure",variable=serviceSVar,value = "Pedicure",bg = "cyan")
    bookingRadNailArt = Radiobutton(BookingFrame, text="Nail Art",variable=serviceSVar,value = "Nail Art",bg = "cyan")
    
    bookingRadNailTreatment.grid(row = 5, column = 0,sticky="W")
    bookingRadPedicure.grid(row = 6, column = 0,sticky="W")
    bookingRadNailArt.grid(row = 7, column = 0,sticky="W")

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

def DeleteAppointmentData(tree):
    conn = sqlite3.connect('CLientInformation.db')
    curs = conn.cursor()

    y = tree.selection()
    tree.delete(y)
            
    deleteDataQuery = curs.execute("DELETE FROM [Appointments] WHERE [AppointmentID] = '"+y+"'")
    deleteData.commit(y)
    print(selected)
    
def databaseView(ViewClientFrame,MenuFrame):

    conn = sqlite3.connect('ClientInformation.db')
    curs = conn.cursor()
    conn.commit()
    
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
        tree.insert("",count,text="",values = (client[0],client[1],client[2],client[3]))
        count += 1
     
    scrollbar = ttk.Scrollbar(ViewClientFrame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=1, column=1, sticky='ns')

    SwitchButton = Button(ViewClientFrame,text="Appointments",command = lambda:GoToWindow(ViewClientFrame, ViewAppointmentFrame))
    SwitchButton.grid(row = 4,column = 2)

    DeleteButton = Button(ViewClientFrame, text="Delete Selected", command = lambda:DeleteClientData(tree))
    DeleteButton.grid(row = 4, column = 0)

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

### THIS SECTION DOES NOT WORK ON SCHOOL COMPUTERS AND REQUIRES USAGE OF OS ENVIROMENT ###  
    Paid = entPaid.get()
    AppID = entAppID.get()

    EMAIL_ADDRESS = os.environ.get('DB_USER')
    EMAIL_PASSWORD =  os.environ.get('DB_PASS')

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
        print("Information added!")

    except sqlite3.Error as e:
        print("An error occurred: " + e.args[0])

def getPayCost(entAppID):
    conn = sqlite3.connect('ClientInformation.db')
    curs = conn.cursor()

    Price = curs.execute("""SELECT * FROM Appointments, TreatmentPrice
                    WHERE AppointmentID = '"""+AppID+"""' AND
                    WHERE Appointment.Treatment = TreatmentPrice.Treatment""")

    
    

def createPayWindow(PayFrame,MenuFrame):

    conn = sqlite3.connect('ClientInformation.db')
    curs = conn.cursor()
    
##    def emailsendtest(EmailAddressEntry):                                                      
##                                                                                               
##        EMAIL_ADDRESS = os.environ.get('DB_USER')
##        EMAIL_PASSWORD =  os.environ.get('DB_PASS')
##
##        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
##            smtp.ehlo()
##            smtp.starttls()
##            smtp.ehlo()
##
##            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
##
##            subject = "Nail Technicion Invoice"
##            body = "Thank you for purchasing my services. Your payment has gone through."
##
##            msg = f'Subject:{subject}\n\n{body}'
##
##            smtp.sendmail(EMAIL_ADDRESS, EmailAddressEntry.get(), msg)
            
            
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

    saveDetails = Button(PayFrame,text = "Save details", command=lambda:addPayConfirmation(AppointmentIDEntry,paidSVar))
    saveDetails.grid(row = 5, column = 2)

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
