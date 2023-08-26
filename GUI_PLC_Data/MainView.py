import tkinter
from tkinter import *
import ViewInit as vi
import GUICommandBase as gcb
from datetime import datetime
from tkcalendar import *
import ploting as plot


class MainView(vi.ViewInit):

    def __init__(self):
        super().__init__()
        self.command = gcb.GUICommandBase()
        self.chosenPeriodLabel = Label(self.root, text="Not applied", font=("Helvetica", 14), fg="white", bg="black")
        self.chosenPeriodLabel.place(x=150, y=415)
        self.infoPlateLabel = Label(self.root, text="Info Plate", font=("Helvetica", 14), fg="white", bg="black")
        self.infoPlateLabel.place(x=25, y=600)
        # vars for date and tiem
        self.dateFrom = 0
        self.timeFrom = 0
        self.dateTo = 0
        self.timeTo = 0
        self.sec_sb_from = 0
        self.min_sb_from = 0
        self.hour_sb_from = 0
        self.cal_from = 0
        self.cal_to = 0
        self.allDateFrom = 0
        self.allDateTo = 0
        # var for tanks
        self.selectedTank = ''
        self.tankListBox = 0

        # process params
        self.currentLevel = []
        self.currentControl = []
        self.currentAlarms_1 = []
        self.currentAlarms_2 = []
        self.currentAlarms_3 = []
        self.currentAlarms_4 = []
        self.currentAlarms_5 = []
        self.currentDisFlow = []
        self.setPoint = []
        self.param_1_tank = []
        self.param_2_tank = []
        self.param_3_tank = []
# ==== > Save selected tank do var < ==== #
    def items_selected(self, event):
        # get selected indices
        selected_indices = self.tankListBox.curselection()
        # get selected items
        self.selectedTank = ",".join([self.tankListBox.get(i) for i in selected_indices])
        msg = f'You selected: {self.selectedTank}'
# ==== > END Save selected tank do var < ==== #

# ==== > Function showing current choosed period < ==== #
    def ShowChossedPeriod(self):
        self.dateFrom = self.command.newFormatDate(self.cal_from.get_date(), '%m/%d/%y', '%d.%m.%Y')
        self.dateTo = self.command.newFormatDate(self.cal_to.get_date(), '%m/%d/%y', '%d.%m.%Y')
        HourF = self.hour_sb_from.get()
        if int(HourF) < 10:
            HourF = "0" + HourF
        MinuteF = self.min_sb_from.get()
        if int(MinuteF) < 10:
            MinuteF = "0" + MinuteF
        SecondF = self.sec_sb_from.get()
        if int(SecondF) < 10:
            SecondF = "0" + SecondF

        self.timeFrom = HourF + ":" + MinuteF + ":" + SecondF

        HourT = self.hour_sb_to.get()
        if int(HourT) < 10:
            HourT = "0" + HourT
        MinuteT = self.min_sb_to.get()
        if int(MinuteT) < 10:
            MinuteT = "0" + MinuteT
        SecondT = self.sec_sb_to.get()
        if int(SecondT) < 10:
            SecondT = "0" + SecondT


        self.timeTo = HourT + ":" + MinuteT + ":" + SecondT

        text = "From: " + self.dateFrom + " " \
               + self.timeFrom + " to: " + self.dateTo + " " + self.timeTo
        self.chosenPeriodLabel.destroy()
        self.chosenPeriodLabel = Label(self.root, text=text, font=("Helvetica", 14), fg="white", bg="black")
        self.chosenPeriodLabel.place(x=150, y=415)
        self.allDateFrom = self.dateFrom + " " + self.timeFrom
        self.allDateTo = self.dateTo + " " + self.timeTo
        self.allDateFrom = self.command.newFormatDate(self.allDateFrom, '%d.%m.%Y %H:%M:%S', '%Y-%m-%d %H:%M:%S')
        self.allDateTo = self.command.newFormatDate(self.allDateTo, '%d.%m.%Y %H:%M:%S', '%Y-%m-%d %H:%M:%S')
# ==== > END Function showing current choosed period < ==== #

# ==== > Function for ploting all data for selected Tank < ==== #
    def plotCharts(self):
        date = []
        # here take all data
        data = self.command.readDataForCharts(self.selectedTank, self.allDateFrom, self.allDateTo)
        if data[0] == 0:
            self.infoPlateLabel.destroy()
            self.infoPlateLabel = Label(self.root, text="No data in this period", font=("Helvetica", 14), fg="white", bg="black")
            self.infoPlateLabel.place(x=25, y=600)
        else:
            self.infoPlateLabel.destroy()
            self.infoPlateLabel = Label(self.root, text="Generating charts", font=("Helvetica", 14),
                                        fg="white", bg="black")
            self.infoPlateLabel.place(x=25, y=600)

            # clear all arrays before next ploting
            self.currentLevel.clear()
            self.setPoint.clear()
            self.currentAlarms_1.clear()
            self.currentAlarms_2.clear()
            self.currentAlarms_3.clear()
            self.currentAlarms_4.clear()
            self.currentAlarms_5.clear()
            self.param_1_tank.clear()
            self.param_2_tank.clear()
            self.param_3_tank.clear()
            self.currentControl.clear()
            self.currentDisFlow.clear()
            date.clear()
            # current level and set point
            for item in data[1]:
                self.currentLevel.append(item[2])
                date.append(item[3])
            for item in data[2]:
                self.setPoint.append(item[2])
            plot.plotcurrentLevelAndSetPoint(date, self.currentLevel, 'Date and time', 'Current Level',
                                             'Level: ' + self.selectedTank, self.setPoint)

            # alarms and params
            for item in data[3]:
                self.currentAlarms_1.append(item[3])
            for item in data[4]:
                self.currentAlarms_2.append(item[3])
            for item in data[5]:
                self.currentAlarms_3.append(item[3])
            for item in data[6]:
                self.currentAlarms_4.append(item[3])
            for item in data[7]:
                self.currentAlarms_5.append(item[3])
            if self.selectedTank == 'Zbiornik_1':
                for item in data[8]:
                    if item[2] == 1:
                        self.param_1_tank.append(item[3])
                    elif item[2] == 5:
                        self.param_2_tank.append(item[3])
            elif self.selectedTank == 'Zbiornik_2':
                for item in data[8]:
                    if item[2] == 2:
                        self.param_1_tank.append(item[3])
                    elif item[2] == 3:
                        self.param_2_tank.append(item[3])
                    elif item[2] == 4:
                        self.param_3_tank.append(item[3])
            elif self.selectedTank == 'Zbiornik_3':
                for item in data[8]:
                    if item[2] == 2:
                        self.param_1_tank.append(item[3])
                    elif item[2] == 3:
                        self.param_2_tank.append(item[3])
                    elif item[2] == 5:
                        self.param_3_tank.append(item[3])

            plot.plotAlarmsAndParams(date, self.currentAlarms_1, self.currentAlarms_2,
                                     self.currentAlarms_3, self.currentAlarms_4, self.currentAlarms_5,
                                     'Date and time', 'Alarm', 'Value of Params',
                                     'Detected Alarm for: ' + self.selectedTank, 'Params for: ' + self.selectedTank,
                                     self.param_1_tank, self.param_2_tank, self.param_3_tank)
            # current DisFlow
            for item in data[9]:
                self.currentDisFlow.append(item[2])
            # current Control
            for item in data[10]:
                self.currentControl.append(item[2])
            plot.plotDisFlowAndControl(date, self.currentDisFlow, self.currentControl,
                                        'Date and time', 'Current Flow', 'Current Control',
                                       'Current Flow for: ' + self.selectedTank,
                                       'Current Control for: ' + self.selectedTank)
            plot.showCharts()
# ==== > END Function for ploting all data for selected Tank < ==== #

# ==== > Show main interface < ==== #
    def ShowMain(self):
        pixelVirtual = PhotoImage(width=1, height=1)
        # delete all data form data base
        deleteAllDataButton = Button(self.root, text="Delete All Data", image=pixelVirtual, width=105, height=50,
                                    compound='c', fg="white", bg="#29a329",
                                    command=lambda: self.command.deleteAllaData())
        deleteAllDataButton.place(x=700, y=25)
        # apply period
        applyPeriodButton = Button(self.root, text="Apply period", image=pixelVirtual, width=105, height=50,
                                     compound='c', fg="white", bg="#29a329",
                                     command=lambda: self.ShowChossedPeriod())
        applyPeriodButton.place(x=25, y=400)

        # show charts
        showCharts = Button(self.root, text="Show Charts", image=pixelVirtual, width=105, height=50,
                            compound='c', fg="white", bg="#29a329",
                            command=lambda: self.plotCharts())
        showCharts.place(x=170, y=500)

        # label for choose time period
        calLabel = Label(self.root, text="Choose time period", font=("Helvetica", 14), bg="orange", fg="white", pady=10,
                        width=47)
        calLabel.place(x=25, y=25)

        # labels
        fromLabel = Label(self.root, text="From", font=("Helvetica", 14), fg="white", bg="black")
        fromLabel.place(x=125, y=80)

        toLabel = Label(self.root, text="To", font=("Helvetica", 14), fg="white", bg="black")
        toLabel.place(x=410, y=80)

        fromLabelTime = Label(self.root, text="Hr          Min         Sec", font=("Helvetica", 12), fg="white", bg="black")
        fromLabelTime.place(x=65, y=360)

        toLabelTime = Label(self.root, text="Hr          Min         Sec", font=("Helvetica", 12), fg="white", bg="black")
        toLabelTime.place(x=335, y=360)

        # calendar
        dt = datetime.now()
        day = dt.day
        month = dt.month
        year = dt.year
        # calender from
        self.cal_from = Calendar(self.root, selectmode="day", year=year, month=month, day=day)
        self.cal_from.pack()
        self.cal_from.place(x=25, y=120)
        # calender to
        self.cal_to = Calendar(self.root, selectmode="day", year=year, month=month, day=day)
        self.cal_to.pack()
        self.cal_to.place(x=295, y=120)

        # clock time
        hour_string_form = StringVar()
        min_string_form = StringVar()
        sec_string_form = StringVar()
        hour_string_to = StringVar()
        min_string_to = StringVar()
        sec_string_to = StringVar()
        f = ('Times', 20)

        # clock time from
        self.sec_sb_from = Spinbox(self.root, from_=0, to=59, wrap=True, textvariable=sec_string_form, font=f, width=2,
                              justify=CENTER)
        self.min_sb_from = Spinbox(self.root, from_=0, to=59, wrap=True, textvariable=min_string_form, font=f, width=2,
                              justify=CENTER)
        self.hour_sb_from = Spinbox(self.root, from_=0, to=23, wrap=True, textvariable=hour_string_form, font=f, width=2,
                               justify=CENTER)
        self.hour_sb_from.pack()
        self.hour_sb_from.place(x=65, y=320)
        self.min_sb_from.pack()
        self.min_sb_from.place(x=125, y=320)
        self.sec_sb_from.pack()
        self.sec_sb_from.place(x=185, y=320)

        # clock time to
        self.sec_sb_to = Spinbox(self.root, from_=0, to=59, wrap=True, textvariable=sec_string_to, font=f, width=2,
                            justify=CENTER)
        self.min_sb_to = Spinbox(self.root, from_=0, to=59, wrap=True, textvariable=min_string_to, font=f, width=2,
                            justify=CENTER)
        self.hour_sb_to = Spinbox(self.root, from_=0, to=23, wrap=True, textvariable=hour_string_to, font=f, width=2,
                             justify=CENTER)
        self.hour_sb_to.pack()
        self.hour_sb_to.place(x=335, y=320)
        self.min_sb_to.pack()
        self.min_sb_to.place(x=395, y=320)
        self.sec_sb_to.pack()
        self.sec_sb_to.place(x=455, y=320)

        # listbox itah tanks
        tanks = ('Zbiornik_1', 'Zbiornik_2', 'Zbiornik_3')
        var = tkinter.Variable(value= tanks)
        self.tankListBox = Listbox(self.root, listvariable=var, height=3, selectmode=tkinter.EXTENDED)
        self.tankListBox.pack()
        self.tankListBox.place(x=25, y=500)
        chooseTankLabel = Label(self.root, text="Choose Tank", font=("Helvetica", 14), fg="white", bg="black")
        chooseTankLabel.place(x=25, y=460)
        self.tankListBox.bind('<<ListboxSelect>>', self.items_selected)
        self.tankListBox.select_set(0)  # This only sets focus on the first item.
        self.tankListBox.event_generate("<<ListboxSelect>>")

        self.root.mainloop()
# ==== > END Show main interface < ==== #
