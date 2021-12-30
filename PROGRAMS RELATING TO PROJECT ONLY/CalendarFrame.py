import calendar
from calendar import TextCalendar
import datetime
import sys
import csv

class CalendarFrame:
        def __init__(self, parent, values):
		self.values = values
		self.parent = parent
		
		self.cal = TextCalendar(calendar.SUNDAY)
		self.year = datetime.date.today().year
		self.month = datetime.date.today().month

		self.yearSelected = self.year
		self.monthSelected = self.month
		self.daySelected = 1
	
	
    # Moves to previous month/year on calendar
        def PreviousMonth(self):
	    if self.month == 1:
                self.month = 12
                self.year -= 1
            else:
                self.month -= 1
                    
	
    # Moves to next month/year on calendar
        def NextMonth(self):
            if self.month == 12:
                self.month = 1
                self.year += 1
            else:
                self.month += 1


    # Calls upon the date selected
        def dateSelect(self,day):
            self.daySelected = day
            self.monthSelected = self.month
            self.yearSelected = self.year
            
            self.values["daySelected"] = day
            self.values["monthSelected"] = self.month
            self.values["yearSelected"] = self.year
            self.values["monthName"] = calendar.monthName[self.monthSelected]

            self.setup(self.year, self.month)

        def CalendarInterface(self, year, month):
            left = tk.Button(self.parent, text="<<",command=lambda:PreviousMonth(self), bg = "cyan")
            right = tk.Button(self.parent, text=">>",command=lambda:NextMonth(self), bg = "cyan")
            
